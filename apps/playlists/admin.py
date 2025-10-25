from django.contrib import admin
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
        'id', 'created_at', 'updated_at', 'musics_count'
    ]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('id', 'name', 'cover')
        }),
        ('Configurações', {
            'fields': ('is_active', 'is_featured')
        }),
        ('Músicas', {
            'fields': ('musics', 'musics_count'),
            'classes': ('collapse',)
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
    
    def get_queryset(self, request):
        """Otimizar consultas"""
        return super().get_queryset(request).prefetch_related('musics')
