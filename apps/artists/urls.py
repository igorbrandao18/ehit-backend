from django.urls import path
from . import views

app_name = 'artists'

urlpatterns = [
    # Lista e criação de artistas
    path('', views.ArtistListView.as_view(), name='artist-list'),
    path('create/', views.ArtistCreateView.as_view(), name='artist-create'),
    path('<int:pk>/', views.ArtistDetailView.as_view(), name='artist-detail'),
    
    # Estatísticas e ações
    path('<int:pk>/stats/', views.artist_stats_view, name='artist-stats'),
    path('<int:pk>/follow/', views.follow_artist_view, name='follow-artist'),
    path('<int:pk>/musics/', views.artist_musics_view, name='artist-musics'),
    
    # Listas especiais
    path('popular/', views.popular_artists_view, name='popular-artists'),
    path('trending/', views.trending_artists_view, name='trending-artists'),
    path('genres/', views.genres_view, name='genres'),
]
