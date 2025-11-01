from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import NotFound
from django.db.models import Q, Count
from .models import Genre
from .serializers import GenreListSerializer
from apps.artists.serializers import ArtistSerializer

class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet somente leitura - apenas GET permitido"""
    queryset = Genre.objects.all()  # Base queryset necessário para o router
    serializer_class = GenreListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        """Retorna apenas gêneros que têm artistas ou músicas relacionados"""
        queryset = Genre.objects.filter(is_active=True).annotate(
            artists_count=Count('artists', filter=Q(artists__is_active=True), distinct=True),
            musics_count=Count('musics', filter=Q(musics__is_active=True), distinct=True)
        ).filter(
            Q(artists_count__gt=0) | Q(musics_count__gt=0)
        )
        return queryset
    
    def get_serializer_context(self):
        """Adiciona request ao contexto para URLs absolutas"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def genre_artists_view(request, pk):
    """
    Retorna todos os artistas relacionados ao gênero
    
    URL: /api/genres/<id>/artists/
    """
    try:
        genre = Genre.objects.get(pk=pk, is_active=True)
    except Genre.DoesNotExist:
        return Response(
            {'error': 'Gênero não encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Buscar artistas do gênero que tenham álbuns ativos
    artists = genre.artists.filter(
        is_active=True
    ).annotate(
        albums_count=Count('albums', filter=Q(albums__is_active=True))
    ).filter(albums_count__gt=0).order_by('-created_at')
    
    artists_serializer = ArtistSerializer(artists, many=True, context={'request': request})
    
    response_data = {
        'genre': {
            'id': genre.id,
            'name': genre.name,
            'slug': genre.slug,
        },
        'artists': artists_serializer.data,
        'count': artists.count()
    }
    
    return Response(response_data)
