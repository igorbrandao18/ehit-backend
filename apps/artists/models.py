from django.db import models


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
    Modelo para Artistas simplificado
    
    Representa artistas com informações essenciais: nome, capa e gênero.
    """
    stage_name = models.CharField(
        max_length=200,
        verbose_name='Nome Artístico'
    )
    photo = models.ImageField(
        upload_to='artists/photos/',
        blank=True,
        null=True,
        verbose_name='Foto do Artista',
        help_text='Foto de perfil do artista'
    )
    genre = models.ForeignKey(
        'genres.Genre',
        on_delete=models.SET_NULL,
        blank=True, 
        null=True,
        related_name='artists',
        verbose_name='Gênero Musical'
    )
    
    class Meta:
        verbose_name = 'Artista'
        verbose_name_plural = 'Artistas'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.stage_name


class Album(BaseModel):
    """
    Modelo para Álbuns dos artistas
    
    Representa álbuns com informações essenciais: nome, artista, capa e destaque.
    """
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name='albums',
        verbose_name='Artista'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Nome do Álbum'
    )
    cover = models.ImageField(
        upload_to='albums/covers/',
        blank=True,
        null=True,
        verbose_name='Capa do Álbum',
        help_text='Capa do álbum'
    )
    release_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Data de Lançamento'
    )
    featured = models.BooleanField(
        default=False,
        verbose_name='Destaque',
        help_text='Álbum em destaque'
    )
    
    class Meta:
        verbose_name = 'Álbum'
        verbose_name_plural = 'Álbuns'
        ordering = ['-featured', '-release_date', '-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.artist.stage_name}"
    
    def get_musics_count(self):
        """Retorna número de músicas no álbum"""
        return self.musics.count()
