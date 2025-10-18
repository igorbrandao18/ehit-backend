from django.urls import path
from . import views

app_name = 'playlists'

urlpatterns = [
    # Lista e criação de playlists
    path('', views.PlaylistListView.as_view(), name='playlist-list'),
    path('create/', views.PlaylistCreateView.as_view(), name='playlist-create'),
    path('<int:pk>/', views.PlaylistDetailView.as_view(), name='playlist-detail'),
    path('my/', views.UserPlaylistsView.as_view(), name='my-playlists'),
    
    # Ações com playlists
    path('<int:pk>/add-music/', views.add_music_to_playlist_view, name='add-music'),
    path('<int:pk>/remove-music/<int:music_id>/', views.remove_music_from_playlist_view, name='remove-music'),
    path('<int:pk>/reorder/', views.reorder_playlist_musics_view, name='reorder-musics'),
    path('<int:pk>/follow/', views.follow_playlist_view, name='follow-playlist'),
    
    # Favoritos
    path('favorites/', views.UserFavoritesView.as_view(), name='favorites'),
    path('favorites/<int:pk>/', views.remove_favorite_view, name='remove-favorite'),
    
    # Listas especiais
    path('public/', views.public_playlists_view, name='public-playlists'),
    path('popular/', views.popular_playlists_view, name='popular-playlists'),
]
