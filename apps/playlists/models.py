from django.db import models
from apps.artists.models import BaseModel
from apps.music.models import Music


class Playlist(BaseModel):
    """
    Modelo para PlayHits
    
    Representa uma coleção de músicas com nome, capa e ativação.
    """
    name = models.CharField(
        max_length=200,
        verbose_name='Nome'
    )
    cover = models.ImageField(
        upload_to='playlist_covers/', 
        blank=True, 
        null=True,
        verbose_name='Capa'
    )
    musics = models.ManyToManyField(
        Music, 
        related_name='playlists',
        verbose_name='Músicas',
        blank=True
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name='Em Destaque',
        help_text='Se marcado, esta playlist aparecerá em destaque'
    )
    
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Ordem',
        help_text='Ordem de exibição no array (menor número = maior prioridade)'
    )
    
    class Meta:
        verbose_name = 'PlayHit'
        verbose_name_plural = 'PlayHits'
        ordering = ['order', '-is_featured', '-created_at']
    
    def __str__(self):
        return self.name
    
    def get_total_duration(self):
        """Retorna duração total da playlist em segundos"""
        total = sum(
            music.duration for music in self.musics.all() 
            if music.duration is not None
        )
        return total or 0
    
    def get_total_duration_formatted(self):
        """Retorna duração total formatada (HH:MM:SS)"""
        total_seconds = self.get_total_duration()
        if total_seconds is None or total_seconds == 0:
            return "0:00"
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"
    
    def get_musics_count(self):
        """Retorna número de músicas na playlist"""
        return self.musics.count()
    
    def add_music(self, music):
        """Adiciona música à playlist"""
        self.musics.add(music)
    
    def remove_music(self, music):
        """Remove música da playlist"""
        self.musics.remove(music)


