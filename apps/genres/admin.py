from django.contrib import admin
from .models import Genre

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'is_active', 'song_count', 'artist_count', 'created_at']
    list_filter = ['is_active', 'parent', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'song_count', 'artist_count']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'slug', 'description', 'is_active')
        }),
        ('Aparência', {
            'fields': ('color', 'icon')
        }),
        ('Hierarquia', {
            'fields': ('parent',)
        }),
        ('Estatísticas', {
            'fields': ('song_count', 'artist_count'),
            'classes': ('collapse',)
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
