from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GenreViewSet, genre_artists_view

router = DefaultRouter()
router.register(r'genres', GenreViewSet, basename='genre')

urlpatterns = [
    # Artistas do gênero (deve vir ANTES do router para evitar conflito)
    path('<int:pk>/artists/', genre_artists_view, name='genre-artists'),
    path('', include(router.urls)),
]
