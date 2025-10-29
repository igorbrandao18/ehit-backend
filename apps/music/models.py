from django.db import models
from django.utils import timezone
from apps.artists.models import BaseModel, Artist, Album
import os
import subprocess
import tempfile
from django.core.files import File


class Music(BaseModel):
    """
    Modelo para músicas baseado no Sua Música
    
    Representa uma música individual na plataforma.
    Cada música pertence a um artista e pode estar em um álbum.
    """
    artist = models.ForeignKey(
        Artist, 
        on_delete=models.CASCADE, 
        related_name='musics',
        verbose_name='Artista'
    )
    album = models.ForeignKey(
        Album,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='musics',
        verbose_name='Álbum'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Título'
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
        blank=True,
        null=True,
        help_text="Duração em segundos (calculada automaticamente)",
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
        if self.duration is None:
            return "0:00"
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
    
    def compress_audio(self, quality='medium'):
        """
        Comprime o arquivo de áudio usando FFmpeg
        
        Args:
            quality (str): Qualidade da compressão ('low', 'medium', 'high')
                - low: 128kbps (menor tamanho)
                - medium: 192kbps (balanceado)
                - high: 320kbps (melhor qualidade)
        """
        if not self.file:
            return False
        
        # Configurações de qualidade
        quality_settings = {
            'low': '128k',
            'medium': '192k', 
            'high': '320k'
        }
        
        bitrate = quality_settings.get(quality, '192k')
        
        try:
            # Criar arquivo temporário
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                temp_path = temp_file.name
            
            # Comando FFmpeg para compressão
            cmd = [
                'ffmpeg',
                '-i', self.file.path,  # Arquivo de entrada
                '-b:a', bitrate,      # Bitrate de áudio
                '-ac', '2',           # 2 canais (estéreo)
                '-ar', '44100',       # Sample rate
                '-y',                 # Sobrescrever arquivo de saída
                temp_path             # Arquivo de saída
            ]
            
            # Executar compressão
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Verificar se o arquivo comprimido é menor
                original_size = os.path.getsize(self.file.path)
                compressed_size = os.path.getsize(temp_path)
                
                if compressed_size < original_size:
                    # Substituir o arquivo original pelo comprimido
                    with open(temp_path, 'rb') as compressed_file:
                        django_file = File(compressed_file)
                        self.file.save(
                            os.path.basename(self.file.name),
                            django_file,
                            save=True
                        )
                    
                    # Limpar arquivo temporário
                    os.unlink(temp_path)
                    
                    return True
                else:
                    # Se não conseguiu comprimir, manter o original
                    os.unlink(temp_path)
                    return False
            else:
                # Erro na compressão
                os.unlink(temp_path)
                return False
                
        except Exception as e:
            print(f"Erro na compressão: {e}")
            return False
    
    def get_file_size_mb(self):
        """Retorna o tamanho do arquivo em MB"""
        if self.file and os.path.exists(self.file.path):
            size_bytes = os.path.getsize(self.file.path)
            return round(size_bytes / (1024 * 1024), 2)
        return 0
