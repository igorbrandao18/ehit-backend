"""
Admin unificado para todos os models do sistema EHIT
Centraliza a administração de todos os modelos em um local
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Importar todos os models
from apps.users.models import User
from apps.artists.models import Artist, Album
from apps.music.models import Music
from apps.genres.models import Genre


# =============================================================================
# USERS ADMIN
# =============================================================================

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin customizado para o modelo User"""
    
    list_display = ('username', 'email', 'user_type', 'verified', 'followers_count', 'date_joined')
    list_filter = ('user_type', 'verified', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': ('user_type', 'bio', 'avatar', 'phone', 'birth_date', 'location', 'verified', 'followers_count')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informações Adicionais', {
            'fields': ('user_type', 'email', 'first_name', 'last_name')
        }),
    )


# =============================================================================
# ARTISTS ADMIN
# =============================================================================

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


# =============================================================================
# ALBUMS ADMIN
# =============================================================================

class MusicInline(admin.TabularInline):
    """Inline para músicas no admin de álbuns - simplificado"""
    model = Music
    extra = 1
    fields = ('title', 'file', 'is_active')
    verbose_name = "Música"
    verbose_name_plural = "Músicas do Álbum"
    can_delete = True
    show_change_link = True  # Permite clicar para editar a música

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    """Admin para o modelo Album"""
    
    list_display = ('name', 'artist', 'featured', 'get_musics_count', 'release_date', 'is_active', 'created_at')
    list_filter = ('featured', 'is_active', 'artist', 'created_at', 'release_date')
    search_fields = ('name', 'artist__stage_name')
    ordering = ('-featured', '-release_date', '-created_at')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('artist', 'name', 'is_active')
        }),
        ('Visual', {
            'fields': ('cover',)
        }),
        ('Lançamento', {
            'fields': ('release_date', 'featured')
        }),
        ('Músicas do Álbum', {
            'fields': ('existing_musics',),
            'description': 'Selecione músicas existentes do artista para adicionar ao álbum'
        }),
    )
    
    inlines = [MusicInline]  # Adiciona as músicas inline
    
    readonly_fields = ('created_at', 'updated_at', 'existing_musics')
    
    def existing_musics(self, obj):
        """Campo customizado para mostrar músicas existentes do artista"""
        if not obj.pk or not obj.artist:
            return "Selecione um artista e salve o álbum para ver músicas disponíveis"
        
        from apps.music.models import Music
        musics = Music.objects.filter(artist=obj.artist, album__isnull=True, is_active=True)
        
        if not musics.exists():
            return "Nenhuma música disponível para este artista"
        
        html = '<ul>'
        for music in musics:
            html += f'<li>{music.title} <a href="/admin/music/music/{music.id}/change/" target="_blank">[Ver]</a></li>'
        html += '</ul>'
        return html
    
    existing_musics.short_description = "Músicas Disponíveis do Artista (sem álbum)"
    existing_musics.allow_tags = True
    
    def save_formset(self, request, form, formset, change):
        """Define valores padrão para músicas ao salvar"""
        instances = formset.save(commit=False)
        for instance in instances:
            # Artista vem do álbum
            if not instance.artist and form.instance.artist:
                instance.artist = form.instance.artist
            
            # Gênero vem do artista do álbum
            if instance.artist and instance.artist.genre:
                instance.genre = instance.artist.genre
            
            # Duração padrão de 180s (3 minutos)
            if not instance.duration:
                instance.duration = 180
            
            # Capa vem do álbum
            if not instance.cover and form.instance.cover:
                instance.cover = form.instance.cover
            
            instance.save()
        
        # Deletar itens marcados
        for obj in formset.deleted_objects:
            obj.delete()


# =============================================================================
# PLAYLISTS ADMIN - REMOVED (handled in apps/playlists/admin.py)
# =============================================================================

# =============================================================================
# MUSIC ADMIN
# =============================================================================

@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    """Admin para o modelo Music"""
    
    list_display = ('title', 'artist', 'album', 'genre', 'duration', 'streams_count', 'downloads_count', 'likes_count', 'is_featured', 'created_at')
    list_filter = ('genre', 'album', 'is_featured', 'is_active', 'created_at', 'release_date')
    search_fields = ('title', 'album__name', 'artist__stage_name')
    ordering = ('-streams_count', '-created_at')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('artist', 'album', 'title', 'genre', 'duration')
        }),
        ('Arquivos', {
            'fields': ('file', 'cover', 'lyrics')
        }),
        ('Lançamento', {
            'fields': ('release_date', 'is_featured')
        }),
        ('Estatísticas', {
            'fields': ('streams_count', 'downloads_count', 'likes_count')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    readonly_fields = ('streams_count', 'downloads_count', 'likes_count', 'created_at', 'updated_at')
    
    def get_duration_formatted(self, obj):
        """Retorna duração formatada"""
        return obj.get_duration_formatted()
    get_duration_formatted.short_description = 'Duração'


# =============================================================================
# GENRES ADMIN
# =============================================================================

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Admin para o modelo Genre"""
    
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


# =============================================================================
# ADMIN SITE CONFIGURATION
# =============================================================================

# Configurações do site admin
admin.site.site_header = "EHIT Backend Administration"
admin.site.site_title = "EHIT Admin"
admin.site.index_title = "Sistema de Música EHIT"
