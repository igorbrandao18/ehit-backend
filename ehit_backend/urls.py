"""
URL configuration for ehit_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .api_views import api_index
from .views import home_view, api_info_view
from .artist_views import (
    artist_dashboard, artist_music_list, artist_music_create,
    artist_music_edit, artist_music_delete, artist_albums, artist_stats
)
from .health_views import health_check

urlpatterns = [
    # Home page
    path('', home_view, name='home'),
    
    # Health check endpoint
    path('health/', health_check, name='health-check'),
    
    # API Info (JSON)
    path('api-info/', api_info_view, name='api-info'),
    
    path('admin/', admin.site.urls),
    
    # API Index
    path('api/', api_index, name='api-index'),
    
    # JWT Authentication
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Artist Admin Area
    path('artist/dashboard/', artist_dashboard, name='artist_dashboard'),
    path('artist/music/', artist_music_list, name='artist_music_list'),
    path('artist/music/create/', artist_music_create, name='artist_music_create'),
    path('artist/music/<int:music_id>/edit/', artist_music_edit, name='artist_music_edit'),
    path('artist/music/<int:music_id>/delete/', artist_music_delete, name='artist_music_delete'),
    path('artist/albums/', artist_albums, name='artist_albums'),
    path('artist/stats/', artist_stats, name='artist_stats'),
    
    # APIs - Simplified (only what's used)
    path('api/artists/', include('apps.artists.urls')),
    path('api/playlists/', include('apps.playlists.urls')),
    # Commented out - not used
    # path('api/users/', include('apps.users.urls')),
    # path('api/music/', include('apps.music.urls')),
    # path('api/genres/', include('apps.genres.urls')),
]

# Servir arquivos de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
