from django.urls import path
from . import views

app_name = 'artists'

urlpatterns = [
    # =============================================================================
    # ARTIST ENDPOINTS - Simplified (only what's used)
    # =============================================================================
    
    # Lista de artistas
    path('', views.ArtistListView.as_view(), name='artist-list'),
    
    # Detalhes do artista
    path('<int:pk>/', views.ArtistDetailView.as_view(), name='artist-detail'),
    
    # Álbuns do artista (essencial para buscar 100% dos álbuns)
    path('<int:pk>/albums/', views.artist_albums_view, name='artist-albums'),
    
    # Músicas do álbum (para ver músicas de um álbum específico)
    path('albums/<int:pk>/musics/', views.album_musics_view, name='album-musics'),
]
