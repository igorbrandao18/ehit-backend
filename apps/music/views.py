from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Count
from django.core.cache import cache
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework.exceptions import PermissionDenied
from datetime import timedelta
from .models import Music
from .serializers import (
    MusicSerializer, MusicCreateSerializer, MusicStatsSerializer, 
    MusicTrendingSerializer, MusicAutocompleteSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    """Paginação padrão"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class MusicListView(generics.ListAPIView):
    """Lista de músicas com cache Redis"""
    queryset = Music.objects.filter(is_active=True)
    serializer_class = MusicSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.AllowAny]
    
    @method_decorator(cache_page(60 * 15))  # Cache por 15 minutos
    @method_decorator(vary_on_headers('Authorization'))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        """Filtros de busca com cache"""
        # Criar chave de cache baseada nos parâmetros
        cache_key = f"musics_list_{self.request.query_params.get('artist', '')}_{self.request.query_params.get('genre', '')}_{self.request.query_params.get('album', '')}_{self.request.query_params.get('featured', '')}_{self.request.query_params.get('search', '')}_{self.request.query_params.get('ordering', '-streams_count')}"
        
        # Tentar buscar do cache primeiro
        cached_queryset = cache.get(cache_key)
        if cached_queryset is not None:
            return cached_queryset
        
        queryset = super().get_queryset()
        
        # Filtro por artista
        artist_id = self.request.query_params.get('artist')
        if artist_id:
            queryset = queryset.filter(artist_id=artist_id)
        
        # Filtro por gênero
        genre = self.request.query_params.get('genre')
        if genre:
            queryset = queryset.filter(genre__icontains=genre)
        
        # Filtro por álbum (ID)
        album_id = self.request.query_params.get('album')
        if album_id:
            try:
                queryset = queryset.filter(album__id=int(album_id))
            except (ValueError, TypeError):
                pass  # Ignorar IDs inválidos
        
        # Filtro por nome do álbum
        album_name = self.request.query_params.get('album_name')
        if album_name:
            queryset = queryset.filter(album__name__icontains=album_name)
        
        # Filtro por destaque
        featured = self.request.query_params.get('featured')
        if featured is not None:
            queryset = queryset.filter(is_featured=featured.lower() == 'true')
        
        # Busca por título/artista/álbum
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(artist__stage_name__icontains=search) |
                Q(album__name__icontains=search)
            )
        
        # Ordenação
        ordering = self.request.query_params.get('ordering', '-streams_count')
        queryset = queryset.order_by(ordering)
        
        # Cache por 10 minutos
        cache.set(cache_key, queryset, 60 * 10)
        
        return queryset


class MusicDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhes da música com cache Redis"""
    queryset = Music.objects.filter(is_active=True)
    serializer_class = MusicSerializer
    permission_classes = [permissions.AllowAny]
    
    @method_decorator(cache_page(60 * 30))  # Cache por 30 minutos
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_permissions(self):
        """Permissões baseadas na ação"""
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class MusicCreateView(generics.CreateAPIView):
    """Criação de música"""
    queryset = Music.objects.all()
    serializer_class = MusicCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        """Define o artista como o usuário logado"""
        # Para simplificar, vamos permitir criação sem verificação de perfil
        # Em um ambiente real, você implementaria a lógica de perfil de artista
        pass


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def trending_music_view(request):
    """Músicas em alta (com cache)"""
    cache_key = 'trending_music'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return Response(cached_data)
    
    # Músicas criadas na última semana com mais de 100 streams
    week_ago = timezone.now() - timedelta(days=7)
    
    musics = Music.objects.filter(
        is_active=True,
        created_at__gte=week_ago,
        streams_count__gte=100
    ).order_by('-streams_count')[:20]
    
    serializer = MusicTrendingSerializer(musics, many=True)
    data = {
        'musics': serializer.data,
        'count': len(serializer.data)
    }
    
    # Cache por 30 minutos
    cache.set(cache_key, data, 1800)
    
    return Response(data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def popular_music_view(request):
    """Músicas populares (com cache)"""
    cache_key = 'popular_music'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return Response(cached_data)
    
    # Músicas com mais de 1000 streams
    musics = Music.objects.filter(
        is_active=True,
        streams_count__gte=1000
    ).order_by('-streams_count')[:20]
    
    serializer = MusicTrendingSerializer(musics, many=True)
    data = {
        'musics': serializer.data,
        'count': len(serializer.data)
    }
    
    # Cache por 1 hora
    cache.set(cache_key, data, 3600)
    
    return Response(data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def featured_music_view(request):
    """Músicas em destaque com cache Redis"""
    cache_key = "featured_music"
    
    # Tentar buscar do cache primeiro
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return Response(cached_data)
    
    musics = Music.objects.filter(
        is_active=True,
        is_featured=True
    ).order_by('-streams_count')
    
    serializer = MusicTrendingSerializer(musics, many=True)
    
    response_data = {
        'musics': serializer.data,
        'count': len(serializer.data)
    }
    
    # Cache por 20 minutos
    cache.set(cache_key, response_data, 60 * 20)
    
    return Response(response_data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def stream_music_view(request, pk):
    """Incrementar contador de streams"""
    try:
        music = Music.objects.get(pk=pk, is_active=True)
    except Music.DoesNotExist:
        return Response(
            {'error': 'Música não encontrada'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Incrementar streams
    music.increment_streams()
    
    return Response({
        'message': 'Stream contabilizado',
        'streams_count': music.streams_count
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def download_music_view(request, pk):
    """Incrementar contador de downloads"""
    try:
        music = Music.objects.get(pk=pk, is_active=True)
    except Music.DoesNotExist:
        return Response(
            {'error': 'Música não encontrada'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Incrementar downloads
    music.increment_downloads()
    
    return Response({
        'message': 'Download contabilizado',
        'downloads_count': music.downloads_count
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_music_view(request, pk):
    """Curtir/descurtir música"""
    try:
        music = Music.objects.get(pk=pk, is_active=True)
    except Music.DoesNotExist:
        return Response(
            {'error': 'Música não encontrada'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    action = request.data.get('action', 'like')
    
    if action == 'like':
        music.increment_likes()
        message = 'Música curtida'
    elif action == 'unlike':
        music.decrement_likes()
        message = 'Curtida removida'
    else:
        return Response(
            {'error': 'Ação inválida. Use "like" ou "unlike"'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    return Response({
        'message': message,
        'likes_count': music.likes_count
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def music_stats_view(request, pk):
    """Estatísticas da música com cache Redis"""
    cache_key = f"music_stats_{pk}"
    
    # Tentar buscar do cache primeiro
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return Response(cached_data)
    
    try:
        music = Music.objects.get(pk=pk, is_active=True)
    except Music.DoesNotExist:
        return Response(
            {'error': 'Música não encontrada'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = MusicStatsSerializer(music)
    
    # Cache por 15 minutos
    cache.set(cache_key, serializer.data, 60 * 15)
    
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def genres_view(request):
    """Lista de gêneros disponíveis"""
    genres = Music.objects.filter(
        is_active=True,
        genre__isnull=False
    ).exclude(genre='').values_list('genre', flat=True).distinct()
    
    return Response({
        'genres': sorted(list(genres)),
        'count': len(genres)
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def music_autocomplete_view(request):
    """
    Endpoint de autocomplete para busca de músicas com cache Redis
    Busca por título, artista ou álbum com limite de resultados
    
    Parâmetros:
    - q: termo de busca (obrigatório, mínimo 2 caracteres)
    - limit: limite de resultados (padrão: 10, máximo: 20)
    - type: tipo de busca ('all', 'title', 'artist', 'album')
    """
    query = request.query_params.get('q', '').strip()
    limit = min(int(request.query_params.get('limit', 10)), 20)
    search_type = request.query_params.get('type', 'all')
    
    if not query or len(query) < 2:
        return Response({
            'results': [],
            'count': 0,
            'message': 'Digite pelo menos 2 caracteres para buscar'
        })
    
    # Criar chave de cache baseada nos parâmetros
    cache_key = f"music_autocomplete_{query}_{limit}_{search_type}"
    
    # Tentar buscar do cache primeiro
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return Response(cached_data)
    
    # Construir query baseada no tipo de busca
    queryset = Music.objects.filter(is_active=True)
    
    if search_type == 'title':
        queryset = queryset.filter(title__icontains=query)
    elif search_type == 'artist':
        queryset = queryset.filter(artist__stage_name__icontains=query)
    elif search_type == 'album':
        queryset = queryset.filter(album__name__icontains=query)
    else:  # 'all'
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(artist__stage_name__icontains=query) |
            Q(album__name__icontains=query)
        )
    
    # Busca otimizada com limite de resultados
    musics = queryset.select_related('artist').order_by('-streams_count')[:limit]
    
    serializer = MusicAutocompleteSerializer(musics, many=True)
    
    response_data = {
        'results': serializer.data,
        'count': len(serializer.data),
        'query': query,
        'search_type': search_type,
        'limit': limit
    }
    
    # Cache por 5 minutos
    cache.set(cache_key, response_data, 60 * 5)
    
    return Response(response_data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def albums_view(request):
    """Lista de álbuns disponíveis"""
    albums = Music.objects.filter(
        is_active=True,
        album__isnull=False
    ).exclude(album='').values_list('album', flat=True).distinct()
    
    return Response({
        'albums': sorted(list(albums)),
        'count': len(albums)
    })