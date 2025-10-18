from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    # Lista e criação de músicas
    path('', views.MusicListView.as_view(), name='music-list'),
    path('create/', views.MusicCreateView.as_view(), name='music-create'),
    path('<int:pk>/', views.MusicDetailView.as_view(), name='music-detail'),
    
    # Ações com músicas
    path('<int:pk>/stream/', views.stream_music_view, name='stream-music'),
    path('<int:pk>/download/', views.download_music_view, name='download-music'),
    path('<int:pk>/like/', views.like_music_view, name='like-music'),
    path('<int:pk>/stats/', views.music_stats_view, name='music-stats'),
    
    # Listas especiais
    path('trending/', views.trending_music_view, name='trending-music'),
    path('popular/', views.popular_music_view, name='popular-music'),
    path('featured/', views.featured_music_view, name='featured-music'),
    path('genres/', views.genres_view, name='genres'),
    path('albums/', views.albums_view, name='albums'),
]
