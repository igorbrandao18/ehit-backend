from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Music
import logging
import os

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Music)
def calculate_duration_after_save(sender, instance, created, **kwargs):
    """
    Calcula a duração da música após salvar (quando o arquivo já está no disco).
    Isso é rápido pois apenas lê metadados do arquivo de áudio.
    
    NOTA: Compressão de áudio foi removida - ela bloqueava o upload.
    Para comprimir, use uma tarefa assíncrona ou faça manualmente.
    """
    # Apenas calcular duração se for uma nova criação e ainda não tiver duração
    if instance.file and created and not instance.duration:
        try:
            if hasattr(instance.file, 'path') and os.path.exists(instance.file.path):
                # Calcular duração (rápido - apenas metadados)
                duration = instance.calculate_duration()
                if duration:
                    # Atualizar sem disparar signals novamente
                    Music.objects.filter(pk=instance.pk).update(duration=duration)
                    logger.info(f"Duração calculada: {duration}s para {instance.title}")
        except Exception as e:
            logger.error(f"Erro ao calcular duração: {e}")
