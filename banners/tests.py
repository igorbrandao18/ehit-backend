from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from banners.models import Banner


class BannerModelTest(TestCase):
    """Testes para o modelo Banner"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.banner_data = {
            'title': 'Banner de Teste',
            'description': 'Descrição do banner de teste',
            'banner_type': 'home',
            'position': 'top',
            'is_active': True,
            'order': 1,
            'start_date': timezone.now(),
        }
    
    def test_banner_creation(self):
        """Testa a criação de um banner"""
        banner = Banner.objects.create(**self.banner_data)
        
        self.assertEqual(banner.title, 'Banner de Teste')
        self.assertEqual(banner.banner_type, 'home')
        self.assertEqual(banner.position, 'top')
        self.assertTrue(banner.is_active)
        self.assertEqual(banner.order, 1)
    
    def test_banner_str_representation(self):
        """Testa a representação string do banner"""
        banner = Banner.objects.create(**self.banner_data)
        expected_str = f"{banner.title} - {banner.get_banner_type_display()}"
        self.assertEqual(str(banner), expected_str)
    
    def test_banner_is_currently_active(self):
        """Testa se o banner está ativo no momento atual"""
        banner = Banner.objects.create(**self.banner_data)
        self.assertTrue(banner.is_currently_active())
    
    def test_banner_not_active_when_inactive(self):
        """Testa banner inativo"""
        self.banner_data['is_active'] = False
        banner = Banner.objects.create(**self.banner_data)
        self.assertFalse(banner.is_currently_active())
    
    def test_banner_not_active_when_future_start_date(self):
        """Testa banner com data de início futura"""
        future_date = timezone.now() + timezone.timedelta(days=1)
        self.banner_data['start_date'] = future_date
        banner = Banner.objects.create(**self.banner_data)
        self.assertFalse(banner.is_currently_active())
    
    def test_banner_not_active_when_past_end_date(self):
        """Testa banner com data de fim passada"""
        past_date = timezone.now() - timezone.timedelta(days=1)
        self.banner_data['end_date'] = past_date
        banner = Banner.objects.create(**self.banner_data)
        self.assertFalse(banner.is_currently_active())
    
    def test_get_active_banners_class_method(self):
        """Testa o método de classe get_active_banners"""
        # Criar banners ativos e inativos
        Banner.objects.create(**self.banner_data)
        
        inactive_data = self.banner_data.copy()
        inactive_data['is_active'] = False
        inactive_data['title'] = 'Banner Inativo'
        Banner.objects.create(**inactive_data)
        
        active_banners = Banner.get_active_banners()
        self.assertEqual(active_banners.count(), 1)
        self.assertEqual(active_banners.first().title, 'Banner de Teste')
    
    def test_get_active_banners_with_type_filter(self):
        """Testa filtro por tipo de banner"""
        Banner.objects.create(**self.banner_data)
        
        artist_data = self.banner_data.copy()
        artist_data['banner_type'] = 'artist'
        artist_data['title'] = 'Banner Artista'
        Banner.objects.create(**artist_data)
        
        home_banners = Banner.get_active_banners(banner_type='home')
        self.assertEqual(home_banners.count(), 1)
        self.assertEqual(home_banners.first().title, 'Banner de Teste')
    
    def test_get_active_banners_with_position_filter(self):
        """Testa filtro por posição"""
        Banner.objects.create(**self.banner_data)
        
        bottom_data = self.banner_data.copy()
        bottom_data['position'] = 'bottom'
        bottom_data['title'] = 'Banner Bottom'
        Banner.objects.create(**bottom_data)
        
        top_banners = Banner.get_active_banners(position='top')
        self.assertEqual(top_banners.count(), 1)
        self.assertEqual(top_banners.first().title, 'Banner de Teste')
    
    def test_banner_ordering(self):
        """Testa a ordenação dos banners"""
        Banner.objects.create(**self.banner_data)
        
        second_banner_data = self.banner_data.copy()
        second_banner_data['title'] = 'Segundo Banner'
        second_banner_data['order'] = 2
        Banner.objects.create(**second_banner_data)
        
        banners = Banner.objects.all()
        self.assertEqual(banners[0].order, 1)
        self.assertEqual(banners[1].order, 2)
    
    def test_banner_meta_verbose_names(self):
        """Testa os nomes verbose do modelo"""
        self.assertEqual(Banner._meta.verbose_name, 'Banner')
        self.assertEqual(Banner._meta.verbose_name_plural, 'Banners')
    
    def test_banner_choices(self):
        """Testa as opções de escolha dos campos"""
        banner = Banner.objects.create(**self.banner_data)
        
        # Testa choices do banner_type
        self.assertIn(('home', 'Página Inicial'), Banner.BANNER_TYPES)
        self.assertIn(('artist', 'Página do Artista'), Banner.BANNER_TYPES)
        
        # Testa choices da position
        self.assertIn(('top', 'Topo'), Banner.POSITIONS)
        self.assertIn(('bottom', 'Rodapé'), Banner.POSITIONS)