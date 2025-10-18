from django.db import models
from apps.users.models import User
from apps.artists.models import BaseModel
from apps.music.models import Music


class Playlist(BaseModel):
    """
    Modelo para playlists baseado no Sua Música
    
    Representa uma coleção de músicas criada por usuários.
    Pode ser pública ou privada e permite organização
    personalizada de músicas favoritas.
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='playlists',
        verbose_name='Usuário'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Nome'
    )
    description = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Descrição'
    )
    is_public = models.BooleanField(
        default=True,
        verbose_name='Pública'
    )
    cover = models.ImageField(
        upload_to='playlist_covers/', 
        blank=True, 
        null=True,
        verbose_name='Capa'
    )
    musics = models.ManyToManyField(
        Music, 
        through='PlaylistMusic', 
        related_name='playlists',
        verbose_name='Músicas'
    )
    followers_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Seguidores'
    )
    
    class Meta:
        verbose_name = 'Playlist'
        verbose_name_plural = 'Playlists'
        ordering = ['-followers_count', '-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"
    
    def get_total_duration(self):
        """Retorna duração total da playlist em segundos"""
        return sum(music.duration for music in self.musics.all())
    
    def get_total_duration_formatted(self):
        """Retorna duração total formatada (HH:MM:SS)"""
        total_seconds = self.get_total_duration()
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"
    
    def get_musics_count(self):
        """Retorna número de músicas na playlist"""
        return self.musics.count()
    
    def add_music(self, music, order=None):
        """Adiciona música à playlist"""
        if order is None:
            order = self.get_musics_count()
        
        PlaylistMusic.objects.create(
            playlist=self,
            music=music,
            order=order
        )
    
    def remove_music(self, music):
        """Remove música da playlist"""
        PlaylistMusic.objects.filter(
            playlist=self,
            music=music
        ).delete()
    
    def reorder_musics(self, music_orders):
        """Reordena músicas na playlist"""
        for music_id, order in music_orders.items():
            PlaylistMusic.objects.filter(
                playlist=self,
                music_id=music_id
            ).update(order=order)


class PlaylistMusic(models.Model):
    """
    Modelo intermediário para playlist-música
    
    Permite ordenação personalizada das músicas
    dentro de cada playlist.
    """
    playlist = models.ForeignKey(
        Playlist, 
        on_delete=models.CASCADE,
        verbose_name='Playlist'
    )
    music = models.ForeignKey(
        Music, 
        on_delete=models.CASCADE,
        verbose_name='Música'
    )
    added_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Adicionado em'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Ordem'
    )
    
    class Meta:
        unique_together = ['playlist', 'music']
        ordering = ['order', '-added_at']
        verbose_name = 'Música da Playlist'
        verbose_name_plural = 'Músicas da Playlist'
    
    def __str__(self):
        return f"{self.playlist.name} - {self.music.title}"


class UserFavorite(models.Model):
    """
    Modelo para músicas favoritas dos usuários
    
    Permite que usuários marquem músicas como favoritas
    sem precisar criar uma playlist específica.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Usuário'
    )
    music = models.ForeignKey(
        Music,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='Música'
    )
    added_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Adicionado em'
    )
    
    class Meta:
        unique_together = ['user', 'music']
        ordering = ['-added_at']
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'
    
    def __str__(self):
        return f"{self.user.username} - {self.music.title}"
