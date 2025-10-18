from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
# from rest_framework.authtoken.models import Token
from apps.artists.models import Artist
from apps.music.models import Music

User = get_user_model()


class MusicAPITest(APITestCase):
    """Testes para a API de músicas"""
    
    def setUp(self):
        """Configuração inicial"""
        self.client = APIClient()
        
        # Criar usuário artista
        self.artist_user = User.objects.create_user(
            username='artistuser',
            email='artist@example.com',
            password='pass123',
            user_type='artist'
        )
        
        # Criar artista
        self.artist = Artist.objects.create(
            user=self.artist_user,
            stage_name='Test Artist',
            genre='Rock',
            verified=True
        )
        
        # Criar músicas
        self.music1 = Music.objects.create(
            artist=self.artist,
            title='Song 1',
            album='Album 1',
            genre='Rock',
            duration=240,
            lyrics='Lyrics for song 1',
            streams_count=1000,
            downloads_count=100,
            likes_count=50,
            is_featured=True
        )
        
        self.music2 = Music.objects.create(
            artist=self.artist,
            title='Song 2',
            album='Album 1',
            genre='Rock',
            duration=180,
            lyrics='Lyrics for song 2',
            streams_count=2000,
            downloads_count=200,
            likes_count=100,
            is_featured=False
        )
        
        # Criar usuário comum para testes
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='pass123',
            user_type='listener'
        )
        
    def tearDown(self):
        """Limpeza após cada teste"""
        # Limpar todos os dados criados
        Music.objects.all().delete()
        Artist.objects.all().delete()
        User.objects.all().delete()
    
    def test_music_list(self):
        """Testa listagem de músicas"""
        url = '/api/music/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_music_detail(self):
        """Testa detalhes da música"""
        url = f'/api/music/{self.music1.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Song 1')
        self.assertEqual(response.data['artist_name'], 'Test Artist')
        self.assertEqual(response.data['streams_count'], 1000)
        self.assertEqual(response.data['is_featured'], True)
    
    def test_music_create(self):
        """Testa criação de música"""
        url = '/api/music/create/'
        self.client.force_authenticate(user=self.artist_user)
        
        music_data = {
            'title': 'New Song',
            'album': 'New Album',
            'genre': 'Pop',
            'duration': 200,
            'lyrics': 'New song lyrics'
        }
        
        response = self.client.post(url, music_data, format='json')
        
        # Como o campo file é obrigatório, deve retornar erro
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('file', response.data)
    
    def test_music_stream(self):
        """Testa contagem de stream"""
        url = f'/api/music/{self.music1.id}/stream/'
        self.client.force_authenticate(user=self.user)
        
        initial_streams = self.music1.streams_count
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('streams_count', response.data)
        
        # Verificar se o contador foi incrementado
        self.music1.refresh_from_db()
        self.assertEqual(self.music1.streams_count, initial_streams + 1)
    
    def test_music_download(self):
        """Testa contagem de download"""
        url = f'/api/music/{self.music1.id}/download/'
        self.client.force_authenticate(user=self.user)
        
        initial_downloads = self.music1.downloads_count
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('downloads_count', response.data)
        
        # Verificar se o contador foi incrementado
        self.music1.refresh_from_db()
        self.assertEqual(self.music1.downloads_count, initial_downloads + 1)
    
    def test_music_like(self):
        """Testa curtir música"""
        url = f'/api/music/{self.music1.id}/like/'
        self.client.force_authenticate(user=self.user)
        
        initial_likes = self.music1.likes_count
        like_data = {'action': 'like'}
        response = self.client.post(url, like_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('likes_count', response.data)
        
        # Verificar se o contador foi incrementado
        self.music1.refresh_from_db()
        self.assertEqual(self.music1.likes_count, initial_likes + 1)
    
    def test_music_unlike(self):
        """Testa descurtir música"""
        url = f'/api/music/{self.music1.id}/like/'
        self.client.force_authenticate(user=self.user)
        
        initial_likes = self.music1.likes_count
        unlike_data = {'action': 'unlike'}
        response = self.client.post(url, unlike_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('likes_count', response.data)
        
        # Verificar se o contador foi decrementado
        self.music1.refresh_from_db()
        self.assertEqual(self.music1.likes_count, initial_likes - 1)
    
    def test_music_stats(self):
        """Testa estatísticas da música"""
        url = f'/api/music/{self.music1.id}/stats/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('streams_count', response.data)
        self.assertIn('downloads_count', response.data)
        self.assertIn('likes_count', response.data)
        self.assertEqual(response.data['streams_count'], 1000)
    
    def test_trending_music(self):
        """Testa músicas em alta"""
        url = '/api/music/trending/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('musics', response.data)
        self.assertIn('count', response.data)
        # Verificar que há pelo menos 2 músicas (criadas no setUp)
        self.assertGreaterEqual(response.data['count'], 2)
    
    def test_popular_music(self):
        """Testa músicas populares"""
        url = '/api/music/popular/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('musics', response.data)
        self.assertIn('count', response.data)
        self.assertEqual(response.data['count'], 2)
    
    def test_featured_music(self):
        """Testa músicas em destaque"""
        url = '/api/music/featured/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('musics', response.data)
        self.assertIn('count', response.data)
        self.assertEqual(response.data['count'], 1)  # Apenas music1 é featured
    
    def test_music_genres(self):
        """Testa lista de gêneros"""
        url = '/api/music/genres/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('genres', response.data)
        self.assertIn('count', response.data)
        self.assertIn('Rock', response.data['genres'])
    
    def test_music_albums(self):
        """Testa lista de álbuns"""
        url = '/api/music/albums/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('albums', response.data)
        self.assertIn('count', response.data)
        self.assertIn('Album 1', response.data['albums'])
    
    def test_music_list_with_filters(self):
        """Testa listagem com filtros"""
        url = '/api/music/'
        
        # Teste com filtro de artista
        response = self.client.get(url, {'artist': self.artist.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        
        # Teste com filtro de gênero
        response = self.client.get(url, {'genre': 'Rock'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        
        # Teste com filtro de álbum
        response = self.client.get(url, {'album': 'Album 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        
        # Teste com filtro de destaque
        response = self.client.get(url, {'featured': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        
        # Teste com busca
        response = self.client.get(url, {'search': 'Song 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_music_list_pagination(self):
        """Testa paginação na listagem"""
        url = '/api/music/'
        response = self.client.get(url, {'page_size': 1})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
    
    def test_music_create_invalid_data(self):
        """Testa criação de música com dados inválidos"""
        url = '/api/music/create/'
        self.client.force_authenticate(user=self.artist_user)
        
        invalid_data = {
            'title': '',  # Título vazio
            'duration': 0  # Duração inválida
        }
        
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
        self.assertIn('file', response.data)
    
    def test_music_not_found(self):
        """Testa música não encontrada"""
        url = '/api/music/999/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_music_unauthorized_actions(self):
        """Testa ações que requerem autenticação"""
        url = f'/api/music/{self.music1.id}/stream/'
        
        # Sem autenticação
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
