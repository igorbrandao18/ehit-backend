from django.contrib import admin
from .models import Playlist, PlaylistMusic, UserFavorite


class PlaylistMusicInline(admin.TabularInline):
    """Inline para músicas da playlist"""
    model = PlaylistMusic
    extra = 1
    ordering = ('order',)


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    """Admin para o modelo Playlist"""
    
    list_display = ('name', 'user', 'is_public', 'followers_count', 'get_musics_count', 'created_at')
    list_filter = ('is_public', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'user__username')
    ordering = ('-followers_count', '-created_at')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('user', 'name', 'description', 'is_public')
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
    inlines = [PlaylistMusicInline]


@admin.register(PlaylistMusic)
class PlaylistMusicAdmin(admin.ModelAdmin):
    """Admin para o modelo PlaylistMusic"""
    
    list_display = ('playlist', 'music', 'order', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('playlist__name', 'music__title')
    ordering = ('playlist', 'order')


@admin.register(UserFavorite)
class UserFavoriteAdmin(admin.ModelAdmin):
    """Admin para o modelo UserFavorite"""
    
    list_display = ('user', 'music', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('user__username', 'music__title')
    ordering = ('-added_at',)
