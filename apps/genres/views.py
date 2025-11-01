from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q, Count
from .models import Genre
from .serializers import GenreListSerializer
from apps.artists.serializers import AlbumSerializer

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
        """Retorna apenas gêneros que têm artistas, álbuns ou músicas relacionados"""
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
    
    @action(detail=True, methods=['get'])
    def albums(self, request, pk=None):
        """
        Retorna álbuns relacionados ao gênero
        
        URL: /api/genres/<id>/albums/
        """
        genre = self.get_object()
        
        # Buscar álbuns dos artistas deste gênero
        from apps.artists.models import Album
        albums = Album.objects.filter(
            artist__genre=genre,
            is_active=True
        ).annotate(
            musics_count=Count('musics', filter=Q(musics__is_active=True))
        ).filter(musics_count__gt=0).order_by('-featured', '-release_date', '-created_at')
        
        albums_serializer = AlbumSerializer(albums, many=True, context={'request': request})
        
        response_data = {
            'genre': {
                'id': genre.id,
                'name': genre.name,
                'slug': genre.slug,
            },
            'albums': albums_serializer.data,
            'count': albums.count()
        }
        
        return Response(response_data)
