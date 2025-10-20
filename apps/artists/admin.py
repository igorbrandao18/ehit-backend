from django.contrib import admin
from .models import Artist


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    """Admin para o modelo Artist simplificado"""
    
    list_display = ('stage_name', 'genre', 'is_active', 'created_at')
    list_filter = ('genre', 'is_active', 'created_at')
    search_fields = ('stage_name',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('stage_name', 'photo', 'is_active')
        }),
        ('Gênero Musical', {
            'fields': ('genre',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
