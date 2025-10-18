from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Usuário customizado baseado no Sua Música
    
    Tipos de usuário:
    - listener: Ouvinte comum
    - artist: Artista que faz upload de músicas
    - venue: Casa de show que cria eventos
    - admin: Administrador da plataforma
    """
    USER_TYPES = [
        ('listener', 'Ouvinte'),
        ('artist', 'Artista'),
        ('venue', 'Casa de Show'),
        ('admin', 'Administrador'),
    ]
    
    user_type = models.CharField(
        max_length=20, 
        choices=USER_TYPES, 
        default='listener',
        verbose_name='Tipo de Usuário'
    )
    bio = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Biografia'
    )
    avatar = models.ImageField(
        upload_to='avatars/', 
        blank=True, 
        null=True,
        verbose_name='Avatar'
    )
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        verbose_name='Telefone'
    )
    birth_date = models.DateField(
        blank=True, 
        null=True,
        verbose_name='Data de Nascimento'
    )
    location = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name='Localização'
    )
    verified = models.BooleanField(
        default=False,
        verbose_name='Verificado'
    )
    followers_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Seguidores'
    )
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
    @property
    def is_artist(self):
        """Verifica se o usuário é um artista"""
        return self.user_type == 'artist'
    
    @property
    def is_venue(self):
        """Verifica se o usuário é uma casa de show"""
        return self.user_type == 'venue'
    
    @property
    def is_admin(self):
        """Verifica se o usuário é administrador"""
        return self.user_type == 'admin'
