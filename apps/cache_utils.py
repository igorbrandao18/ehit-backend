"""
Utilitários de cache Redis para invalidação automática
"""
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .artists.models import Artist, Album
from .music.models import Music
from .playlists.models import Playlist


def invalidate_artist_cache(artist_id=None):
    """Invalidar cache relacionado a artistas"""
    if artist_id:
        # Cache específico do artista
        cache.delete(f"artist_complete_{artist_id}")
        cache.delete(f"artist_with_musics_{artist_id}")
    
    # Cache geral de artistas
    cache.delete_many([
        "active_artists",
        "artists_list_",
        "featured_albums",
        "albums_list_",
    ])


def invalidate_album_cache(album_id=None, artist_id=None):
    """Invalidar cache relacionado a álbuns"""
    if album_id:
        cache.delete(f"album_musics_{album_id}")
    
    if artist_id:
        invalidate_artist_cache(artist_id)
    
    # Cache geral de álbuns
    cache.delete_many([
        "featured_albums",
        "albums_list_",
    ])


def invalidate_music_cache(music_id=None, artist_id=None, album_id=None):
    """Invalidar cache relacionado a músicas"""
    if music_id:
        cache.delete(f"music_stats_{music_id}")
    
    if artist_id:
        invalidate_artist_cache(artist_id)
    
    if album_id:
        invalidate_album_cache(album_id)
    
    # Cache geral de músicas
    cache.delete_many([
        "trending_music",
        "popular_music",
        "featured_music",
        "musics_list_",
        "music_autocomplete_",
    ])


def invalidate_playlist_cache(playlist_id=None):
    """Invalidar cache relacionado a playlists"""
    if playlist_id:
        cache.delete(f"playlist_detail_{playlist_id}")
    
    # Cache geral de playlists
    cache.delete_many([
        "active_playhits",
        "playlists_list_",
    ])


# =============================================================================
# SIGNALS PARA INVALIDAÇÃO AUTOMÁTICA DE CACHE
# =============================================================================

@receiver(post_save, sender=Artist)
def artist_saved(sender, instance, **kwargs):
    """Invalidar cache quando artista é salvo"""
    invalidate_artist_cache(instance.id)


@receiver(post_delete, sender=Artist)
def artist_deleted(sender, instance, **kwargs):
    """Invalidar cache quando artista é deletado"""
    invalidate_artist_cache(instance.id)


@receiver(post_save, sender=Album)
def album_saved(sender, instance, **kwargs):
    """Invalidar cache quando álbum é salvo"""
    invalidate_album_cache(instance.id, instance.artist.id)


@receiver(post_delete, sender=Album)
def album_deleted(sender, instance, **kwargs):
    """Invalidar cache quando álbum é deletado"""
    invalidate_album_cache(instance.id, instance.artist.id)


@receiver(post_save, sender=Music)
def music_saved(sender, instance, **kwargs):
    """Invalidar cache quando música é salva"""
    invalidate_music_cache(
        instance.id, 
        instance.artist.id if instance.artist else None,
        instance.album.id if instance.album else None
    )


@receiver(post_delete, sender=Music)
def music_deleted(sender, instance, **kwargs):
    """Invalidar cache quando música é deletada"""
    invalidate_music_cache(
        instance.id, 
        instance.artist.id if instance.artist else None,
        instance.album.id if instance.album else None
    )


@receiver(post_save, sender=Playlist)
def playlist_saved(sender, instance, **kwargs):
    """Invalidar cache quando playlist é salva"""
    invalidate_playlist_cache(instance.id)


@receiver(post_delete, sender=Playlist)
def playlist_deleted(sender, instance, **kwargs):
    """Invalidar cache quando playlist é deletada"""
    invalidate_playlist_cache(instance.id)


# =============================================================================
# COMANDOS DE CACHE MANAGEMENT
# =============================================================================

def clear_all_cache():
    """Limpar todo o cache"""
    cache.clear()


def warm_up_cache():
    """Aquecer cache com dados frequentes"""
    from .artists.views import active_artists_view, featured_albums_view
    from .music.views import trending_music_view, popular_music_view, featured_music_view
    from .playlists.views import active_playhits_view
    
    # Simular requests para popular cache
    from django.test import RequestFactory
    factory = RequestFactory()
    
    try:
        # Aquecer cache de artistas
        request = factory.get('/api/artists/active/')
        active_artists_view(request)
        
        # Aquecer cache de álbuns
        request = factory.get('/api/artists/albums/featured/')
        featured_albums_view(request)
        
        # Aquecer cache de músicas
        request = factory.get('/api/music/trending/')
        trending_music_view(request)
        
        request = factory.get('/api/music/popular/')
        popular_music_view(request)
        
        request = factory.get('/api/music/featured/')
        featured_music_view(request)
        
        # Aquecer cache de playlists
        request = factory.get('/api/playlists/active/')
        active_playhits_view(request)
        
        print("✅ Cache aquecido com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao aquecer cache: {e}")


def get_cache_stats():
    """Obter estatísticas do cache"""
    try:
        # Informações básicas do cache
        info = {
            'cache_backend': 'django_redis.cache.RedisCache',
            'status': 'Ativo',
        }
        
        # Teste básico de conectividade
        test_key = 'cache_test_key'
        test_value = 'test'
        
        cache.set(test_key, test_value, 10)
        cached_value = cache.get(test_key)
        
        if cached_value == test_value:
            info['connectivity'] = 'OK'
        else:
            info['connectivity'] = 'FALHOU'
        
        cache.delete(test_key)
        
        return info
        
    except Exception as e:
        return {'error': str(e), 'status': 'Inativo'}
