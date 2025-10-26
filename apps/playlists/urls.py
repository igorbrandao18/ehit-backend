from django.urls import path
from . import views

app_name = 'playlists'

urlpatterns = [
    # =============================================================================
    # PLAYLISTS (PlayHits) - Simplified (only what's used)
    # =============================================================================
    
    # Lista de PlayHits
    path('', views.PlaylistListView.as_view(), name='playlist-list'),
    
    # PlayHits em destaque (featured)
    path('featured/', views.featured_playhits_view, name='featured-playhits'),
    
    # Detalhes do PlayHit
    path('<int:pk>/', views.PlaylistDetailView.as_view(), name='playlist-detail'),
]
