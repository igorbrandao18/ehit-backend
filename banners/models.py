from django.db import models
from django.utils import timezone
from django.db import models


class Banner(models.Model):
    """
    Modelo para gerenciar banners do sistema
    """
    
    BANNER_TYPES = [
        ('home', 'Página Inicial'),
        ('artist', 'Página do Artista'),
        ('music', 'Página de Música'),
        ('playlist', 'Página de Playlist'),
        ('general', 'Geral'),
    ]
    
    POSITIONS = [
        ('top', 'Topo'),
        ('middle', 'Meio'),
        ('bottom', 'Rodapé'),
        ('sidebar', 'Barra Lateral'),
    ]
    
    title = models.CharField(
        max_length=200,
        verbose_name='Título',
        help_text='Título do banner'
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descrição',
        help_text='Descrição do banner'
    )
    
    image = models.ImageField(
        upload_to='banners/',
        verbose_name='Imagem',
        help_text='Imagem do banner'
    )
    
    link_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='URL de Destino',
        help_text='URL para onde o banner deve redirecionar'
    )
    
    banner_type = models.CharField(
        max_length=20,
        choices=BANNER_TYPES,
        default='general',
        verbose_name='Tipo de Banner',
        help_text='Tipo de página onde o banner será exibido'
    )
    
    position = models.CharField(
        max_length=20,
        choices=POSITIONS,
        default='top',
        verbose_name='Posição',
        help_text='Posição onde o banner será exibido'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Ativo',
        help_text='Se o banner está ativo e será exibido'
    )
    
    start_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Data de Início',
        help_text='Data e hora de início da exibição do banner'
    )
    
    end_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Data de Fim',
        help_text='Data e hora de fim da exibição do banner (opcional)'
    )
    
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Ordem',
        help_text='Ordem de exibição (menor número = maior prioridade)'
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
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.get_banner_type_display()}"
    
    def is_currently_active(self):
        """Verifica se o banner está ativo no momento atual"""
        now = timezone.now()
        
        if not self.is_active:
            return False
            
        if self.start_date > now:
            return False
            
        if self.end_date and self.end_date < now:
            return False
            
        return True
    
    @classmethod
    def get_active_banners(cls, banner_type=None, position=None):
        """Retorna banners ativos filtrados por tipo e posição"""
        queryset = cls.objects.filter(is_active=True)
        
        if banner_type:
            queryset = queryset.filter(banner_type=banner_type)
            
        if position:
            queryset = queryset.filter(position=position)
        
        # Filtrar por data atual
        now = timezone.now()
        queryset = queryset.filter(
            start_date__lte=now
        ).filter(
            models.Q(end_date__isnull=True) | models.Q(end_date__gte=now)
        )
        
        return queryset.order_by('order', '-created_at')