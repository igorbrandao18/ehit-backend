from django.contrib import admin
from .models import Music


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    """Admin para o modelo Music"""
    
    list_display = ('title', 'artist', 'genre', 'duration', 'streams_count', 'downloads_count', 'likes_count', 'is_featured', 'created_at')
    list_filter = ('genre', 'is_featured', 'is_active', 'created_at', 'release_date')
    search_fields = ('title', 'album', 'artist__stage_name', 'artist__user__username')
    ordering = ('-streams_count', '-created_at')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('artist', 'title', 'album', 'genre', 'duration')
        }),
        ('Arquivos', {
            'fields': ('file', 'cover', 'lyrics')
        }),
        ('Lançamento', {
            'fields': ('release_date', 'is_featured')
        }),
        ('Estatísticas', {
            'fields': ('streams_count', 'downloads_count', 'likes_count')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    readonly_fields = ('streams_count', 'downloads_count', 'likes_count', 'created_at', 'updated_at')
    
    def get_duration_formatted(self, obj):
        """Retorna duração formatada"""
        return obj.get_duration_formatted()
    get_duration_formatted.short_description = 'Duração'
