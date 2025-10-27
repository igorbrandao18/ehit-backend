from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Playlist


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    """Admin para o modelo Playlist"""
    
    list_display = [
        'id', 'name', 'musics_count', 'is_active', 'is_featured', 
        'created_at', 'updated_at'
    ]
    
    list_filter = [
        'is_active', 'is_featured', 'created_at', 'updated_at'
    ]
    
    search_fields = [
        'name'
    ]
    
    readonly_fields = [
        'id', 'created_at', 'updated_at', 'musics_count', 'add_music_link'
    ]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('id', 'name', 'cover')
        }),
        ('Configurações', {
            'fields': ('is_active', 'is_featured')
        }),
        ('Músicas', {
            'fields': ('add_music_link', 'musics', 'musics_count'),
            'description': '💡 Dica: Use o botão "Adicionar Música" acima para criar novas músicas. Ou selecione músicas existentes no campo abaixo.'
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    filter_horizontal = ['musics']
    
    def musics_count(self, obj):
        """Contador de músicas"""
        return obj.musics.count()
    musics_count.short_description = 'Nº de Músicas'
    
    def add_music_link(self, obj):
        """Link para adicionar nova música"""
        if obj.pk:
            url = reverse('admin:music_music_add')
            return format_html(
                '<a href="{}" target="_blank" class="addlink" style="display: inline-block; '
                'padding: 5px 10px; background: #417690; color: white; text-decoration: none; '
                'border-radius: 3px; font-weight: bold;">➕ Adicionar Nova Música</a>',
                url
            )
        return "Salve a playlist primeiro para adicionar músicas"
    add_music_link.short_description = "Ações"
    
    def get_queryset(self, request):
        """Otimizar consultas"""
        return super().get_queryset(request).prefetch_related('musics')
