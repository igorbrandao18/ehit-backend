from django.urls import path
from . import views

app_name = 'artists'

urlpatterns = [
    # Lista e criação de artistas
    path('', views.ArtistListView.as_view(), name='artist-list'),
    path('create/', views.ArtistCreateView.as_view(), name='artist-create'),
    path('<int:pk>/', views.ArtistDetailView.as_view(), name='artist-detail'),
    
    # Ações
    path('<int:pk>/musics/', views.artist_musics_view, name='artist-musics'),
    path('<int:pk>/albums/', views.artist_albums_view, name='artist-albums'),
    
    # Listas especiais
    path('active/', views.active_artists_view, name='active-artists'),
    
    # =============================================================================
    # ALBUM ROUTES
    # =============================================================================
    
    # Lista e criação de álbuns
    path('albums/', views.AlbumListView.as_view(), name='album-list'),
    path('albums/create/', views.AlbumCreateView.as_view(), name='album-create'),
    path('albums/<int:pk>/', views.AlbumDetailView.as_view(), name='album-detail'),
    
    # Ações com álbuns
    path('albums/<int:pk>/musics/', views.album_musics_view, name='album-musics'),
    
    # Listas especiais de álbuns
    path('albums/featured/', views.featured_albums_view, name='featured-albums'),
]
