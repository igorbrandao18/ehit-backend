from django.contrib import admin
from .models import Playlist, UserFavorite


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    """Admin para o modelo Playlist"""
    
    list_display = ('name', 'user', 'is_public', 'followers_count', 'get_musics_count', 'created_at')
    list_filter = ('is_public', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'user__username')
    ordering = ('-followers_count', '-created_at')
    filter_horizontal = ('musics',)  # Widget horizontal para seleção de músicas
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('user', 'name', 'description', 'is_public')
        }),
        ('Músicas', {
            'fields': ('musics',)
        }),
        ('Visual', {
            'fields': ('cover',)
        }),
        ('Estatísticas', {
            'fields': ('followers_count',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    readonly_fields = ('followers_count', 'created_at', 'updated_at')


@admin.register(UserFavorite)
class UserFavoriteAdmin(admin.ModelAdmin):
    """Admin para o modelo UserFavorite"""
    
    list_display = ('user', 'music', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('user__username', 'music__title')
    ordering = ('-added_at',)
