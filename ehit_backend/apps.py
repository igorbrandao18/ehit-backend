from django.apps import AppConfig

class EhitBackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ehit_backend'
    
    def ready(self):
        from django.contrib import admin
        admin.site.site_header = "Éhit Administração"
        admin.site.site_title = "Éhit Administração"
        admin.site.index_title = "Painel Administrativo Éhit"
        
        # Importar configurações de admin dos apps
        try:
            from apps.playlists.admin import PlaylistAdmin
            from apps.playlists.models import Playlist
            admin.site.register(Playlist, PlaylistAdmin)
        except ImportError:
            pass