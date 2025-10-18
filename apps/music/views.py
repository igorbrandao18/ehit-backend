from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Count
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
from .models import Music
from .serializers import (
    MusicSerializer, MusicCreateSerializer, MusicStatsSerializer, MusicTrendingSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    """Paginação padrão"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class MusicListView(generics.ListAPIView):
    """Lista de músicas"""
    queryset = Music.objects.filter(is_active=True)
    serializer_class = MusicSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        """Filtros de busca"""
        queryset = super().get_queryset()
        
        # Filtro por artista
        artist_id = self.request.query_params.get('artist')
        if artist_id:
            queryset = queryset.filter(artist_id=artist_id)
        
        # Filtro por gênero
        genre = self.request.query_params.get('genre')
        if genre:
            queryset = queryset.filter(genre__icontains=genre)
        
        # Filtro por álbum
        album = self.request.query_params.get('album')
        if album:
            queryset = queryset.filter(album__icontains=album)
        
        # Filtro por destaque
        featured = self.request.query_params.get('featured')
        if featured is not None:
            queryset = queryset.filter(is_featured=featured.lower() == 'true')
        
        # Busca por título/artista
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(artist__stage_name__icontains=search) |
                Q(album__icontains=search)
            )
        
        # Ordenação
        ordering = self.request.query_params.get('ordering', '-streams_count')
        queryset = queryset.order_by(ordering)
        
        return queryset


class MusicDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhes da música"""
    queryset = Music.objects.filter(is_active=True)
    serializer_class = MusicSerializer
    permission_classes = [permissions.AllowAny]
    
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
        # Verificar se o usuário é um artista
        if not self.request.user.is_artist:
            raise permissions.PermissionDenied("Apenas artistas podem criar músicas.")
        
        # Obter o perfil do artista
        try:
            artist = self.request.user.artist_profile
        except:
            raise permissions.PermissionDenied("Perfil de artista não encontrado.")
        
        serializer.save(artist=artist)


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
    """Músicas em destaque"""
    musics = Music.objects.filter(
        is_active=True,
        is_featured=True
    ).order_by('-streams_count')
    
    serializer = MusicTrendingSerializer(musics, many=True)
    
    return Response({
        'musics': serializer.data,
        'count': len(serializer.data)
    })


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
    """Estatísticas da música"""
    try:
        music = Music.objects.get(pk=pk, is_active=True)
    except Music.DoesNotExist:
        return Response(
            {'error': 'Música não encontrada'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = MusicStatsSerializer(music)
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