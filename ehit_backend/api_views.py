from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.shortcuts import render
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


@api_view(['GET'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([AllowAny])
def api_index(request):
    """API Index - Simplified endpoints only"""
    
    base_url = request.build_absolute_uri('/api/')
    
    endpoints = {
        "message": "🎵 Ehit Backend API",
        "version": "1.0.0",
        "description": "API simplificada - apenas endpoints essenciais",
        "base_url": base_url,
        "endpoints": {
            "artists": {
                "url": f"{base_url}artists/",
                "description": "Gestão de artistas",
                "methods": ["GET"],
                "endpoints": {
                    "list": f"{base_url}artists/",
                    "detail": f"{base_url}artists/<id>/",
                    "albums": f"{base_url}artists/<id>/albums/"
                }
            },
            "playlists": {
                "url": f"{base_url}playlists/",
                "description": "PlayHits (Playlists)",
                "methods": ["GET"],
                "endpoints": {
                    "list": f"{base_url}playlists/",
                    "detail": f"{base_url}playlists/<id>/",
                    "featured_filter": f"{base_url}playlists/?featured=true"
                }
            },
            "banners": {
                "url": f"{base_url}banners/",
                "description": "Banners publicitários",
                "methods": ["GET"],
                "endpoints": {
                    "list": f"{base_url}banners/",
                    "detail": f"{base_url}banners/<id>/",
                    "all_banners": f"{base_url}banners/all/",
                    "active_banners": f"{base_url}banners/active/"
                }
            }
        },
        "query_parameters": {
            "artists": {
                "search": "Buscar por nome do artista",
                "ordering": "Ordenação (default: -created_at)",
                "page_size": "Itens por página (default: 20)"
            },
            "playlists": {
                "featured": "true para mostrar apenas em destaque",
                "search": "Buscar por nome da playlist",
                "ordering": "Ordenação (default: -created_at)",
                "page_size": "Itens por página (default: 20)"
            },
            "banners": {
                "ordering": "Ordenação (default: -start_date)",
                "page_size": "Itens por página (default: 20)"
            }
        },
        "examples": {
            "all_artists": f"{base_url}artists/",
            "artist_detail": f"{base_url}artists/5/",
            "artist_albums": f"{base_url}artists/5/albums/",
            "all_playlists": f"{base_url}playlists/",
            "featured_playlists": f"{base_url}playlists/?featured=true",
            "playlist_detail": f"{base_url}playlists/1/",
            "active_banners": f"{base_url}banners/",
            "all_banners": f"{base_url}banners/all/",
            "banner_detail": f"{base_url}banners/1/"
        }
    }
    
    return Response(endpoints)
