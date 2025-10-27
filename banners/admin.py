from django.contrib import admin
from .models import Banner


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
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
            'fields': ('name', 'link')
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
    
    def is_active_status(self, obj):
        """Exibe o status do banner"""
        if obj.is_currently_active():
            return "✅ Ativo"
        return "❌ Inativo"
    is_active_status.short_description = "Status"