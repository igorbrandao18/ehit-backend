from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from .models import Artist, Album
from .serializers import ArtistSerializer, ArtistCreateSerializer, AlbumSerializer, AlbumCreateSerializer


class StandardResultsSetPagination(PageNumberPagination):
    """Paginação padrão"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class ArtistListView(generics.ListAPIView):
    """Lista de artistas com cache Redis"""
    queryset = Artist.objects.filter(is_active=True)
    serializer_class = ArtistSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.AllowAny]
    
    @method_decorator(cache_page(60 * 15))  # Cache por 15 minutos
    @method_decorator(vary_on_headers('Authorization'))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        """Filtros de busca com cache"""
        # Criar chave de cache baseada nos parâmetros
        cache_key = f"artists_list_{self.request.query_params.get('genre', '')}_{self.request.query_params.get('search', '')}_{self.request.query_params.get('ordering', '-created_at')}"
        
        # Tentar buscar do cache primeiro
        cached_queryset = cache.get(cache_key)
        if cached_queryset is not None:
            return cached_queryset
        
        queryset = super().get_queryset()
        
        # Filtro por gênero
        genre = self.request.query_params.get('genre')
        if genre:
            queryset = queryset.filter(genre__name__icontains=genre)
        
        # Busca por nome artístico
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(stage_name__icontains=search)
        
        # Ordenação
        ordering = self.request.query_params.get('ordering', '-created_at')
        queryset = queryset.order_by(ordering)
        
        # Cache por 10 minutos
        cache.set(cache_key, queryset, 60 * 10)
        
        return queryset


class ArtistDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhes do artista com cache Redis"""
    queryset = Artist.objects.filter(is_active=True)
    serializer_class = ArtistSerializer
    permission_classes = [permissions.AllowAny]
    
    @method_decorator(cache_page(60 * 30))  # Cache por 30 minutos
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ArtistCreateView(generics.CreateAPIView):
    """Criação de artista"""
    queryset = Artist.objects.all()
    serializer_class = ArtistCreateSerializer
    permission_classes = [permissions.AllowAny]


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
@cache_page(60 * 20)  # Cache por 20 minutos
def active_artists_view(request):
    """Artistas ativos com cache Redis"""
    cache_key = "active_artists"
    
    # Tentar buscar do cache primeiro
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return Response(cached_data)
    
    artists = Artist.objects.filter(
        is_active=True
    ).order_by('-created_at')
    
    serializer = ArtistSerializer(artists, many=True)
    
    response_data = {
        'artists': serializer.data,
        'count': len(serializer.data)
    }
    
    # Cache por 15 minutos
    cache.set(cache_key, response_data, 60 * 15)
    
    return Response(response_data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def artist_complete_view(request, pk):
    """Artista completo com álbuns e músicas - cache Redis"""
    cache_key = f"artist_complete_{pk}"
    
    # Tentar buscar do cache primeiro
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return Response(cached_data)
    
    try:
        artist = Artist.objects.get(pk=pk, is_active=True)
    except Artist.DoesNotExist:
        return Response(
            {'error': 'Artista não encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Serializar artista
    artist_serializer = ArtistSerializer(artist)
    
    # Buscar álbuns do artista
    albums = artist.albums.filter(is_active=True).order_by('-featured', '-release_date', '-created_at')
    albums_serializer = AlbumSerializer(albums, many=True)
    
    # Buscar músicas do artista
    musics = artist.musics.filter(is_active=True).order_by('-streams_count', '-created_at')
    from apps.music.serializers import MusicSerializer
    musics_serializer = MusicSerializer(musics, many=True)
    
    response_data = {
        'artist': artist_serializer.data,
        'albums': albums_serializer.data,
        'musics': musics_serializer.data,
        'albums_count': albums.count(),
        'musics_count': musics.count()
    }
    
    # Cache por 20 minutos
    cache.set(cache_key, response_data, 60 * 20)
    
    return Response(response_data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
@cache_page(60 * 20)  # Cache por 20 minutos
def artist_albums_view(request, pk):
    """Álbuns do artista com cache Redis"""
    cache_key = f"artist_albums_{pk}"
    
    # Tentar buscar do cache primeiro
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return Response(cached_data)
    
    try:
        artist = Artist.objects.get(pk=pk, is_active=True)
    except Artist.DoesNotExist:
        return Response(
            {'error': 'Artista não encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Buscar álbuns do artista
    albums = artist.albums.filter(is_active=True).order_by('-featured', '-release_date', '-created_at')
    albums_serializer = AlbumSerializer(albums, many=True)
    
    response_data = {
        'artist': {
            'id': artist.id,
            'stage_name': artist.stage_name,
            'photo': artist.photo.url if artist.photo else None,
        },
        'albums': albums_serializer.data,
        'count': albums.count()
    }
    
    # Cache por 15 minutos
    cache.set(cache_key, response_data, 60 * 15)
    
    return Response(response_data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def artist_with_musics_view(request, pk):
    """Artista com suas músicas"""
    try:
        artist = Artist.objects.get(pk=pk, is_active=True)
    except Artist.DoesNotExist:
        return Response(
            {'error': 'Artista não encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Serializar artista
    artist_serializer = ArtistSerializer(artist)
    
    # Buscar músicas do artista com paginação
    musics = artist.musics.filter(is_active=True).order_by('-streams_count', '-created_at')
    
    # Paginação manual
    page_size = int(request.query_params.get('page_size', 20))
    page = int(request.query_params.get('page', 1))
    
    start = (page - 1) * page_size
    end = start + page_size
    
    musics_page = musics[start:end]
    from apps.music.serializers import MusicSerializer
    musics_serializer = MusicSerializer(musics_page, many=True)
    
    return Response({
        'artist': artist_serializer.data,
        'musics': musics_serializer.data,
        'count': musics.count(),
        'page': page,
        'page_size': page_size,
        'total_pages': (musics.count() + page_size - 1) // page_size
    })


# =============================================================================
# ALBUM VIEWS
# =============================================================================

class AlbumListView(generics.ListAPIView):
    """
    Lista de álbuns com filtros avançados e cache Redis
    
    Query Parameters:
    - artist: ID do artista para filtrar álbuns
    - featured: true/false para filtrar álbuns em destaque
    - search: busca por nome do álbum
    - ordering: ordenação (padrão: -featured, -release_date, -created_at)
    - page_size: tamanho da página (padrão: 20)
    
    Exemplos:
    - GET /api/artists/albums/?artist=1
    - GET /api/artists/albums/?featured=true
    - GET /api/artists/albums/?search=rock
    """
    queryset = Album.objects.filter(is_active=True)
    serializer_class = AlbumSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.AllowAny]
    
    @method_decorator(cache_page(60 * 15))  # Cache por 15 minutos
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        """Filtros de busca avançados com cache"""
        # Criar chave de cache baseada nos parâmetros
        cache_key = f"albums_list_{self.request.query_params.get('artist', '')}_{self.request.query_params.get('featured', '')}_{self.request.query_params.get('search', '')}_{self.request.query_params.get('genre', '')}_{self.request.query_params.get('ordering', '-featured')}"
        
        # Tentar buscar do cache primeiro
        cached_queryset = cache.get(cache_key)
        if cached_queryset is not None:
            return cached_queryset
        
        queryset = super().get_queryset()
        
        # Filtro por artista (ID)
        artist_id = self.request.query_params.get('artist')
        if artist_id:
            try:
                queryset = queryset.filter(artist__id=int(artist_id))
            except (ValueError, TypeError):
                pass  # Ignorar IDs inválidos
        
        # Filtro por nome do artista
        artist_name = self.request.query_params.get('artist_name')
        if artist_name:
            queryset = queryset.filter(artist__stage_name__icontains=artist_name)
        
        # Filtro por destaque
        featured = self.request.query_params.get('featured')
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(featured=True)
        elif featured and featured.lower() == 'false':
            queryset = queryset.filter(featured=False)
        
        # Busca por nome do álbum
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        # Filtro por gênero do artista
        genre = self.request.query_params.get('genre')
        if genre:
            queryset = queryset.filter(artist__genre__name__icontains=genre)
        
        # Ordenação personalizada
        ordering = self.request.query_params.get('ordering')
        if ordering:
            queryset = queryset.order_by(ordering)
        else:
            # Ordenação padrão: destaque primeiro, depois data de lançamento
            queryset = queryset.order_by('-featured', '-release_date', '-created_at')
        
        # Cache por 10 minutos
        cache.set(cache_key, queryset, 60 * 10)
        
        return queryset


class AlbumDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhes do álbum com cache Redis"""
    queryset = Album.objects.filter(is_active=True)
    serializer_class = AlbumSerializer
    permission_classes = [permissions.AllowAny]
    
    @method_decorator(cache_page(60 * 30))  # Cache por 30 minutos
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AlbumCreateView(generics.CreateAPIView):
    """Criação de álbum"""
    queryset = Album.objects.all()
    serializer_class = AlbumCreateSerializer
    permission_classes = [permissions.AllowAny]


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
@cache_page(60 * 20)  # Cache por 20 minutos
def featured_albums_view(request):
    """Álbuns em destaque com cache Redis"""
    cache_key = "featured_albums"
    
    # Tentar buscar do cache primeiro
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return Response(cached_data)
    
    albums = Album.objects.filter(
        is_active=True,
        featured=True
    ).order_by('-release_date', '-created_at')
    
    serializer = AlbumSerializer(albums, many=True)
    
    response_data = {
        'albums': serializer.data,
        'count': len(serializer.data)
    }
    
    # Cache por 15 minutos
    cache.set(cache_key, response_data, 60 * 15)
    
    return Response(response_data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def album_musics_view(request, pk):
    """Músicas do álbum com cache Redis"""
    cache_key = f"album_musics_{pk}_{request.query_params.get('page', 1)}_{request.query_params.get('page_size', 20)}"
    
    # Tentar buscar do cache primeiro
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return Response(cached_data)
    
    try:
        album = Album.objects.get(pk=pk, is_active=True)
    except Album.DoesNotExist:
        return Response(
            {'error': 'Álbum não encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    musics = album.musics.filter(is_active=True).order_by('-created_at')
    
    # Paginação manual
    page_size = int(request.query_params.get('page_size', 20))
    page = int(request.query_params.get('page', 1))
    
    start = (page - 1) * page_size
    end = start + page_size
    
    musics_page = musics[start:end]
    
    from apps.music.serializers import MusicSerializer
    serializer = MusicSerializer(musics_page, many=True)
    
    response_data = {
        'musics': serializer.data,
        'count': musics.count(),
        'page': page,
        'page_size': page_size,
        'total_pages': (musics.count() + page_size - 1) // page_size
    }
    
    # Cache por 10 minutos
    cache.set(cache_key, response_data, 60 * 10)
    
    return Response(response_data)