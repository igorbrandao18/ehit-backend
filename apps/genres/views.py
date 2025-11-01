from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db import models
from django.db.models import Q, Count
from .models import Genre
from .serializers import GenreSerializer, GenreListSerializer
from apps.artists.serializers import ArtistSerializer, AlbumSerializer
from apps.music.serializers import MusicSerializer

class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet somente leitura - apenas GET permitido"""
    queryset = Genre.objects.filter(is_active=True)
    serializer_class = GenreSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['parent', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'song_count', 'artist_count']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return GenreListSerializer
        return GenreSerializer
    
    def get_serializer_context(self):
        """Adiciona request ao contexto para URLs absolutas"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    @action(detail=False, methods=['get'])
    def main_genres(self, request):
        """Retorna apenas os gêneros principais (sem parent)"""
        main_genres = self.queryset.filter(parent__isnull=True)
        serializer = self.get_serializer(main_genres, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def subgenres(self, request, pk=None):
        """Retorna os subgêneros de um gênero específico"""
        genre = self.get_object()
        subgenres = genre.subgenres.filter(is_active=True)
        serializer = self.get_serializer(subgenres, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def with_counts(self, request):
        """Retorna gêneros com contadores de músicas e artistas"""
        genres = self.queryset.annotate(
            total_songs=models.Count('musics', distinct=True),
            total_artists=models.Count('artists', distinct=True)
        )
        serializer = self.get_serializer(genres, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def complete(self, request, pk=None):
        """
        Retorna gênero completo com artistas, álbuns e músicas
        
        URL: /api/genres/<id>/complete/
        """
        genre = self.get_object()
        
        # Serializar gênero
        genre_serializer = GenreSerializer(genre, context={'request': request})
        
        # Buscar artistas do gênero que tenham álbuns ativos
        artists = genre.artists.filter(
            is_active=True
        ).annotate(
            albums_count=Count('albums', filter=Q(albums__is_active=True))
        ).filter(albums_count__gt=0)
        
        artists_serializer = ArtistSerializer(artists, many=True, context={'request': request})
        
        # Buscar álbuns dos artistas deste gênero
        from apps.artists.models import Album
        albums = Album.objects.filter(
            artist__genre=genre,
            is_active=True
        ).annotate(
            musics_count=Count('musics', filter=Q(musics__is_active=True))
        ).filter(musics_count__gt=0).order_by('-featured', '-release_date', '-created_at')
        
        albums_serializer = AlbumSerializer(albums, many=True, context={'request': request})
        
        # Buscar músicas do gênero
        musics = genre.musics.filter(is_active=True).order_by('-streams_count', '-created_at')
        musics_serializer = MusicSerializer(musics, many=True, context={'request': request})
        
        response_data = {
            'genre': genre_serializer.data,
            'artists': artists_serializer.data,
            'albums': albums_serializer.data,
            'musics': musics_serializer.data,
            'artists_count': artists.count(),
            'albums_count': albums.count(),
            'musics_count': musics.count()
        }
        
        return Response(response_data)
