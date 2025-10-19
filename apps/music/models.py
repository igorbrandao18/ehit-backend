from django.db import models
from django.utils import timezone
from apps.artists.models import BaseModel, Artist


class Music(BaseModel):
    """
    Modelo para músicas baseado no Sua Música
    
    Representa uma música individual na plataforma.
    Cada música pertence a um artista e possui metadados
    completos incluindo arquivo de áudio, capa, letras e estatísticas.
    """
    artist = models.ForeignKey(
        Artist, 
        on_delete=models.CASCADE, 
        related_name='musics',
        verbose_name='Artista'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Título'
    )
    album = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        verbose_name='Álbum'
    )
    genre = models.ForeignKey(
        'genres.Genre',
        on_delete=models.SET_NULL,
        blank=True, 
        null=True,
        related_name='musics',
        verbose_name='Gênero Musical'
    )
    duration = models.PositiveIntegerField(
        help_text="Duração em segundos",
        verbose_name='Duração (segundos)'
    )
    file = models.FileField(
        upload_to='music/', 
        help_text="Arquivo de áudio",
        verbose_name='Arquivo de Áudio'
    )
    cover = models.ImageField(
        upload_to='covers/', 
        blank=True, 
        null=True,
        verbose_name='Capa'
    )
    lyrics = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Letra'
    )
    release_date = models.DateField(
        default=timezone.now,
        verbose_name='Data de Lançamento'
    )
    streams_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Reproduções'
    )
    downloads_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Downloads'
    )
    likes_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Curtidas'
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name='Em Destaque'
    )
    
    class Meta:
        verbose_name = 'Música'
        verbose_name_plural = 'Músicas'
        ordering = ['-streams_count', '-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.artist.stage_name}"
    
    def get_stream_url(self):
        """Retorna URL para streaming"""
        return f"/api/music/{self.id}/stream/"
    
    def get_download_url(self):
        """Retorna URL para download"""
        return f"/api/music/{self.id}/download/"
    
    def get_duration_formatted(self):
        """Retorna duração formatada (MM:SS)"""
        minutes, seconds = divmod(self.duration, 60)
        return f"{minutes}:{seconds:02d}"
    
    def increment_streams(self):
        """Incrementa contador de streams"""
        self.streams_count += 1
        self.save(update_fields=['streams_count'])
    
    def increment_downloads(self):
        """Incrementa contador de downloads"""
        self.downloads_count += 1
        self.save(update_fields=['downloads_count'])
    
    def increment_likes(self):
        """Incrementa contador de curtidas"""
        self.likes_count += 1
        self.save(update_fields=['likes_count'])
    
    def decrement_likes(self):
        """Decrementa contador de curtidas"""
        if self.likes_count > 0:
            self.likes_count -= 1
            self.save(update_fields=['likes_count'])
    
    @property
    def is_popular(self):
        """Verifica se a música é popular (mais de 1000 streams)"""
        return self.streams_count > 1000
    
    @property
    def is_trending(self):
        """Verifica se a música está em alta (criada nas últimas 7 dias e com muitos streams)"""
        from datetime import timedelta
        week_ago = timezone.now() - timedelta(days=7)
        return self.created_at >= week_ago and self.streams_count > 100
