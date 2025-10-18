from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json


def home_view(request):
    """Página inicial do Ehit Backend"""
    context = {
        'title': 'Ehit Backend API',
        'description': 'API completa para plataforma de música',
        'version': '1.0.0',
        'endpoints': {
            'api': '/api/',
            'admin': '/admin/',
            'users': '/api/users/',
            'artists': '/api/artists/',
            'music': '/api/music/',
            'playlists': '/api/playlists/',
        },
        'features': [
            'Sistema completo de usuários',
            'Gestão de artistas e músicas',
            'Playlists e favoritos',
            'API RESTful com Django REST Framework',
            'Autenticação e autorização',
            'Testes automatizados (100% cobertura)',
            'Documentação completa',
        ],
    }
    return render(request, 'home.html', context)


def api_info_view(request):
    """Informações da API em JSON"""
    api_info = {
        'name': 'Ehit Backend API',
        'version': '1.0.0',
        'description': 'API completa para plataforma de música',
        'status': 'active',
        'endpoints': {
            'users': {
                'list': '/api/users/',
                'create': '/api/users/create/',
                'login': '/api/users/login/',
                'profile': '/api/users/profile/',
                'stats': '/api/users/stats/',
            },
            'artists': {
                'list': '/api/artists/',
                'create': '/api/artists/create/',
                'detail': '/api/artists/{id}/',
                'popular': '/api/artists/popular/',
                'trending': '/api/artists/trending/',
                'genres': '/api/artists/genres/',
                'musics': '/api/artists/{id}/musics/',
                'stats': '/api/artists/{id}/stats/',
            },
            'music': {
                'list': '/api/music/',
                'create': '/api/music/create/',
                'detail': '/api/music/{id}/',
                'stream': '/api/music/{id}/stream/',
                'download': '/api/music/{id}/download/',
                'like': '/api/music/{id}/like/',
                'trending': '/api/music/trending/',
                'popular': '/api/music/popular/',
                'featured': '/api/music/featured/',
                'genres': '/api/music/genres/',
                'albums': '/api/music/albums/',
                'stats': '/api/music/{id}/stats/',
            },
            'playlists': {
                'list': '/api/playlists/',
                'create': '/api/playlists/create/',
                'detail': '/api/playlists/{id}/',
                'add_music': '/api/playlists/{id}/add-music/',
                'remove_music': '/api/playlists/{id}/remove-music/{music_id}/',
                'reorder': '/api/playlists/{id}/reorder/',
                'follow': '/api/playlists/{id}/follow/',
                'my': '/api/playlists/my/',
                'public': '/api/playlists/public/',
                'popular': '/api/playlists/popular/',
                'favorites': '/api/playlists/favorites/',
            }
        },
        'authentication': {
            'type': 'Token Authentication',
            'header': 'Authorization: Token <your_token>',
        },
        'pagination': {
            'default_page_size': 20,
            'max_page_size': 100,
            'page_param': 'page',
            'page_size_param': 'page_size',
        },
        'filters': {
            'search': '?search=term',
            'ordering': '?ordering=field',
            'filtering': '?field=value',
        },
        'status_codes': {
            '200': 'OK',
            '201': 'Created',
            '400': 'Bad Request',
            '401': 'Unauthorized',
            '403': 'Forbidden',
            '404': 'Not Found',
            '500': 'Internal Server Error',
        }
    }
    return JsonResponse(api_info, json_dumps_params={'indent': 2})
