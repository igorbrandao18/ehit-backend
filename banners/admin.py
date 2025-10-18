from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Banner


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = [
        'title', 
        'banner_type', 
        'position', 
        'is_active', 
        'order',
        'start_date',
        'end_date',
        'image_preview',
        'created_at'
    ]
    
    list_filter = [
        'banner_type',
        'position', 
        'is_active',
        'created_at',
        'start_date',
        'end_date'
    ]
    
    search_fields = [
        'title',
        'description',
        'link_url'
    ]
    
    list_editable = [
        'is_active',
        'order'
    ]
    
    ordering = ['order', '-created_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('title', 'description', 'image')
        }),
        ('Configuração', {
            'fields': ('banner_type', 'position', 'link_url')
        }),
        ('Controle de Exibição', {
            'fields': ('is_active', 'order', 'start_date', 'end_date'),
            'description': 'Configure quando e onde o banner será exibido'
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    
    def image_preview(self, obj):
        """Exibe uma prévia da imagem do banner"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 50px; border-radius: 4px;" />',
                obj.image.url
            )
        return "Sem imagem"
    image_preview.short_description = "Prévia"
    
    def get_queryset(self, request):
        """Otimiza a consulta para evitar N+1 queries"""
        return super().get_queryset(request).select_related()
    
    def save_model(self, request, obj, form, change):
        """Salva o modelo e registra quem fez a alteração"""
        if not change:  # Se é um novo banner
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
    
    actions = ['activate_banners', 'deactivate_banners']
    
    def activate_banners(self, request, queryset):
        """Ação para ativar banners selecionados"""
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            f'{updated} banner(s) foram ativados com sucesso.'
        )
    activate_banners.short_description = "Ativar banners selecionados"
    
    def deactivate_banners(self, request, queryset):
        """Ação para desativar banners selecionados"""
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f'{updated} banner(s) foram desativados com sucesso.'
        )
    deactivate_banners.short_description = "Desativar banners selecionados"
    
    class Media:
        css = {
            'all': ('admin/css/banner_admin.css',)
        }
        js = ('admin/js/banner_admin.js',)