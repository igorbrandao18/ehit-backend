from django.db import models
from django.utils.text import slugify

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nome")
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name="Slug")
    description = models.TextField(blank=True, null=True, verbose_name="Descrição")
    color = models.CharField(max_length=7, default="#FF6B6B", verbose_name="Cor")
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name="Ícone")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subgenres', verbose_name="Gênero Pai")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Gênero"
        verbose_name_plural = "Gêneros"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def song_count(self):
        """Retorna o número de músicas neste gênero"""
        return self.musics.count()

    @property
    def artist_count(self):
        """Retorna o número de artistas neste gênero"""
        return self.artists.count()
