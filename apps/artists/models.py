from django.db import models
from django.utils import timezone
from apps.users.models import User
from apps.constants import GENRE_CHOICES


class BaseModel(models.Model):
    """Modelo base com campos comuns"""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    
    class Meta:
        abstract = True
        ordering = ['-created_at']


class Artist(BaseModel):
    """
    Modelo para artistas baseado no Sua Música
    
    Representa artistas que fazem upload de músicas na plataforma.
    Cada artista tem um perfil detalhado com informações pessoais,
    estatísticas e links sociais.
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='artist_profile',
        verbose_name='Usuário'
    )
    stage_name = models.CharField(
        max_length=200,
        verbose_name='Nome Artístico'
    )
    real_name = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        verbose_name='Nome Real'
    )
    bio = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Biografia'
    )
    genre = models.CharField(
        max_length=100, 
        choices=GENRE_CHOICES,
        blank=True, 
        null=True,
        verbose_name='Gênero Musical'
    )
    location = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name='Localização'
    )
    website = models.URLField(
        blank=True, 
        null=True,
        verbose_name='Website'
    )
    social_links = models.JSONField(
        default=dict, 
        blank=True,
        verbose_name='Links Sociais',
        help_text='Links para redes sociais (Instagram, YouTube, etc.)'
    )
    verified = models.BooleanField(
        default=False,
        verbose_name='Verificado'
    )
    followers_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Seguidores'
    )
    monthly_listeners = models.PositiveIntegerField(
        default=0,
        verbose_name='Ouvintes Mensais'
    )
    
    class Meta:
        verbose_name = 'Artista'
        verbose_name_plural = 'Artistas'
        ordering = ['-followers_count', '-created_at']
    
    def __str__(self):
        return self.stage_name
    
    def get_total_streams(self):
        """Retorna total de streams de todas as músicas"""
        return sum(music.streams_count for music in self.musics.all())
    
    def get_total_downloads(self):
        """Retorna total de downloads de todas as músicas"""
        return sum(music.downloads_count for music in self.musics.all())
    
    def get_total_likes(self):
        """Retorna total de curtidas de todas as músicas"""
        return sum(music.likes_count for music in self.musics.all())
    
    @property
    def is_verified(self):
        """Verifica se o artista é verificado"""
        return self.verified
    
    def increment_followers(self):
        """Incrementa contador de seguidores"""
        self.followers_count += 1
        self.save(update_fields=['followers_count'])
    
    def decrement_followers(self):
        """Decrementa contador de seguidores"""
        if self.followers_count > 0:
            self.followers_count -= 1
            self.save(update_fields=['followers_count'])
