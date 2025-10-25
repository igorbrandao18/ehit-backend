"""
Testes automatizados para a app Artists
Testa todos os endpoints de artistas e álbuns
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from apps.artists.models import Artist, Album
from apps.genres.models import Genre
from apps.music.models import Music
from apps.users.models import User
import json


class ArtistAPITestCase(APITestCase):
    """Testes para endpoints de artistas"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.client = APIClient()
        
        # Criar gênero
        self.genre = Genre.objects.create(
            name='Rock',
            slug='rock',
            description='Rock music',
            is_active=True
        )
        
        # Criar artista
        self.artist = Artist.objects.create(
            stage_name='Test Artist',
            genre=self.genre,
            is_active=True
        )
        
        # Criar álbum
        self.album = Album.objects.create(
            artist=self.artist,
            name='Test Album',
            featured=True,
            is_active=True
        )
        
        # Criar música
        self.music = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Test Music',
            duration=180,
            is_active=True
        )
    
    def test_artist_list_endpoint(self):
        """Testa o endpoint de lista de artistas"""
        url = reverse('artists:artist-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['stage_name'], 'Test Artist')
    
    def test_artist_detail_endpoint(self):
        """Testa o endpoint de detalhes do artista"""
        url = reverse('artists:artist-detail', kwargs={'pk': self.artist.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stage_name'], 'Test Artist')
        self.assertEqual(response.data['genre_data']['name'], 'Rock')
    
    def test_artist_create_endpoint(self):
        """Testa o endpoint de criação de artista"""
        url = reverse('artists:artist-create')
        data = {
            'stage_name': 'New Artist',
            'genre': self.genre.pk,
            'is_active': True
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['stage_name'], 'New Artist')
        self.assertTrue(Artist.objects.filter(stage_name='New Artist').exists())
    
    def test_artist_complete_endpoint(self):
        """Testa o endpoint de artista completo"""
        url = reverse('artists:artist-complete', kwargs={'pk': self.artist.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('artist', response.data)
        self.assertIn('albums', response.data)
        self.assertIn('musics', response.data)
        self.assertEqual(response.data['albums_count'], 1)
        self.assertEqual(response.data['musics_count'], 1)
    
    def test_artist_with_musics_endpoint(self):
        """Testa o endpoint de artista com músicas"""
        url = reverse('artists:artist-with-musics', kwargs={'pk': self.artist.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('artist', response.data)
        self.assertIn('musics', response.data)
        self.assertEqual(response.data['count'], 1)
    
    def test_active_artists_endpoint(self):
        """Testa o endpoint de artistas ativos"""
        url = reverse('artists:active-artists')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('artists', response.data)
        self.assertEqual(len(response.data['artists']), 1)


class AlbumAPITestCase(APITestCase):
    """Testes para endpoints de álbuns"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.client = APIClient()
        
        # Criar gênero
        self.genre = Genre.objects.create(
            name='Pop',
            slug='pop',
            description='Pop music',
            is_active=True
        )
        
        # Criar artistas
        self.artist1 = Artist.objects.create(
            stage_name='Artist One',
            genre=self.genre,
            is_active=True
        )
        
        self.artist2 = Artist.objects.create(
            stage_name='Artist Two',
            genre=self.genre,
            is_active=True
        )
        
        # Criar álbuns
        self.album1 = Album.objects.create(
            artist=self.artist1,
            name='Album One',
            featured=True,
            is_active=True
        )
        
        self.album2 = Album.objects.create(
            artist=self.artist2,
            name='Album Two',
            featured=False,
            is_active=True
        )
    
    def test_album_list_endpoint(self):
        """Testa o endpoint de lista de álbuns"""
        url = reverse('artists:album-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_album_list_filter_by_artist(self):
        """Testa filtro de álbuns por artista"""
        url = reverse('artists:album-list')
        response = self.client.get(url, {'artist': self.artist1.pk})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Album One')
    
    def test_album_list_filter_by_featured(self):
        """Testa filtro de álbuns por destaque"""
        url = reverse('artists:album-list')
        response = self.client.get(url, {'featured': 'true'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Album One')
    
    def test_album_list_filter_by_search(self):
        """Testa busca de álbuns por nome"""
        url = reverse('artists:album-list')
        response = self.client.get(url, {'search': 'One'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Album One')
    
    def test_album_list_filter_by_artist_name(self):
        """Testa filtro de álbuns por nome do artista"""
        url = reverse('artists:album-list')
        response = self.client.get(url, {'artist_name': 'Artist One'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Album One')
    
    def test_album_list_filter_by_genre(self):
        """Testa filtro de álbuns por gênero"""
        url = reverse('artists:album-list')
        response = self.client.get(url, {'genre': 'pop'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_album_list_multiple_filters(self):
        """Testa múltiplos filtros combinados"""
        url = reverse('artists:album-list')
        response = self.client.get(url, {
            'artist': self.artist1.pk,
            'featured': 'true'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Album One')
    
    def test_album_detail_endpoint(self):
        """Testa o endpoint de detalhes do álbum"""
        url = reverse('artists:album-detail', kwargs={'pk': self.album1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Album One')
        self.assertEqual(response.data['featured'], True)
    
    def test_album_create_endpoint(self):
        """Testa o endpoint de criação de álbum"""
        url = reverse('artists:album-create')
        data = {
            'artist': self.artist1.pk,
            'name': 'New Album',
            'featured': False,
            'is_active': True
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Album')
        self.assertTrue(Album.objects.filter(name='New Album').exists())
    
    def test_featured_albums_endpoint(self):
        """Testa o endpoint de álbuns em destaque"""
        url = reverse('artists:featured-albums')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('albums', response.data)
        self.assertEqual(len(response.data['albums']), 1)
        self.assertEqual(response.data['albums'][0]['name'], 'Album One')
    
    def test_album_musics_endpoint(self):
        """Testa o endpoint de músicas do álbum"""
        # Criar música para o álbum
        music = Music.objects.create(
            artist=self.artist1,
            album=self.album1,
            title='Test Music',
            duration=180,
            is_active=True
        )
        
        url = reverse('artists:album-musics', kwargs={'pk': self.album1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('musics', response.data)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['musics'][0]['title'], 'Test Music')


class ArtistModelTestCase(TestCase):
    """Testes para o modelo Artist"""
    
    def setUp(self):
        """Configuração inicial"""
        self.genre = Genre.objects.create(
            name='Jazz',
            slug='jazz',
            description='Jazz music',
            is_active=True
        )
    
    def test_artist_creation(self):
        """Testa criação de artista"""
        artist = Artist.objects.create(
            stage_name='Jazz Artist',
            genre=self.genre,
            is_active=True
        )
        
        self.assertEqual(artist.stage_name, 'Jazz Artist')
        self.assertEqual(artist.genre, self.genre)
        self.assertTrue(artist.is_active)
        self.assertIsNotNone(artist.created_at)
    
    def test_artist_str_representation(self):
        """Testa representação string do artista"""
        artist = Artist.objects.create(
            stage_name='Test Artist',
            genre=self.genre
        )
        
        self.assertEqual(str(artist), 'Test Artist')


class AlbumModelTestCase(TestCase):
    """Testes para o modelo Album"""
    
    def setUp(self):
        """Configuração inicial"""
        self.genre = Genre.objects.create(
            name='Blues',
            slug='blues',
            description='Blues music',
            is_active=True
        )
        
        self.artist = Artist.objects.create(
            stage_name='Blues Artist',
            genre=self.genre,
            is_active=True
        )
    
    def test_album_creation(self):
        """Testa criação de álbum"""
        album = Album.objects.create(
            artist=self.artist,
            name='Blues Album',
            featured=True,
            is_active=True
        )
        
        self.assertEqual(album.name, 'Blues Album')
        self.assertEqual(album.artist, self.artist)
        self.assertTrue(album.featured)
        self.assertTrue(album.is_active)
        self.assertIsNotNone(album.created_at)
    
    def test_album_str_representation(self):
        """Testa representação string do álbum"""
        album = Album.objects.create(
            artist=self.artist,
            name='Test Album'
        )
        
        self.assertEqual(str(album), 'Test Album - Blues Artist')
    
    def test_album_musics_count(self):
        """Testa contagem de músicas do álbum"""
        album = Album.objects.create(
            artist=self.artist,
            name='Test Album'
        )
        
        # Criar músicas
        Music.objects.create(
            artist=self.artist,
            album=album,
            title='Music 1',
            duration=180,
            is_active=True
        )
        
        Music.objects.create(
            artist=self.artist,
            album=album,
            title='Music 2',
            duration=200,
            is_active=True
        )
        
        self.assertEqual(album.get_musics_count(), 2)
