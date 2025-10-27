from django.db import models
from django.utils import timezone


class Banner(models.Model):
    """
    Modelo simplificado para gerenciar banners do sistema
    """
    
    name = models.CharField(
        max_length=200,
        default='Banner',
        verbose_name='Nome',
        help_text='Nome do banner'
    )
    
    image = models.ImageField(
        upload_to='banners/',
        verbose_name='Imagem',
        help_text='Imagem do banner'
    )
    
    link = models.URLField(
        blank=True,
        null=True,
        verbose_name='Link',
        help_text='URL para onde o banner deve redirecionar'
    )
    
    start_date = models.DateTimeField(
        verbose_name='Data de Início',
        help_text='Data e hora de início da exibição do banner'
    )
    
    end_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Data de Fim',
        help_text='Data e hora de fim da exibição do banner (opcional)'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )
    
    class Meta:
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'
        ordering = ['-start_date']
    
    def __str__(self):
        return self.name
    
    def is_currently_active(self):
        """Verifica se o banner está ativo no momento atual"""
        now = timezone.now()
        
        if self.start_date > now:
            return False
            
        if self.end_date and self.end_date < now:
            return False
            
        return True
    
    @classmethod
    def get_active_banners(cls):
        """Retorna banners ativos no momento atual"""
        now = timezone.now()
        
        queryset = cls.objects.filter(
            start_date__lte=now
        ).filter(
            models.Q(end_date__isnull=True) | models.Q(end_date__gte=now)
        )
        
        return queryset.order_by('-start_date')