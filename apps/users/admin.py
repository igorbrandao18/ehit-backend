"""
Admin unificado para todos os models do sistema EHIT
Centraliza a administração de todos os modelos em um local
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db import models

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

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    """Admin para o modelo Album - similar a Playlist com filter_horizontal"""
    
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
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    class MusicInline(admin.TabularInline):
        """Inline para músicas no admin de álbuns - igual playlists"""
        model = Music
        extra = 0  # Não criar linha vazia automaticamente
        fields = ('title', 'file', 'is_active')  # Simplificado
        verbose_name = "Música"
        verbose_name_plural = "Músicas do Álbum"
        can_delete = True
        show_change_link = True
    
    inlines = [MusicInline]
    
    def save_formset(self, request, form, formset, change):
        """Define valores padrão para músicas ao salvar"""
        instances = formset.save(commit=False)
        for instance in instances:
            # Validações básicas primeiro - se não tiver dados mínimos, pular
            if not instance.title or not instance.title.strip():
                # Se não tem título, pular esta instância (linha vazia)
                continue
            
            # Álbum vem do form (o álbum sendo editado)
            if not instance.album and form.instance.pk:
                instance.album = form.instance
            
            # Artista vem do álbum - verificar de forma segura
            try:
                has_artist = instance.artist_id is not None
            except AttributeError:
                has_artist = False
            
            if not has_artist and form.instance.artist:
                instance.artist = form.instance.artist
            
            # Validação crítica: artista é obrigatório
            try:
                if not instance.artist_id:
                    # Se não tem artista, pular esta instância
                    continue
            except AttributeError:
                # Se não consegue verificar, pular esta instância
                continue
            
            # Gênero vem do artista do álbum (apenas se não tiver)
            if not instance.genre:
                try:
                    if instance.artist and instance.artist.genre:
                        instance.genre = instance.artist.genre
                except (AttributeError, TypeError):
                    pass
            
            # Capa vem do álbum (apenas se não tiver)
            if not instance.cover and form.instance.cover:
                instance.cover = form.instance.cover
            
            # Não definir duração padrão - deixar o signal calcular
            # A duração será calculada automaticamente pelo signal após o arquivo ser salvo
            
            # Salvar a instância com tratamento de erros
            try:
                instance.save()
                # Salvar relacionamento ManyToMany se houver
                formset.save_m2m()
            except Exception as e:
                # Log do erro mas não interromper o processo
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Erro ao salvar música '{instance.title if hasattr(instance, 'title') else 'sem título'}': {e}")
                # Continuar com as próximas instâncias
        
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
    
    list_display = ('title', 'artist', 'album', 'genre', 'streams_count', 'downloads_count', 'likes_count', 'is_featured', 'created_at')
    list_filter = ('genre', 'album', 'is_featured', 'is_active', 'created_at', 'release_date')
    search_fields = ('title', 'album__name', 'artist__stage_name')
    ordering = ('-streams_count', '-created_at')
    
    class Media:
        css = {
            'all': ('admin/css/music_admin.css',)
        }
        js = ('admin/js/music_admin.js',)
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('artist', 'album', 'title', 'genre'),
            'description': '💡 O campo Álbum é OPCIONAL. Deixe em branco se a música não faz parte de um álbum.'
        }),
        ('Arquivos', {
            'fields': ('file', 'cover'),
            'description': '🎵 Limite de upload: 500MB por arquivo. Arquivos grandes serão processados automaticamente.'
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
        ('Metadados', {
            'fields': ('created_at', 'updated_at', 'duration'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('streams_count', 'downloads_count', 'likes_count', 'created_at', 'updated_at', 'duration')
    
    autocomplete_fields = ['artist', 'album', 'genre']
    
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
