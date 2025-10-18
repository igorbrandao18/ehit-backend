from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Playlist, PlaylistMusic, UserFavorite
from .serializers import (
    PlaylistSerializer, PlaylistCreateSerializer, PlaylistDetailSerializer,
    PlaylistMusicSerializer, UserFavoriteSerializer, UserFavoriteCreateSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    """Paginação padrão"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class PlaylistListView(generics.ListAPIView):
    """Lista de playlists"""
    queryset = Playlist.objects.filter(is_active=True)
    serializer_class = PlaylistSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        """Filtros de busca"""
        queryset = super().get_queryset()
        
        # Filtro por usuário
        user_id = self.request.query_params.get('user')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        # Filtro por visibilidade
        is_public = self.request.query_params.get('is_public')
        if is_public is not None:
            queryset = queryset.filter(is_public=is_public.lower() == 'true')
        
        # Busca por nome/descrição
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )
        
        # Ordenação
        ordering = self.request.query_params.get('ordering', '-followers_count')
        queryset = queryset.order_by(ordering)
        
        return queryset


class PlaylistDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalhes da playlist"""
    queryset = Playlist.objects.filter(is_active=True)
    serializer_class = PlaylistDetailSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_permissions(self):
        """Permissões baseadas na ação"""
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
    def get_serializer_class(self):
        """Serializer baseado na ação"""
        if self.request.method == 'GET':
            return PlaylistDetailSerializer
        return PlaylistSerializer


class PlaylistCreateView(generics.CreateAPIView):
    """Criação de playlist"""
    queryset = Playlist.objects.all()
    serializer_class = PlaylistCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        """Define o usuário como o usuário logado"""
        serializer.save(user=self.request.user)


class UserPlaylistsView(generics.ListAPIView):
    """Playlists do usuário logado"""
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Playlists do usuário logado"""
        return Playlist.objects.filter(
            user=self.request.user,
            is_active=True
        ).order_by('-created_at')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_music_to_playlist_view(request, pk):
    """Adicionar música à playlist"""
    try:
        playlist = Playlist.objects.get(pk=pk, user=request.user, is_active=True)
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
    if PlaylistMusic.objects.filter(playlist=playlist, music=music).exists():
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


class UserFavoritesView(generics.ListCreateAPIView):
    """Favoritos do usuário"""
    serializer_class = UserFavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Favoritos do usuário logado"""
        return UserFavorite.objects.filter(
            user=self.request.user
        ).order_by('-added_at')
    
    def get_serializer_class(self):
        """Serializer baseado na ação"""
        if self.request.method == 'POST':
            return UserFavoriteCreateSerializer
        return UserFavoriteSerializer
    
    def perform_create(self, serializer):
        """Define o usuário como o usuário logado"""
        serializer.save(user=self.request.user)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def remove_favorite_view(request, pk):
    """Remover música dos favoritos"""
    try:
        favorite = UserFavorite.objects.get(pk=pk, user=request.user)
    except UserFavorite.DoesNotExist:
        return Response(
            {'error': 'Favorito não encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    favorite.delete()
    
    return Response({'message': 'Música removida dos favoritos'})


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def public_playlists_view(request):
    """Playlists públicas"""
    playlists = Playlist.objects.filter(
        is_active=True,
        is_public=True
    ).order_by('-followers_count')
    
    serializer = PlaylistSerializer(playlists, many=True)
    
    return Response({
        'playlists': serializer.data,
        'count': len(serializer.data)
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def popular_playlists_view(request):
    """Playlists populares"""
    playlists = Playlist.objects.filter(
        is_active=True,
        is_public=True,
        followers_count__gte=10
    ).order_by('-followers_count')[:20]
    
    serializer = PlaylistSerializer(playlists, many=True)
    
    return Response({
        'playlists': serializer.data,
        'count': len(serializer.data)
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_playlist_view(request, pk):
    """Seguir/deixar de seguir playlist"""
    try:
        playlist = Playlist.objects.get(pk=pk, is_active=True)
    except Playlist.DoesNotExist:
        return Response(
            {'error': 'Playlist não encontrada'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Verificar se não é a própria playlist
    if playlist.user == request.user:
        return Response(
            {'error': 'Você não pode seguir sua própria playlist'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    action = request.data.get('action', 'follow')
    
    if action == 'follow':
        playlist.followers_count += 1
        playlist.save()
        message = f'Agora você está seguindo a playlist {playlist.name}'
    elif action == 'unfollow':
        if playlist.followers_count > 0:
            playlist.followers_count -= 1
            playlist.save()
        message = f'Você parou de seguir a playlist {playlist.name}'
    else:
        return Response(
            {'error': 'Ação inválida. Use "follow" ou "unfollow"'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    return Response({
        'message': message,
        'followers_count': playlist.followers_count
    })