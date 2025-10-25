from django.urls import path
from . import views

app_name = 'playlists'

urlpatterns = [
    # Lista e criação de PlayHits
    path('', views.PlaylistListView.as_view(), name='playlist-list'),
    path('create/', views.PlaylistCreateView.as_view(), name='playlist-create'),
    path('<int:pk>/', views.PlaylistDetailView.as_view(), name='playlist-detail'),
    
    # Ações com PlayHits
    path('<int:pk>/add-music/', views.add_music_to_playlist_view, name='add-music'),
    path('<int:pk>/remove-music/<int:music_id>/', views.remove_music_from_playlist_view, name='remove-music'),
    path('<int:pk>/reorder/', views.reorder_playlist_musics_view, name='reorder-musics'),
    
    # Listas especiais
    path('active/', views.active_playhits_view, name='active-playhits'),
    path('featured/', views.featured_playhits_view, name='featured-playhits'),
]
