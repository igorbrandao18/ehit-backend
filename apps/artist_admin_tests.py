from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from apps.users.models import User
from apps.artists.models import Artist
from apps.music.models import Music

User = get_user_model()


class ArtistAdminViewsTest(TestCase):
    """Testes para as views administrativas do artista"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.client = Client()
        
        # Criar usuário comum
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            user_type='listener'
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
            genre='Rock',
            location='Test City'
        )
        
        # Criar algumas músicas para o artista
        self.music1 = Music.objects.create(
            artist=self.artist,
            title='Song 1',
            album='Album 1',
            genre='Rock',
            duration=180,
            lyrics='Test lyrics 1'
        )
        
        self.music2 = Music.objects.create(
            artist=self.artist,
            title='Song 2',
            album='Album 1',
            genre='Rock',
            duration=200,
            lyrics='Test lyrics 2'
        )
    
    def test_artist_dashboard_access_authenticated(self):
        """Testa acesso ao dashboard do artista autenticado"""
        self.client.login(username='artistuser', password='testpass123')
        response = self.client.get('/artist/dashboard/')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Artist')
        self.assertContains(response, 'Song 1')
        self.assertContains(response, 'Song 2')
    
    def test_artist_dashboard_access_unauthenticated(self):
        """Testa acesso ao dashboard sem autenticação"""
        response = self.client.get('/artist/dashboard/')
        
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_artist_dashboard_access_non_artist(self):
        """Testa acesso ao dashboard por usuário não-artista"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/artist/dashboard/')
        
        self.assertEqual(response.status_code, 302)  # Redirect to home
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('Você precisa ser um artista', str(messages[0]))
    
    def test_artist_music_list(self):
        """Testa listagem de músicas do artista"""
        self.client.login(username='artistuser', password='testpass123')
        response = self.client.get('/artist/music/')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Song 1')
        self.assertContains(response, 'Song 2')
        self.assertContains(response, 'Album 1')
    
    def test_artist_music_list_with_search(self):
        """Testa busca de músicas"""
        self.client.login(username='artistuser', password='testpass123')
        response = self.client.get('/artist/music/', {'search': 'Song 1'})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Song 1')
        self.assertNotContains(response, 'Song 2')
    
    def test_artist_music_list_with_album_filter(self):
        """Testa filtro por álbum"""
        self.client.login(username='artistuser', password='testpass123')
        response = self.client.get('/artist/music/', {'album': 'Album 1'})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Song 1')
        self.assertContains(response, 'Song 2')
    
    def test_artist_music_create_get(self):
        """Testa acesso ao formulário de criação de música"""
        self.client.login(username='artistuser', password='testpass123')
        response = self.client.get('/artist/music/create/')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Criar Nova Música')
    
    def test_artist_music_create_post_valid(self):
        """Testa criação de música com dados válidos"""
        self.client.login(username='artistuser', password='testpass123')
        
        data = {
            'title': 'New Song',
            'album': 'New Album',
            'genre': 'Pop',
            'duration': '240',
            'lyrics': 'New song lyrics'
        }
        
        response = self.client.post('/artist/music/create/', data)
        
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Music.objects.filter(title='New Song').exists())
        
        # Verificar se a música foi associada ao artista correto
        new_music = Music.objects.get(title='New Song')
        self.assertEqual(new_music.artist, self.artist)
    
    def test_artist_music_create_post_invalid(self):
        """Testa criação de música com dados inválidos"""
        self.client.login(username='artistuser', password='testpass123')
        
        data = {
            'title': '',  # Título vazio
            'album': 'New Album',
            'genre': 'Pop',
            'duration': '240',
            'lyrics': 'New song lyrics'
        }
        
        response = self.client.post('/artist/music/create/', data)
        
        self.assertEqual(response.status_code, 200)  # Stay on form
        self.assertContains(response, 'Título é obrigatório')
        self.assertFalse(Music.objects.filter(album='New Album').exists())
    
    def test_artist_music_edit_get(self):
        """Testa acesso ao formulário de edição de música"""
        self.client.login(username='artistuser', password='testpass123')
        response = self.client.get(f'/artist/music/{self.music1.id}/edit/')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Song 1')
    
    def test_artist_music_edit_post(self):
        """Testa edição de música"""
        self.client.login(username='artistuser', password='testpass123')
        
        data = {
            'title': 'Updated Song',
            'album': 'Updated Album',
            'genre': 'Jazz',
            'duration': '300',
            'lyrics': 'Updated lyrics'
        }
        
        response = self.client.post(f'/artist/music/{self.music1.id}/edit/', data)
        
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Verificar se a música foi atualizada
        updated_music = Music.objects.get(id=self.music1.id)
        self.assertEqual(updated_music.title, 'Updated Song')
        self.assertEqual(updated_music.album, 'Updated Album')
        self.assertEqual(updated_music.genre, 'Jazz')
    
    def test_artist_music_delete_get(self):
        """Testa acesso à página de confirmação de exclusão"""
        self.client.login(username='artistuser', password='testpass123')
        response = self.client.get(f'/artist/music/{self.music1.id}/delete/')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Song 1')
        self.assertContains(response, 'Tem certeza')
    
    def test_artist_music_delete_post(self):
        """Testa exclusão de música (soft delete)"""
        self.client.login(username='artistuser', password='testpass123')
        
        response = self.client.post(f'/artist/music/{self.music1.id}/delete/')
        
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Verificar se a música foi marcada como inativa
        deleted_music = Music.objects.get(id=self.music1.id)
        self.assertFalse(deleted_music.is_active)
    
    def test_artist_albums_view(self):
        """Testa visualização de álbuns"""
        self.client.login(username='artistuser', password='testpass123')
        response = self.client.get('/artist/albums/')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Album 1')
        self.assertContains(response, 'Song 1')
        self.assertContains(response, 'Song 2')
    
    def test_artist_stats_view(self):
        """Testa visualização de estatísticas"""
        self.client.login(username='artistuser', password='testpass123')
        response = self.client.get('/artist/stats/')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Artist')
        self.assertContains(response, 'Song 1')
        self.assertContains(response, 'Song 2')
    
    def test_artist_cannot_access_other_artist_music(self):
        """Testa que artista não pode acessar músicas de outros artistas"""
        # Criar outro artista
        other_artist_user = User.objects.create_user(
            username='otherartist',
            email='other@example.com',
            password='testpass123',
            user_type='artist'
        )
        
        other_artist = Artist.objects.create(
            user=other_artist_user,
            stage_name='Other Artist',
            real_name='Other Artist Real',
            bio='Other bio',
            genre='Pop',
            location='Other City'
        )
        
        self.client.login(username='otherartist', password='testpass123')
        
        # Tentar acessar música do primeiro artista
        response = self.client.get(f'/artist/music/{self.music1.id}/edit/')
        
        self.assertEqual(response.status_code, 404)  # Not found
    
    def test_artist_dashboard_statistics(self):
        """Testa estatísticas no dashboard"""
        self.client.login(username='artistuser', password='testpass123')
        response = self.client.get('/artist/dashboard/')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2')  # Total de músicas
        self.assertContains(response, 'Song 1')  # Música recente
        self.assertContains(response, 'Song 2')  # Música recente
