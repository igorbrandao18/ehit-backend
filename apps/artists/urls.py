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
    
    # Listas especiais
    path('active/', views.active_artists_view, name='active-artists'),
]
