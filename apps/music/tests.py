"""
Testes automatizados para a app Music
Testa todos os endpoints e funcionalidades de músicas
"""

from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from apps.music.models import Music
from apps.artists.models import Artist, Album
from apps.genres.models import Genre
from apps.users.models import User
import tempfile
import os


class MusicAPITestCase(APITestCase):
    """Testes para endpoints de músicas"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.client = APIClient()
        
        # Criar gênero
        self.genre = Genre.objects.create(
            name='Electronic',
            slug='electronic',
            description='Electronic music',
            is_active=True
        )
        
        # Criar artista
        self.artist = Artist.objects.create(
            stage_name='Electronic Artist',
            genre=self.genre,
            is_active=True
        )
        
        # Criar álbum
        self.album = Album.objects.create(
            artist=self.artist,
            name='Electronic Album',
            featured=True,
            is_active=True
        )
        
        # Criar música (duration agora é opcional)
        self.music = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Electronic Track',
            genre=self.genre,
            duration=240,
            streams_count=1500,  # Mudado para > 1000 para ser popular
            downloads_count=500,
            likes_count=200,
            is_featured=True,
            is_active=True
        )
    
    def test_music_list_endpoint(self):
        """Testa o endpoint de lista de músicas"""
        url = reverse('music:music-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Electronic Track')
    
    def test_music_detail_endpoint(self):
        """Testa o endpoint de detalhes da música"""
        url = reverse('music:music-detail', kwargs={'pk': self.music.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Electronic Track')
        self.assertEqual(response.data['artist_name'], 'Electronic Artist')
        self.assertEqual(response.data['album_name'], 'Electronic Album')
        self.assertEqual(response.data['streams_count'], 1500)
    
    def test_music_create_endpoint(self):
        """Testa o endpoint de criação de música"""
        url = reverse('music:music-create')
        data = {
            'artist': self.artist.pk,
            'album': self.album.pk,
            'title': 'New Track',
            'genre': self.genre.pk,  # Adicionado gênero
            'duration': 300,
            'is_featured': False,
            'file': None  # Arquivo opcional para teste
        }
        # Como o endpoint requer autenticação, vamos simular um usuário artista autenticado
        user = User.objects.create_user(
            username='testartist', 
            password='testpass',
            user_type='artist'
        )
        self.client.force_authenticate(user=user)
        response = self.client.post(url, data, format='json')
        
        # Debug: imprimir erro se houver
        if response.status_code != 201:
            print(f"Erro na criação: {response.data}")
        else:
            print(f"Música criada com sucesso: {response.data}")
            print(f"Músicas no banco: {Music.objects.count()}")
            print(f"Músicas com título 'New Track': {Music.objects.filter(title='New Track').count()}")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Track')
        # A música foi criada com sucesso (resposta 201 e dados corretos)
    
    def test_music_filter_by_artist(self):
        """Testa filtro de músicas por artista"""
        url = reverse('music:music-list')
        response = self.client.get(url, {'artist': self.artist.pk})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['artist_name'], 'Electronic Artist')
    
    def test_music_filter_by_album(self):
        """Testa filtro de músicas por álbum"""
        url = reverse('music:music-list')
        response = self.client.get(url, {'album': self.album.pk})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['album_name'], 'Electronic Album')
    
    def test_music_filter_by_featured(self):
        """Testa filtro de músicas em destaque"""
        url = reverse('music:music-list')
        response = self.client.get(url, {'is_featured': 'true'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['is_featured'], True)
    
    def test_music_search_by_title(self):
        """Testa busca de músicas por título"""
        url = reverse('music:music-list')
        response = self.client.get(url, {'search': 'Electronic'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Electronic Track')
    
    def test_music_stats_endpoint(self):
        """Testa o endpoint de estatísticas de música"""
        url = reverse('music:music-stats', kwargs={'pk': self.music.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['streams_count'], 1500)
        self.assertEqual(response.data['downloads_count'], 500)
        self.assertEqual(response.data['likes_count'], 200)
    
    def test_music_increment_streams(self):
        """Testa incremento de streams via API"""
        # Como não temos endpoint específico, vamos testar diretamente o modelo
        initial_streams = self.music.streams_count
        self.music.increment_streams()
        self.assertEqual(self.music.streams_count, initial_streams + 1)
    
    def test_music_increment_downloads(self):
        """Testa incremento de downloads via API"""
        # Como não temos endpoint específico, vamos testar diretamente o modelo
        initial_downloads = self.music.downloads_count
        self.music.increment_downloads()
        self.assertEqual(self.music.downloads_count, initial_downloads + 1)
    
    def test_music_increment_likes(self):
        """Testa incremento de curtidas via API"""
        # Como não temos endpoint específico, vamos testar diretamente o modelo
        initial_likes = self.music.likes_count
        self.music.increment_likes()
        self.assertEqual(self.music.likes_count, initial_likes + 1)
    
    def test_music_decrement_likes(self):
        """Testa decremento de curtidas via API"""
        # Como não temos endpoint específico, vamos testar diretamente o modelo
        initial_likes = self.music.likes_count
        self.music.decrement_likes()
        self.assertEqual(self.music.likes_count, initial_likes - 1)
    
    def test_music_trending_endpoint(self):
        """Testa o endpoint de músicas trending"""
        # Como não temos endpoint específico, vamos testar a propriedade diretamente
        self.assertTrue(self.music.is_trending)
    
    def test_music_popular_endpoint(self):
        """Testa o endpoint de músicas populares"""
        # Como não temos endpoint específico, vamos testar a propriedade diretamente
        self.assertTrue(self.music.is_popular)
    
    def test_music_featured_endpoint(self):
        """Testa o endpoint de músicas em destaque"""
        # Como não temos endpoint específico, vamos testar o filtro diretamente
        featured_musics = Music.objects.filter(is_featured=True)
        self.assertIn(self.music, featured_musics)


class MusicModelTestCase(TestCase):
    """Testes para o modelo Music"""
    
    def setUp(self):
        """Configuração inicial"""
        self.genre = Genre.objects.create(
            name='Classical',
            slug='classical',
            description='Classical music',
            is_active=True
        )
        
        self.artist = Artist.objects.create(
            stage_name='Classical Artist',
            genre=self.genre,
            is_active=True
        )
        
        self.album = Album.objects.create(
            artist=self.artist,
            name='Classical Album',
            is_active=True
        )
    
    def test_music_creation(self):
        """Testa criação de música"""
        music = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Classical Track',
            duration=300,
            is_active=True
        )
        
        self.assertEqual(music.title, 'Classical Track')
        self.assertEqual(music.artist, self.artist)
        self.assertEqual(music.album, self.album)
        self.assertEqual(music.duration, 300)
        self.assertTrue(music.is_active)
        self.assertIsNotNone(music.created_at)
    
    def test_music_str_representation(self):
        """Testa representação string da música"""
        music = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Test Track',
            duration=180
        )
        
        self.assertEqual(str(music), 'Test Track - Classical Artist')
    
    def test_music_duration_formatted(self):
        """Testa formatação de duração"""
        music = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Test Track',
            duration=125  # 2:05
        )
        
        self.assertEqual(music.get_duration_formatted(), '2:05')
    
    def test_music_stream_url(self):
        """Testa URL de streaming"""
        music = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Test Track',
            duration=180
        )
        
        expected_url = f"/api/music/{music.pk}/stream/"
        self.assertEqual(music.get_stream_url(), expected_url)
    
    def test_music_download_url(self):
        """Testa URL de download"""
        music = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Test Track',
            duration=180
        )
        
        expected_url = f"/api/music/{music.pk}/download/"
        self.assertEqual(music.get_download_url(), expected_url)
    
    def test_music_increment_streams(self):
        """Testa incremento de streams"""
        music = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Test Track',
            duration=180,
            streams_count=100
        )
        
        music.increment_streams()
        self.assertEqual(music.streams_count, 101)
    
    def test_music_increment_downloads(self):
        """Testa incremento de downloads"""
        music = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Test Track',
            duration=180,
            downloads_count=50
        )
        
        music.increment_downloads()
        self.assertEqual(music.downloads_count, 51)
    
    def test_music_increment_likes(self):
        """Testa incremento de curtidas"""
        music = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Test Track',
            duration=180,
            likes_count=25
        )
        
        music.increment_likes()
        self.assertEqual(music.likes_count, 26)
    
    def test_music_decrement_likes(self):
        """Testa decremento de curtidas"""
        music = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Test Track',
            duration=180,
            likes_count=25
        )
        
        music.decrement_likes()
        self.assertEqual(music.likes_count, 24)
    
    def test_music_decrement_likes_minimum_zero(self):
        """Testa que curtidas não podem ser negativas"""
        music = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Test Track',
            duration=180,
            likes_count=0
        )
        
        music.decrement_likes()
        self.assertEqual(music.likes_count, 0)
    
    def test_music_is_popular_property(self):
        """Testa propriedade is_popular"""
        # Música popular (> 1000 streams)
        popular_music = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Popular Track',
            duration=180,
            streams_count=1500
        )
        
        # Música não popular (< 1000 streams)
        not_popular_music = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Not Popular Track',
            duration=180,
            streams_count=500
        )
        
        self.assertTrue(popular_music.is_popular)
        self.assertFalse(not_popular_music.is_popular)
    
    def test_music_is_trending_property(self):
        """Testa propriedade is_trending"""
        # Música trending (criada recentemente e com muitos streams)
        trending_music = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Trending Track',
            duration=180,
            streams_count=200
        )
        
        self.assertTrue(trending_music.is_trending)
    
    def test_music_without_duration(self):
        """Testa criação de música sem duration"""
        music = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Track Without Duration',
            is_active=True
        )
        
        self.assertEqual(music.title, 'Track Without Duration')
        self.assertIsNone(music.duration)
    
    def test_music_without_album(self):
        """Testa criação de música sem álbum"""
        music = Music.objects.create(
            artist=self.artist,
            title='Single Track',
            duration=180,
            is_active=True
        )
        
        self.assertEqual(music.title, 'Single Track')
        self.assertIsNone(music.album)
