from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
# from rest_framework.authtoken.models import Token
from apps.artists.models import Artist
from apps.music.models import Music

User = get_user_model()


class ArtistsAPITest(APITestCase):
    """Testes para a API de artistas"""
    
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
            real_name='Test Artist Real',
            bio='Test artist bio',
            genre='Rock',
            location='Test City',
            verified=True,
            followers_count=1000,
            monthly_listeners=5000
        )
        
        # Criar token para autenticação
        # self.token = Token.objects.create(user=self.artist_user)
        
        # Criar músicas para o artista
        self.music1 = Music.objects.create(
            artist=self.artist,
            title='Song 1',
            duration=240,
            streams_count=1000,
            downloads_count=100,
            likes_count=50
        )
        
        self.music2 = Music.objects.create(
            artist=self.artist,
            title='Song 2',
            duration=180,
            streams_count=2000,
            downloads_count=200,
            likes_count=100
        )
    
    def test_artist_list(self):
        """Testa listagem de artistas"""
        url = '/api/artists/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['stage_name'], 'Test Artist')
    
    def test_artist_detail(self):
        """Testa detalhes do artista"""
        url = f'/api/artists/{self.artist.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stage_name'], 'Test Artist')
        self.assertEqual(response.data['verified'], True)
        self.assertEqual(response.data['followers_count'], 1000)
    
    def test_artist_create(self):
        """Testa criação de artista"""
        url = '/api/artists/create/'
        self.client.force_authenticate(user=self.artist_user)
        
        artist_data = {
            'stage_name': 'New Artist',
            'real_name': 'New Artist Real',
            'bio': 'New artist bio',
            'genre': 'Pop',
            'location': 'New City'
        }
        
        response = self.client.post(url, artist_data, format='json')
        
        # Como o usuário já tem um artista, deve retornar erro
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Verificar se há erro de validação
        has_error = False
        if isinstance(response.data, dict):
            has_error = (
                'non_field_errors' in response.data or 
                'error' in response.data or 
                any('artista' in str(v) for v in response.data.values() if isinstance(v, list))
            )
        elif isinstance(response.data, list):
            has_error = any('artista' in str(item) for item in response.data)
        
        self.assertTrue(has_error, f"Response data: {response.data}")
    
    def test_artist_stats(self):
        """Testa estatísticas do artista"""
        url = f'/api/artists/{self.artist.id}/stats/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_streams', response.data)
        self.assertIn('total_downloads', response.data)
        self.assertIn('total_likes', response.data)
        self.assertIn('musics_count', response.data)
        
        # Verificar valores corretos
        self.assertEqual(response.data['total_streams'], 3000)  # 1000 + 2000
        self.assertEqual(response.data['total_downloads'], 300)  # 100 + 200
        self.assertEqual(response.data['total_likes'], 150)  # 50 + 100
        self.assertEqual(response.data['musics_count'], 2)
    
    def test_artist_musics(self):
        """Testa músicas do artista"""
        url = f'/api/artists/{self.artist.id}/musics/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('musics', response.data)
        self.assertIn('count', response.data)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['musics']), 2)
    
    def test_artist_follow(self):
        """Testa seguir artista"""
        url = f'/api/artists/{self.artist.id}/follow/'
        self.client.force_authenticate(user=self.artist_user)
        
        follow_data = {'action': 'follow'}
        response = self.client.post(url, follow_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('followers_count', response.data)
    
    def test_artist_unfollow(self):
        """Testa deixar de seguir artista"""
        url = f'/api/artists/{self.artist.id}/follow/'
        self.client.force_authenticate(user=self.artist_user)
        
        unfollow_data = {'action': 'unfollow'}
        response = self.client.post(url, unfollow_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('followers_count', response.data)
    
    def test_popular_artists(self):
        """Testa artistas populares"""
        url = '/api/artists/popular/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('artists', response.data)
        self.assertIn('count', response.data)
        self.assertEqual(response.data['count'], 1)
    
    def test_trending_artists(self):
        """Testa artistas em alta"""
        url = '/api/artists/trending/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('artists', response.data)
        self.assertIn('count', response.data)
    
    def test_artists_genres(self):
        """Testa lista de gêneros"""
        url = '/api/artists/genres/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('genres', response.data)
        self.assertIn('count', response.data)
        self.assertIn('Rock', response.data['genres'])
    
    def test_artist_list_with_filters(self):
        """Testa listagem com filtros"""
        url = '/api/artists/'
        
        # Teste com filtro de gênero
        response = self.client.get(url, {'genre': 'Rock'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        
        # Teste com filtro de verificação
        response = self.client.get(url, {'verified': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        
        # Teste com busca
        response = self.client.get(url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_artist_list_pagination(self):
        """Testa paginação na listagem"""
        url = '/api/artists/'
        response = self.client.get(url, {'page_size': 1})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
    
    def test_artist_create_invalid_data(self):
        """Testa criação de artista com dados inválidos"""
        url = '/api/artists/create/'
        self.client.force_authenticate(user=self.artist_user)
        
        invalid_data = {
            'stage_name': '',  # Nome vazio
            'genre': 'Rock'
        }
        
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('stage_name', response.data)
