from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from apps.users.models import User
from apps.artists.models import Artist
from apps.music.models import Music
from apps.constants import GENRE_CHOICES

User = get_user_model()


class GenreChoicesTest(TestCase):
    """Testes para verificar se os gêneros musicais estão funcionando como select"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.client = Client()
        
        # Criar superusuário
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        # Criar usuário artista
        self.artist_user = User.objects.create_user(
            username='artistuser',
            email='artist@example.com',
            password='testpass123',
            user_type='artist'
        )
        
        # Criar perfil de artista
        self.artist = Artist.objects.create(
            user=self.artist_user,
            stage_name='Test Artist',
            real_name='Test Artist Real',
            bio='Test bio',
            genre='sertanejo',  # Usar gênero válido
            location='Test City'
        )
    
    def test_genre_choices_available(self):
        """Testa se as opções de gênero estão disponíveis"""
        self.client.login(username='admin', password='adminpass123')
        
        # Testar página de criação de artista
        response = self.client.get('/admin/artists/artist/add/')
        self.assertEqual(response.status_code, 200)
        
        # Verificar se as opções de gênero estão presentes
        for value, label in GENRE_CHOICES:
            if value:  # Pular opção vazia
                self.assertContains(response, f'value="{value}"')
                self.assertContains(response, label)
    
    def test_genre_choices_in_music_form(self):
        """Testa se as opções de gênero estão disponíveis no formulário de música"""
        self.client.login(username='admin', password='adminpass123')
        
        # Testar página de criação de música
        response = self.client.get('/admin/music/music/add/')
        self.assertEqual(response.status_code, 200)
        
        # Verificar se as opções de gênero estão presentes
        for value, label in GENRE_CHOICES:
            if value:  # Pular opção vazia
                self.assertContains(response, f'value="{value}"')
                self.assertContains(response, label)
    
    def test_genre_display_in_admin_list(self):
        """Testa se o gênero é exibido corretamente na listagem do admin"""
        self.client.login(username='admin', password='adminpass123')
        
        # Verificar listagem de artistas
        response = self.client.get('/admin/artists/artist/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sertanejo')  # Label do choice
        
        # Criar música para testar
        music = Music.objects.create(
            artist=self.artist,
            title='Test Song',
            album='Test Album',
            genre='funk',  # Usar outro gênero
            duration=180,
            lyrics='Test lyrics'
        )
        
        # Verificar listagem de músicas
        response = self.client.get('/admin/music/music/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Funk')  # Label do choice
    
    def test_genre_validation(self):
        """Testa se a validação de gênero está funcionando"""
        self.client.login(username='admin', password='adminpass123')
        
        # Tentar criar artista com gênero inválido
        data = {
            'user': self.artist_user.id,
            'stage_name': 'Test Artist 2',
            'genre': 'genero_invalido',  # Gênero que não está nas opções
        }
        
        response = self.client.post('/admin/artists/artist/add/', data)
        # Deve retornar erro de validação
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Select a valid choice')
    
    def test_genre_filter_in_admin(self):
        """Testa se o filtro por gênero está funcionando"""
        self.client.login(username='admin', password='adminpass123')
        
        # Criar música com gênero específico
        music = Music.objects.create(
            artist=self.artist,
            title='Sertanejo Song',
            album='Sertanejo Album',
            genre='sertanejo',
            duration=180,
            lyrics='Sertanejo lyrics'
        )
        
        # Filtrar por gênero sertanejo
        response = self.client.get('/admin/music/music/', {'genre__exact': 'sertanejo'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sertanejo Song')
        
        # Filtrar por gênero diferente
        response = self.client.get('/admin/music/music/', {'genre__exact': 'rock'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Sertanejo Song')
    
    def test_genre_choices_completeness(self):
        """Testa se todas as opções de gênero estão implementadas"""
        # Verificar se temos os gêneros principais do Brasil
        expected_genres = ['sertanejo', 'funk', 'pop', 'rock', 'mpb', 'forro', 'pagode', 'samba']
        
        for genre in expected_genres:
            # Verificar se o gênero está nas opções
            genre_values = [choice[0] for choice in GENRE_CHOICES]
            self.assertIn(genre, genre_values, f"Gênero '{genre}' não encontrado nas opções")
    
    def test_genre_labels_in_portuguese(self):
        """Testa se os labels dos gêneros estão em português"""
        # Verificar alguns labels importantes
        genre_labels = dict(GENRE_CHOICES)
        
        self.assertEqual(genre_labels['sertanejo'], 'Sertanejo')
        self.assertEqual(genre_labels['funk'], 'Funk')
        self.assertEqual(genre_labels['pop'], 'Pop')
        self.assertEqual(genre_labels['rock'], 'Rock')
        self.assertEqual(genre_labels['mpb'], 'MPB')
        self.assertEqual(genre_labels['forro'], 'Forró')
        self.assertEqual(genre_labels['pagode'], 'Pagode')
        self.assertEqual(genre_labels['samba'], 'Samba')
