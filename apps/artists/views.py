from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Artist, Album
from .serializers import ArtistSerializer, ArtistCreateSerializer, AlbumSerializer, AlbumCreateSerializer


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
            queryset = queryset.filter(genre__name__icontains=genre)
        
        # Busca por nome artístico
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(stage_name__icontains=search)
        
        # Ordenação
        ordering = self.request.query_params.get('ordering', '-created_at')
        queryset = queryset.order_by(ordering)
        
        return queryset


class ArtistDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhes do artista"""
    queryset = Artist.objects.filter(is_active=True)
    serializer_class = ArtistSerializer
    permission_classes = [permissions.AllowAny]


class ArtistCreateView(generics.CreateAPIView):
    """Criação de artista"""
    queryset = Artist.objects.all()
    serializer_class = ArtistCreateSerializer
    permission_classes = [permissions.AllowAny]


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def active_artists_view(request):
    """Artistas ativos"""
    artists = Artist.objects.filter(
        is_active=True
    ).order_by('-created_at')
    
    serializer = ArtistSerializer(artists, many=True)
    
    return Response({
        'artists': serializer.data,
        'count': len(serializer.data)
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def artist_complete_view(request, pk):
    """Artista completo com álbuns e músicas"""
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
    
    return Response({
        'artist': artist_serializer.data,
        'albums': albums_serializer.data,
        'musics': musics_serializer.data,
        'albums_count': albums.count(),
        'musics_count': musics.count()
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def artist_with_albums_view(request, pk):
    """Artista com seus álbuns"""
    try:
        artist = Artist.objects.get(pk=pk, is_active=True)
    except Artist.DoesNotExist:
        return Response(
            {'error': 'Artista não encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Serializar artista
    artist_serializer = ArtistSerializer(artist)
    
    # Buscar álbuns do artista com paginação
    albums = artist.albums.filter(is_active=True).order_by('-featured', '-release_date', '-created_at')
    
    # Paginação manual
    page_size = int(request.query_params.get('page_size', 20))
    page = int(request.query_params.get('page', 1))
    
    start = (page - 1) * page_size
    end = start + page_size
    
    albums_page = albums[start:end]
    albums_serializer = AlbumSerializer(albums_page, many=True)
    
    return Response({
        'artist': artist_serializer.data,
        'albums': albums_serializer.data,
        'count': albums.count(),
        'page': page,
        'page_size': page_size,
        'total_pages': (albums.count() + page_size - 1) // page_size
    })


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
    """Lista de álbuns"""
    queryset = Album.objects.filter(is_active=True)
    serializer_class = AlbumSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        """Filtros de busca"""
        queryset = super().get_queryset()
        
        # Filtro por artista
        artist = self.request.query_params.get('artist')
        if artist:
            queryset = queryset.filter(artist__id=artist)
        
        # Filtro por destaque
        featured = self.request.query_params.get('featured')
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(featured=True)
        
        # Busca por nome do álbum
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        # Ordenação
        ordering = self.request.query_params.get('ordering', '-featured', '-release_date', '-created_at')
        queryset = queryset.order_by(ordering)
        
        return queryset


class AlbumDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhes do álbum"""
    queryset = Album.objects.filter(is_active=True)
    serializer_class = AlbumSerializer
    permission_classes = [permissions.AllowAny]


class AlbumCreateView(generics.CreateAPIView):
    """Criação de álbum"""
    queryset = Album.objects.all()
    serializer_class = AlbumCreateSerializer
    permission_classes = [permissions.AllowAny]


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def featured_albums_view(request):
    """Álbuns em destaque"""
    albums = Album.objects.filter(
        is_active=True,
        featured=True
    ).order_by('-release_date', '-created_at')
    
    serializer = AlbumSerializer(albums, many=True)
    
    return Response({
        'albums': serializer.data,
        'count': len(serializer.data)
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def album_musics_view(request, pk):
    """Músicas do álbum"""
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
    
    return Response({
        'musics': serializer.data,
        'count': musics.count(),
        'page': page,
        'page_size': page_size,
        'total_pages': (musics.count() + page_size - 1) // page_size
    })