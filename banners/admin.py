from django.contrib import admin
from django.utils.html import format_html
from .models import Banner


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'image_preview',
        'link',
        'start_date',
        'end_date',
        'is_active_status',
        'created_at'
    ]
    
    list_filter = [
        'created_at',
        'start_date',
        'end_date'
    ]
    
    search_fields = [
        'name',
        'link'
    ]
    
    ordering = ['-start_date']
    
    fieldsets = (
        ('Informações', {
            'fields': ('name', 'image', 'link')
        }),
        ('Controle de Exibição', {
            'fields': ('start_date', 'end_date'),
            'description': 'Configure quando o banner será exibido'
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def image_preview(self, obj):
        """Exibe uma prévia da imagem do banner"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 50px; border-radius: 4px;" />',
                obj.image.url
            )
        return "Sem imagem"
    image_preview.short_description = "Imagem"
    
    def is_active_status(self, obj):
        """Exibe o status do banner"""
        if obj.is_currently_active():
            return "✅ Ativo"
        return "❌ Inativo"
    is_active_status.short_description = "Status"