from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Count
from django.core.cache import cache
from .models import Artist
from .serializers import ArtistSerializer, ArtistCreateSerializer, ArtistStatsSerializer


class StandardResultsSetPagination(PageNumberPagination):
    """Paginação padrão"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class ArtistListView(generics.ListAPIView):
    """Lista de artistas"""
    queryset = Artist.objects.filter(is_active=True)
    serializer_class = ArtistSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        """Filtros de busca"""
        queryset = super().get_queryset()
        
        # Filtro por gênero
        genre = self.request.query_params.get('genre')
        if genre:
            queryset = queryset.filter(genre__icontains=genre)
        
        # Filtro por verificação
        verified = self.request.query_params.get('verified')
        if verified is not None:
            queryset = queryset.filter(verified=verified.lower() == 'true')
        
        # Filtro por localização
        location = self.request.query_params.get('location')
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        # Busca por nome artístico
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(stage_name__icontains=search) |
                Q(real_name__icontains=search) |
                Q(bio__icontains=search)
            )
        
        # Ordenação
        ordering = self.request.query_params.get('ordering', '-followers_count')
        queryset = queryset.order_by(ordering)
        
        return queryset


class ArtistDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhes do artista"""
    queryset = Artist.objects.filter(is_active=True)
    serializer_class = ArtistSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_permissions(self):
        """Permissões baseadas na ação"""
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class ArtistCreateView(generics.CreateAPIView):
    """Criação de artista"""
    queryset = Artist.objects.all()
    serializer_class = ArtistCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        """Define o usuário como o usuário logado"""
        serializer.save(user=self.request.user)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def popular_artists_view(request):
    """Artistas populares (com cache)"""
    cache_key = 'popular_artists'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return Response(cached_data)
    
    # Buscar artistas populares
    artists = Artist.objects.filter(
        is_active=True,
        followers_count__gte=1000
    ).order_by('-followers_count')[:10]
    
    serializer = ArtistSerializer(artists, many=True)
    data = {
        'artists': serializer.data,
        'count': len(serializer.data)
    }
    
    # Cache por 1 hora
    cache.set(cache_key, data, 3600)
    
    return Response(data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def trending_artists_view(request):
    """Artistas em alta"""
    # Artistas com mais seguidores na última semana
    from django.utils import timezone
    from datetime import timedelta
    
    week_ago = timezone.now() - timedelta(days=7)
    
    artists = Artist.objects.filter(
        is_active=True,
        created_at__gte=week_ago
    ).order_by('-followers_count')[:10]
    
    serializer = ArtistSerializer(artists, many=True)
    
    return Response({
        'artists': serializer.data,
        'count': len(serializer.data)
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def artist_stats_view(request, pk):
    """Estatísticas do artista"""
    try:
        artist = Artist.objects.get(pk=pk, is_active=True)
    except Artist.DoesNotExist:
        return Response(
            {'error': 'Artista não encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = ArtistStatsSerializer(artist)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_artist_view(request, pk):
    """Seguir/deixar de seguir artista"""
    try:
        artist = Artist.objects.get(pk=pk, is_active=True)
    except Artist.DoesNotExist:
        return Response(
            {'error': 'Artista não encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Verificar se já está seguindo
    # Aqui você implementaria a lógica de seguir/seguidores
    # Por enquanto, apenas incrementa os seguidores
    
    action = request.data.get('action', 'follow')
    
    if action == 'follow':
        artist.increment_followers()
        message = f'Agora você está seguindo {artist.stage_name}'
    elif action == 'unfollow':
        artist.decrement_followers()
        message = f'Você parou de seguir {artist.stage_name}'
    else:
        return Response(
            {'error': 'Ação inválida. Use "follow" ou "unfollow"'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    return Response({
        'message': message,
        'followers_count': artist.followers_count
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def artist_musics_view(request, pk):
    """Músicas do artista"""
    try:
        artist = Artist.objects.get(pk=pk, is_active=True)
    except Artist.DoesNotExist:
        return Response(
            {'error': 'Artista não encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    musics = artist.musics.filter(is_active=True).order_by('-streams_count')
    
    # Paginação manual
    page_size = int(request.query_params.get('page_size', 20))
    page = int(request.query_params.get('page', 1))
    
    start = (page - 1) * page_size
    end = start + page_size
    
    musics_page = musics[start:end]
    
    from apps.music.serializers import MusicSerializer
    serializer = MusicSerializer(musics_page, many=True)
    
    return Response({
        'musics': serializer.data,
        'count': musics.count(),
        'page': page,
        'page_size': page_size,
        'total_pages': (musics.count() + page_size - 1) // page_size
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def genres_view(request):
    """Lista de gêneros disponíveis"""
    genres = Artist.objects.filter(
        is_active=True,
        genre__isnull=False
    ).exclude(genre='').values_list('genre', flat=True).distinct()
    
    return Response({
        'genres': sorted(list(genres)),
        'count': len(genres)
    })