from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.urls import reverse


@require_http_methods(["GET"])
def api_index(request):
    """Página inicial da API com todos os endpoints disponíveis"""
    
    base_url = request.build_absolute_uri('/api/')
    
    endpoints = {
        "message": "🎵 Ehit Backend API",
        "version": "1.0.0",
        "description": "API REST completa para plataforma de música",
        "base_url": base_url,
        "endpoints": {
            "users": {
                "url": f"{base_url}users/",
                "description": "Gestão de usuários",
                "methods": ["GET", "POST"],
                "endpoints": {
                    "list": f"{base_url}users/",
                    "create": f"{base_url}users/create/",
                    "login": f"{base_url}users/login/",
                    "profile": f"{base_url}users/profile/",
                    "stats": f"{base_url}users/stats/"
                }
            },
            "artists": {
                "url": f"{base_url}artists/",
                "description": "Gestão de artistas",
                "methods": ["GET", "POST"],
                "endpoints": {
                    "list": f"{base_url}artists/",
                    "create": f"{base_url}artists/create/",
                    "popular": f"{base_url}artists/popular/",
                    "trending": f"{base_url}artists/trending/",
                    "genres": f"{base_url}artists/genres/"
                }
            },
            "music": {
                "url": f"{base_url}music/",
                "description": "Gestão de músicas",
                "methods": ["GET", "POST"],
                "endpoints": {
                    "list": f"{base_url}music/",
                    "create": f"{base_url}music/create/",
                    "trending": f"{base_url}music/trending/",
                    "popular": f"{base_url}music/popular/",
                    "featured": f"{base_url}music/featured/",
                    "genres": f"{base_url}music/genres/",
                    "albums": f"{base_url}music/albums/"
                }
            },
            "playlists": {
                "url": f"{base_url}playlists/",
                "description": "Gestão de playlists e favoritos",
                "methods": ["GET", "POST"],
                "endpoints": {
                    "list": f"{base_url}playlists/",
                    "create": f"{base_url}playlists/create/",
                    "my": f"{base_url}playlists/my/",
                    "public": f"{base_url}playlists/public/",
                    "popular": f"{base_url}playlists/popular/",
                    "favorites": f"{base_url}playlists/favorites/"
                }
            }
        },
        "authentication": {
            "required": "Para endpoints protegidos, use:",
            "header": "Authorization: Token <seu_token>",
            "login_endpoint": f"{base_url}users/login/"
        },
        "pagination": {
            "description": "Todos os endpoints de lista suportam paginação",
            "parameters": {
                "page": "Número da página (padrão: 1)",
                "page_size": "Itens por página (padrão: 20, máximo: 100)"
            },
            "example": f"{base_url}music/?page=2&page_size=10"
        },
        "filters": {
            "description": "Filtros disponíveis por endpoint",
            "common": ["search", "ordering", "page_size"],
            "music": ["artist", "genre", "album", "featured"],
            "artists": ["genre", "verified", "location"],
            "playlists": ["user", "is_public"]
        },
        "examples": {
            "list_music": f"{base_url}music/",
            "search_music": f"{base_url}music/?search=forró",
            "trending_music": f"{base_url}music/trending/",
            "artist_musics": f"{base_url}artists/1/musics/",
            "login": f"{base_url}users/login/"
        },
        "documentation": {
            "api_docs": "Veja API.md para documentação completa",
            "tests": "Execute 'python manage.py test' para ver os 60 testes",
            "admin": "http://127.0.0.1:8000/admin/ (admin / 81927d75)"
        }
    }
    
    return JsonResponse(endpoints, json_dumps_params={'indent': 2})
