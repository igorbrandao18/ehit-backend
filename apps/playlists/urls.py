from django.urls import path
from . import views

app_name = 'playlists'

urlpatterns = [
    # =============================================================================
    # PLAYLISTS (PlayHits) - Simplified (only what's used)
    # =============================================================================
    
    # Lista de PlayHits (usa ?featured=true para filtro)
    path('', views.PlaylistListView.as_view(), name='playlist-list'),
    
    # Detalhes do PlayHit
    path('<int:pk>/', views.PlaylistDetailView.as_view(), name='playlist-detail'),
]
