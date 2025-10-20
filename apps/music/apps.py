from django.apps import AppConfig


class MusicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.music'
    verbose_name = 'Músicas'
    
    def ready(self):
        """Importa os signals quando o app estiver pronto"""
        import apps.music.signals