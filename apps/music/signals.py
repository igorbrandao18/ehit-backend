from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Music
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Music)
def compress_audio_on_upload(sender, instance, created, **kwargs):
    """
    Comprime automaticamente o áudio após o upload
    """
    if created and instance.file:
        try:
            # Verificar se o arquivo é maior que 10MB
            file_size_mb = instance.get_file_size_mb()
            
            if file_size_mb > 10:  # Comprimir arquivos maiores que 10MB
                logger.info(f"Comprimindo áudio da música {instance.title} ({file_size_mb}MB)")
                
                # Comprimir com qualidade média
                success = instance.compress_audio(quality='medium')
                
                if success:
                    new_size = instance.get_file_size_mb()
                    logger.info(f"Compressão bem-sucedida: {file_size_mb}MB -> {new_size}MB")
                else:
                    logger.warning(f"Falha na compressão da música {instance.title}")
                    
        except Exception as e:
            logger.error(f"Erro ao comprimir áudio da música {instance.title}: {e}")
