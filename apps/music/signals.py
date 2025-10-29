from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Music
import logging

logger = logging.getLogger(__name__)

@receiver(pre_save, sender=Music)
def calculate_duration_before_save(sender, instance, **kwargs):
    """
    Calcula a duração da música automaticamente antes de salvar
    """
    if instance.file and not instance.duration:
        try:
            logger.info(f"Calculando duração da música {instance.title}")
            duration = instance.calculate_duration()
            if duration:
                instance.duration = duration
                logger.info(f"Duração calculada: {duration} segundos ({duration//60}:{duration%60:02d})")
            else:
                logger.warning(f"Não foi possível calcular a duração da música {instance.title}")
        except Exception as e:
            logger.error(f"Erro ao calcular duração da música {instance.title}: {e}")

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
