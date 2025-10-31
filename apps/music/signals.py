from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Music
import logging
import os

logger = logging.getLogger(__name__)

@receiver(pre_save, sender=Music)
def calculate_duration_before_save(sender, instance, **kwargs):
    """
    Calcula a duração da música automaticamente antes de salvar
    Apenas se o arquivo já existe no disco (caso de atualização)
    """
    if instance.file and not instance.duration:
        try:
            # Verificar se o arquivo existe no disco antes de tentar calcular
            if hasattr(instance.file, 'path'):
                try:
                    if os.path.exists(instance.file.path):
                        logger.info(f"Calculando duração da música {instance.title} (antes de salvar)")
                        duration = instance.calculate_duration()
                        if duration:
                            instance.duration = duration
                            logger.info(f"Duração calculada: {duration} segundos ({duration//60}:{duration%60:02d})")
                        else:
                            logger.warning(f"Não foi possível calcular a duração da música {instance.title}")
                    else:
                        # Arquivo ainda não foi salvo, será calculado após salvar
                        logger.debug(f"Arquivo ainda não salvo para {instance.title}, cálculo será feito após salvar")
                except (ValueError, AttributeError, OSError) as e:
                    # Arquivo pode estar em memória ou ainda não ter caminho válido
                    logger.debug(f"Arquivo sem caminho válido para {instance.title}: {e}. Cálculo será feito após salvar")
        except Exception as e:
            logger.error(f"Erro ao calcular duração da música {instance.title}: {e}")

@receiver(post_save, sender=Music)
def handle_music_file_after_save(sender, instance, created, **kwargs):
    """
    Processa o arquivo de áudio após salvar:
    1. Calcula duração se ainda não foi calculada
    2. Comprime automaticamente se necessário
    """
    if instance.file:
        try:
            # 1. Calcular duração se ainda não foi calculada
            if not instance.duration:
                try:
                    if hasattr(instance.file, 'path') and os.path.exists(instance.file.path):
                        logger.info(f"Calculando duração da música {instance.title} (após salvar)")
                        duration = instance.calculate_duration()
                        if duration:
                            # Atualizar sem disparar signals novamente
                            Music.objects.filter(pk=instance.pk).update(duration=duration)
                            logger.info(f"Duração calculada: {duration} segundos ({duration//60}:{duration%60:02d})")
                except Exception as e:
                    logger.error(f"Erro ao calcular duração após salvar {instance.title}: {e}")
            
            # 2. Comprimir áudio se necessário (apenas em novas criações para evitar reprocessar)
            if created:
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
                    
        except Exception as e:
            logger.error(f"Erro ao processar arquivo da música {instance.title}: {e}")
