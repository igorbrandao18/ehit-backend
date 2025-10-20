from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Artist
from .serializers import ArtistSerializer, ArtistCreateSerializer


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
def artist_musics_view(request, pk):
    """Músicas do artista"""
    try:
        artist = Artist.objects.get(pk=pk, is_active=True)
    except Artist.DoesNotExist:
        return Response(
            {'error': 'Artista não encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    musics = artist.musics.filter(is_active=True).order_by('-created_at')
    
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