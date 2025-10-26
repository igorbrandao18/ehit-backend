from django.urls import path
from . import views

app_name = 'artists'

urlpatterns = [
    # =============================================================================
    # ARTIST ENDPOINTS
    # =============================================================================
    
    # Lista e criação de artistas
    path('', views.ArtistListView.as_view(), name='artist-list'),
    path('create/', views.ArtistCreateView.as_view(), name='artist-create'),
    path('<int:pk>/', views.ArtistDetailView.as_view(), name='artist-detail'),
    
    # Busca completa de artista (com álbuns e músicas)
    path('<int:pk>/complete/', views.artist_complete_view, name='artist-complete'),
    path('<int:pk>/albums/', views.artist_albums_view, name='artist-albums'),
    path('<int:pk>/with-musics/', views.artist_with_musics_view, name='artist-with-musics'),
    
    # Listas especiais
    path('active/', views.active_artists_view, name='active-artists'),
    
    # =============================================================================
    # ALBUM ENDPOINTS
    # =============================================================================
    
    # Lista e criação de álbuns (com filtros avançados)
    path('albums/', views.AlbumListView.as_view(), name='album-list'),
    path('albums/create/', views.AlbumCreateView.as_view(), name='album-create'),
    path('albums/<int:pk>/', views.AlbumDetailView.as_view(), name='album-detail'),
    
    # Músicas do álbum
    path('albums/<int:pk>/musics/', views.album_musics_view, name='album-musics'),
    
    # Listas especiais de álbuns
    path('albums/featured/', views.featured_albums_view, name='featured-albums'),
]
