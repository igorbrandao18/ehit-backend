from django.contrib import admin
from .models import Artist


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    """Admin para o modelo Artist"""
    
    list_display = ('stage_name', 'user', 'genre', 'verified', 'followers_count', 'monthly_listeners', 'created_at')
    list_filter = ('verified', 'genre', 'is_active', 'created_at')
    search_fields = ('stage_name', 'real_name', 'user__username', 'user__email')
    ordering = ('-followers_count', '-created_at')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('user', 'stage_name', 'real_name', 'bio', 'photo')
        }),
        ('Detalhes Artísticos', {
            'fields': ('genre', 'location', 'website', 'social_links')
        }),
        ('Status e Estatísticas', {
            'fields': ('verified', 'followers_count', 'monthly_listeners', 'is_active')
        }),
    )
    
    readonly_fields = ('followers_count', 'monthly_listeners', 'created_at', 'updated_at')
