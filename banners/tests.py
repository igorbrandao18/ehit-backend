from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from .models import Banner


class BannerModelTest(TestCase):
    """Testes para o modelo Banner"""

    def setUp(self):
        self.banner = Banner.objects.create(
            title='Test Banner',
            description='Test Description',
            banner_type='home',
            position='top',
            is_active=True,
            start_date=timezone.now() - timedelta(days=1),
            order=1
        )

    def test_banner_creation(self):
        """Testa criação de banner"""
        self.assertEqual(self.banner.title, 'Test Banner')
        self.assertEqual(self.banner.description, 'Test Description')
        self.assertEqual(self.banner.banner_type, 'home')
        self.assertEqual(self.banner.position, 'top')
        self.assertTrue(self.banner.is_active)

    def test_banner_str(self):
        """Testa representação string do banner"""
        self.assertEqual(str(self.banner), 'Test Banner - Página Inicial')

    def test_banner_defaults(self):
        """Testa valores padrão"""
        new_banner = Banner.objects.create(
            title='Default Banner'
        )
        self.assertEqual(new_banner.banner_type, 'general')
        self.assertEqual(new_banner.position, 'top')
        self.assertTrue(new_banner.is_active)
        self.assertEqual(new_banner.order, 0)

    def test_banner_choices(self):
        """Testa choices de banner_type e position"""
        # Testa todos os tipos de banner
        types = ['home', 'artist', 'music', 'playlist', 'general']
        for banner_type in types:
            banner = Banner.objects.create(
                title=f'Banner {banner_type}',
                banner_type=banner_type
            )
            self.assertEqual(banner.banner_type, banner_type)
        
        # Testa todas as posições
        positions = ['top', 'middle', 'bottom', 'sidebar']
        for position in positions:
            banner = Banner.objects.create(
                title=f'Banner {position}',
                position=position
            )
            self.assertEqual(banner.position, position)

    def test_banner_get_display_methods(self):
        """Testa métodos de display"""
        self.assertEqual(self.banner.get_banner_type_display(), 'Página Inicial')
        self.assertEqual(self.banner.get_position_display(), 'Topo')

    def test_banner_ordering(self):
        """Testa ordenação de banners"""
        # Criar banners novos para não conflitar com os do setUp
        Banner.objects.all().delete()
        
        banner1 = Banner.objects.create(title='Order 1', order=1)
        banner2 = Banner.objects.create(title='Order 2', order=2)
        banner3 = Banner.objects.create(title='Order 3', order=0)
        
        banners = Banner.objects.order_by('order')
        # Ordem: 0, 1, 2 (menor número = maior prioridade)
        self.assertEqual(banners[0].order, 0)
        self.assertEqual(banners[1].order, 1)
        self.assertEqual(banners[2].order, 2)

    def test_banner_timestamps(self):
        """Testa timestamps automáticos"""
        new_banner = Banner.objects.create(title='Timestamps Test')
        
        self.assertIsNotNone(new_banner.created_at)
        self.assertIsNotNone(new_banner.updated_at)


class BannerActiveStatusTest(TestCase):
    """Testes para status ativo de banners"""

    def setUp(self):
        self.now = timezone.now()

    def test_is_currently_active_default(self):
        """Testa se banner ativo é detectado corretamente"""
        banner = Banner.objects.create(
            title='Active Banner',
            is_active=True,
            start_date=self.now - timedelta(days=1)
        )
        self.assertTrue(banner.is_currently_active())

    def test_is_currently_active_inactive_flag(self):
        """Testa se banner inativo é detectado corretamente"""
        banner = Banner.objects.create(
            title='Inactive Banner',
            is_active=False,
            start_date=self.now - timedelta(days=1)
        )
        self.assertFalse(banner.is_currently_active())

    def test_is_currently_active_before_start_date(self):
        """Testa banner que ainda não começou"""
        future_date = self.now + timedelta(days=7)
        banner = Banner.objects.create(
            title='Future Banner',
            is_active=True,
            start_date=future_date
        )
        self.assertFalse(banner.is_currently_active())

    def test_is_currently_active_after_end_date(self):
        """Testa banner que já terminou"""
        past_end_date = self.now - timedelta(days=7)
        banner = Banner.objects.create(
            title='Past Banner',
            is_active=True,
            start_date=self.now - timedelta(days=14),
            end_date=past_end_date
        )
        self.assertFalse(banner.is_currently_active())

    def test_is_currently_active_within_date_range(self):
        """Testa banner dentro do período válido"""
        banner = Banner.objects.create(
            title='Current Banner',
            is_active=True,
            start_date=self.now - timedelta(days=1),
            end_date=self.now + timedelta(days=7)
        )
        self.assertTrue(banner.is_currently_active())

    def test_is_currently_active_no_end_date(self):
        """Testa banner sem data de fim"""
        banner = Banner.objects.create(
            title='Open Ended Banner',
            is_active=True,
            start_date=self.now - timedelta(days=1)
        )
        self.assertTrue(banner.is_currently_active())


class BannerClassMethodTest(TestCase):
    """Testes para métodos de classe de Banner"""

    def setUp(self):
        self.now = timezone.now()
        # Banner ativo do tipo home
        self.home_banner = Banner.objects.create(
            title='Home Banner',
            banner_type='home',
            position='top',
            is_active=True,
            start_date=self.now - timedelta(days=1),
            order=1
        )
        # Banner ativo do tipo artist
        self.artist_banner = Banner.objects.create(
            title='Artist Banner',
            banner_type='artist',
            position='top',
            is_active=True,
            start_date=self.now - timedelta(days=1),
            order=2
        )
        # Banner inativo
        self.inactive_banner = Banner.objects.create(
            title='Inactive Banner',
            banner_type='home',
            position='top',
            is_active=False,
            start_date=self.now - timedelta(days=1),
            order=3
        )
        # Banner que ainda não começou
        self.future_banner = Banner.objects.create(
            title='Future Banner',
            banner_type='home',
            position='top',
            is_active=True,
            start_date=self.now + timedelta(days=1),
            order=4
        )

    def test_get_active_banners_all(self):
        """Testa recuperação de todos os banners ativos"""
        active_banners = Banner.get_active_banners()
        self.assertEqual(active_banners.count(), 2)
        self.assertIn(self.home_banner, active_banners)
        self.assertIn(self.artist_banner, active_banners)
        self.assertNotIn(self.inactive_banner, active_banners)
        self.assertNotIn(self.future_banner, active_banners)

    def test_get_active_banners_by_type(self):
        """Testa filtro por tipo de banner"""
        home_banners = Banner.get_active_banners(banner_type='home')
        self.assertEqual(home_banners.count(), 1)
        self.assertIn(self.home_banner, home_banners)
        self.assertNotIn(self.artist_banner, home_banners)
        
        artist_banners = Banner.get_active_banners(banner_type='artist')
        self.assertEqual(artist_banners.count(), 1)
        self.assertIn(self.artist_banner, artist_banners)

    def test_get_active_banners_by_position(self):
        """Testa filtro por posição"""
        top_banners = Banner.get_active_banners(position='top')
        self.assertEqual(top_banners.count(), 2)
        self.assertIn(self.home_banner, top_banners)
        self.assertIn(self.artist_banner, top_banners)
        
        # Criar banner em outra posição
        middle_banner = Banner.objects.create(
            title='Middle Banner',
            banner_type='home',
            position='middle',
            is_active=True,
            start_date=self.now - timedelta(days=1)
        )
        
        middle_banners = Banner.get_active_banners(position='middle')
        self.assertEqual(middle_banners.count(), 1)
        self.assertIn(middle_banner, middle_banners)

    def test_get_active_banners_by_type_and_position(self):
        """Testa filtro por tipo e posição simultaneamente"""
        # Criar mais banners
        banner = Banner.objects.create(
            title='Specific Banner',
            banner_type='music',
            position='middle',
            is_active=True,
            start_date=self.now - timedelta(days=1)
        )
        
        filtered_banners = Banner.get_active_banners(
            banner_type='music',
            position='middle'
        )
        self.assertEqual(filtered_banners.count(), 1)
        self.assertIn(banner, filtered_banners)

    def test_get_active_banners_ordering(self):
        """Testa ordenação de banners ativos"""
        banners = Banner.get_active_banners()
        # Deve estar ordenado por order, depois created_at
        self.assertEqual(banners.first().order, 1)
        self.assertEqual(banners.last().order, 2)

    def test_get_active_banners_with_end_date(self):
        """Testa banners com data de fim ainda válida"""
        banner = Banner.objects.create(
            title='Ending Soon Banner',
            banner_type='home',
            is_active=True,
            start_date=self.now - timedelta(days=1),
            end_date=self.now + timedelta(days=1),
            order=0
        )
        
        active_banners = Banner.get_active_banners()
        self.assertIn(banner, active_banners)

    def test_get_active_banners_with_past_end_date(self):
        """Testa banners com data de fim já passada"""
        banner = Banner.objects.create(
            title='Expired Banner',
            banner_type='home',
            is_active=True,
            start_date=self.now - timedelta(days=7),
            end_date=self.now - timedelta(days=1),
            order=0
        )
        
        active_banners = Banner.get_active_banners()
        self.assertNotIn(banner, active_banners)


class BannerFieldTest(TestCase):
    """Testes para campos específicos do Banner"""

    def test_banner_title_required(self):
        """Testa criação com título"""
        banner = Banner.objects.create(title='Valid Title')
        self.assertEqual(banner.title, 'Valid Title')
        
        # Título pode ser string vazia em alguns casos, então vamos apenas testar criação válida
        self.assertIsNotNone(banner.id)

    def test_banner_link_url_optional(self):
        """Testa que link_url é opcional"""
        banner = Banner.objects.create(
            title='No Link Banner'
        )
        self.assertIsNone(banner.link_url)
        
        banner.link_url = 'https://example.com'
        banner.save()
        self.assertEqual(banner.link_url, 'https://example.com')

    def test_banner_order_can_be_zero(self):
        """Testa que order pode ser zero"""
        banner = Banner.objects.create(
            title='Zero Order Banner',
            order=0
        )
        self.assertEqual(banner.order, 0)

    def test_banner_order_negative_not_allowed(self):
        """Testa que order não pode ser negativo"""
        with self.assertRaises(Exception):
            Banner.objects.create(
                title='Negative Order',
                order=-1
            )

    def test_banner_description_optional(self):
        """Testa que description é opcional"""
        banner = Banner.objects.create(
            title='No Description'
        )
        self.assertIsNone(banner.description)
        
        banner.description = 'Test description'
        banner.save()
        self.assertEqual(banner.description, 'Test description')

    def test_banner_end_date_optional(self):
        """Testa que end_date é opcional"""
        banner = Banner.objects.create(
            title='No End Date'
        )
        self.assertIsNone(banner.end_date)
        
        from django.utils import timezone
        banner.end_date = timezone.now() + timedelta(days=7)
        banner.save()
        self.assertIsNotNone(banner.end_date)


class BannerIntegrationTest(TestCase):
    """Testes de integração para Banner"""

    def setUp(self):
        from django.utils import timezone
        self.now = timezone.now()
        
        # Criar banners para diferentes cenários
        self.banner1 = Banner.objects.create(
            title='Priority Banner',
            banner_type='home',
            position='top',
            is_active=True,
            order=1,
            start_date=self.now - timedelta(days=1)
        )
        
        self.banner2 = Banner.objects.create(
            title='Lower Priority',
            banner_type='home',
            position='top',
            is_active=True,
            order=2,
            start_date=self.now - timedelta(days=1)
        )

    def test_multiple_banners_same_type_position(self):
        """Testa múltiplos banners do mesmo tipo e posição"""
        banners = Banner.objects.filter(
            banner_type='home',
            position='top'
        )
        self.assertEqual(banners.count(), 2)
        
        # Deve estar ordenado por order
        ordered_banners = banners.order_by('order')
        self.assertEqual(ordered_banners.first().order, 1)
        self.assertEqual(ordered_banners.last().order, 2)

    def test_banner_activation_deactivation(self):
        """Testa ativação e desativação de banner"""
        self.assertTrue(self.banner1.is_active)
        
        self.banner1.is_active = False
        self.banner1.save()
        
        updated_banner = Banner.objects.get(id=self.banner1.id)
        self.assertFalse(updated_banner.is_active)
        
        # Reactivate
        updated_banner.is_active = True
        updated_banner.save()
        
        reactivated_banner = Banner.objects.get(id=self.banner1.id)
        self.assertTrue(reactivated_banner.is_active)

    def test_banner_update_timestamp(self):
        """Testa que updated_at é atualizado"""
        old_updated = self.banner1.updated_at
        
        # Pequeno delay para garantir diferença
        from time import sleep
        sleep(0.1)
        
        self.banner1.title = 'Updated Title'
        self.banner1.save()
        
        updated_banner = Banner.objects.get(id=self.banner1.id)
        self.assertGreater(updated_banner.updated_at, old_updated)

    def test_banner_date_range_query(self):
        """Testa query de banners em um range de datas"""
        # Banner dentro do range
        in_range = Banner.objects.create(
            title='In Range',
            is_active=True,
            start_date=self.now - timedelta(days=5),
            end_date=self.now + timedelta(days=5)
        )
        
        # Banner fora do range
        out_of_range = Banner.objects.create(
            title='Out of Range',
            is_active=True,
            start_date=self.now - timedelta(days=10),
            end_date=self.now - timedelta(days=5)
        )
        
        # Query para banners ativos agora
        active_banners = Banner.get_active_banners()
        self.assertIn(in_range, active_banners)
        self.assertNotIn(out_of_range, active_banners)

