from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db import models
from .models import Playlist
from .serializers import (
    PlaylistSerializer, PlaylistCreateSerializer, PlaylistDetailSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    """Paginação padrão"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class PlaylistListView(generics.ListAPIView):
    """Lista de playlists com cache Redis"""
    queryset = Playlist.objects.filter(is_active=True).annotate(
        musics_count=models.Count('musics')
    ).filter(musics_count__gt=0)
    serializer_class = PlaylistSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        """Filtros de busca com cache"""
        queryset = super().get_queryset()
        
        # Filtro por visibilidade (apenas ativas)
        queryset = queryset.filter(is_active=True)
        
        # Apenas playlists com músicas
        queryset = queryset.annotate(
            musics_count=models.Count('musics')
        ).filter(musics_count__gt=0)
        
        # Busca por nome
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        # Filtro por destaque
        featured = self.request.query_params.get('featured')
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)
        
        # Ordenação
        ordering = self.request.query_params.get('ordering', 'order')
        queryset = queryset.order_by(ordering)
        
        return queryset


class PlaylistDetailView(generics.RetrieveAPIView):
    """Detalhes da PlayHit - apenas GET permitido"""
    queryset = Playlist.objects.filter(is_active=True)
    serializer_class = PlaylistDetailSerializer
    permission_classes = [permissions.AllowAny]


class PlaylistCreateView(generics.CreateAPIView):
    """Criação de PlayHit"""
    queryset = Playlist.objects.all()
    serializer_class = PlaylistCreateSerializer
    permission_classes = [permissions.AllowAny]




@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def add_music_to_playlist_view(request, pk):
    """Adicionar música à playlist"""
    try:
        playlist = Playlist.objects.get(pk=pk, is_active=True)
    except Playlist.DoesNotExist:
        return Response(
            {'error': 'Playlist não encontrada'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    music_id = request.data.get('music_id')
    if not music_id:
        return Response(
            {'error': 'music_id é obrigatório'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        from apps.music.models import Music
        music = Music.objects.get(pk=music_id, is_active=True)
    except Music.DoesNotExist:
        return Response(
            {'error': 'Música não encontrada'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Verificar se música já está na playlist
    if playlist.musics.filter(pk=music.pk).exists():
        return Response(
            {'error': 'Música já está na playlist'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Adicionar música
    playlist.add_music(music)
    
    return Response({
        'message': 'Música adicionada à playlist',
        'musics_count': playlist.get_musics_count()
    })


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def remove_music_from_playlist_view(request, pk, music_id):
    """Remover música da playlist"""
    try:
        playlist = Playlist.objects.get(pk=pk, user=request.user, is_active=True)
    except Playlist.DoesNotExist:
        return Response(
            {'error': 'Playlist não encontrada'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    try:
        from apps.music.models import Music
        music = Music.objects.get(pk=music_id, is_active=True)
    except Music.DoesNotExist:
        return Response(
            {'error': 'Música não encontrada'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Remover música
    playlist.remove_music(music)
    
    return Response({
        'message': 'Música removida da playlist',
        'musics_count': playlist.get_musics_count()
    })


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def reorder_playlist_musics_view(request, pk):
    """Reordenar músicas da playlist"""
    try:
        playlist = Playlist.objects.get(pk=pk, user=request.user, is_active=True)
    except Playlist.DoesNotExist:
        return Response(
            {'error': 'Playlist não encontrada'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    music_orders = request.data.get('music_orders')
    if not music_orders:
        return Response(
            {'error': 'music_orders é obrigatório'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Reordenar músicas
    playlist.reorder_musics(music_orders)
    
    return Response({'message': 'Músicas reordenadas com sucesso'})




@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def active_playhits_view(request):
    """PlayHits ativas"""
    playhits = Playlist.objects.filter(
        is_active=True
    ).annotate(
        musics_count=models.Count('musics')
    ).filter(musics_count__gt=0).order_by('order', '-is_featured', '-created_at')
    
    serializer = PlaylistSerializer(playhits, many=True)
    
    response_data = {
        'playhits': serializer.data,
        'count': len(serializer.data)
    }
    
    return Response(response_data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def featured_playhits_view(request):
    """PlayHits em destaque"""
    featured_playhits = Playlist.objects.filter(
        is_active=True,
        is_featured=True
    ).annotate(
        musics_count=models.Count('musics')
    ).filter(musics_count__gt=0).order_by('order', '-created_at')
    
    serializer = PlaylistSerializer(featured_playhits, many=True)
    
    response_data = {
        'featured_playhits': serializer.data,
        'count': len(serializer.data)
    }
    
    return Response(response_data)