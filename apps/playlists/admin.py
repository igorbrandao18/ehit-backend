from django.contrib import admin
from .models import Playlist


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    """Admin para o modelo PlayHit"""
    
    list_display = ('name', 'get_musics_count', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)
    filter_horizontal = ('musics',)  # Widget horizontal para seleção de músicas
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'is_active')
        }),
        ('Músicas', {
            'fields': ('musics',)
        }),
        ('Visual', {
            'fields': ('cover',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
