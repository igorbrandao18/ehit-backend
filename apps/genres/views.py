from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db import models
from .models import Genre
from .serializers import GenreSerializer, GenreListSerializer

class GenreViewSet(viewsets.ModelViewSet):
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
