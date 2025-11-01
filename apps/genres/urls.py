from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GenreViewSet, genre_artists_view

router = DefaultRouter()
router.register(r'genres', GenreViewSet, basename='genre')

urlpatterns = [
    path('', include(router.urls)),
    # Artistas do gênero
    path('genres/<int:pk>/artists/', genre_artists_view, name='genre-artists'),
]
