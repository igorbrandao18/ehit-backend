"""
Testes automatizados para a app Genres
Testa todos os endpoints e funcionalidades de gêneros
"""

from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from apps.genres.models import Genre
from apps.artists.models import Artist, Album
from apps.music.models import Music


class GenreAPITestCase(APITestCase):
    """Testes para endpoints de gêneros"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.client = APIClient()
        
        # Criar gêneros
        self.genre1 = Genre.objects.create(
            name='Rock',
            slug='rock',
            description='Rock music',
            color='#FF0000',
            icon='🎸',
            is_active=True
        )
        
        self.genre2 = Genre.objects.create(
            name='Pop',
            slug='pop',
            description='Pop music',
            color='#00FF00',
            icon='🎵',
            is_active=True
        )
        
        # Criar artista
        self.artist = Artist.objects.create(
            stage_name='Rock Artist',
            genre=self.genre1,
            is_active=True
        )
        
        # Criar álbum
        self.album = Album.objects.create(
            artist=self.artist,
            name='Rock Album',
            is_active=True
        )
        
        # Criar música
        self.music = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Rock Track',
            duration=180,
            is_active=True
        )
    
    def test_genre_list_endpoint(self):
        """Testa o endpoint de lista de gêneros"""
        url = reverse('genre-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_genre_detail_endpoint(self):
        """Testa o endpoint de detalhes do gênero"""
        url = reverse('genre-detail', kwargs={'pk': self.genre1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Rock')
        self.assertEqual(response.data['slug'], 'rock')
        self.assertEqual(response.data['color'], '#FF0000')
        self.assertEqual(response.data['icon'], '🎸')
    
    def test_genre_create_endpoint(self):
        """Testa o endpoint de criação de gênero"""
        url = reverse('genre-list')
        data = {
            'name': 'Jazz',
            'slug': 'jazz',
            'description': 'Jazz music',
            'color': '#0000FF',
            'icon': '🎷',
            'is_active': True
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Jazz')
        self.assertTrue(Genre.objects.filter(name='Jazz').exists())
    
    def test_genre_search_by_name(self):
        """Testa busca de gêneros por nome"""
        url = reverse('genre-list')
        response = self.client.get(url, {'search': 'Rock'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Rock')
    
    def test_genre_filter_by_active(self):
        """Testa filtro de gêneros por status ativo"""
        # Criar gênero inativo
        inactive_genre = Genre.objects.create(
            name='Inactive Genre',
            slug='inactive',
            description='Inactive genre',
            is_active=False
        )
        
        url = reverse('genre-list')
        response = self.client.get(url, {'is_active': 'true'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Apenas os ativos


class GenreModelTestCase(TestCase):
    """Testes para o modelo Genre"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.parent_genre = Genre.objects.create(
            name='Electronic',
            slug='electronic',
            description='Electronic music',
            color='#00FFFF',
            icon='🎛️',
            is_active=True
        )
        
        self.sub_genre = Genre.objects.create(
            name='Techno',
            slug='techno',
            description='Techno music',
            color='#FF00FF',
            icon='🎧',
            parent=self.parent_genre,
            is_active=True
        )
        
        # Criar artista e música para testes de contagem
        self.artist = Artist.objects.create(
            stage_name='Techno Artist',
            genre=self.sub_genre,
            is_active=True
        )
        
        self.album = Album.objects.create(
            artist=self.artist,
            name='Techno Album',
            is_active=True
        )
        
        self.music1 = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Techno Track 1',
            duration=200,
            genre=self.sub_genre,
            is_active=True
        )
        
        self.music2 = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Techno Track 2',
            duration=180,
            genre=self.sub_genre,
            is_active=True
        )
    
    def test_genre_creation(self):
        """Testa criação de gênero"""
        genre = Genre.objects.create(
            name='Hip Hop',
            slug='hip-hop',
            description='Hip hop music',
            color='#000000',
            icon='🎤',
            is_active=True
        )
        
        self.assertEqual(genre.name, 'Hip Hop')
        self.assertEqual(genre.slug, 'hip-hop')
        self.assertTrue(genre.is_active)
    
    def test_genre_str_representation(self):
        """Testa representação string do gênero"""
        self.assertEqual(str(self.parent_genre), 'Electronic')
        self.assertEqual(str(self.sub_genre), 'Techno')
    
    def test_genre_slug_auto_generation(self):
        """Testa geração automática de slug"""
        genre = Genre.objects.create(
            name='House Music',
            description='House music genre',
            is_active=True
        )
        
        # Slug deve ser gerado automaticamente
        self.assertEqual(genre.slug, 'house-music')
    
    def test_genre_artist_count(self):
        """Testa contagem de artistas do gênero"""
        # O método artist_count deve contar artistas ativos
        self.assertEqual(self.sub_genre.artist_count, 1)
    
    def test_genre_song_count(self):
        """Testa contagem de músicas do gênero"""
        # O método song_count deve contar músicas ativas
        self.assertEqual(self.sub_genre.song_count, 2)