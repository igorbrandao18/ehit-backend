"""
Testes automatizados para a app Playlists
Testa todos os endpoints e funcionalidades de playlists (PlayHits)
"""

from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from apps.playlists.models import Playlist
from apps.artists.models import Artist, Album
from apps.genres.models import Genre
from apps.music.models import Music


class PlaylistAPITestCase(APITestCase):
    """Testes para endpoints de playlists"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.client = APIClient()
        
        # Criar gênero
        self.genre = Genre.objects.create(
            name='Hip Hop',
            slug='hip-hop',
            description='Hip Hop music',
            is_active=True
        )
        
        # Criar artista
        self.artist = Artist.objects.create(
            stage_name='Hip Hop Artist',
            genre=self.genre,
            is_active=True
        )
        
        # Criar álbum
        self.album = Album.objects.create(
            artist=self.artist,
            name='Hip Hop Album',
            is_active=True
        )
        
        # Criar músicas
        self.music1 = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Hip Hop Track 1',
            duration=180,
            is_active=True
        )
        
        self.music2 = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Hip Hop Track 2',
            duration=200,
            is_active=True
        )
        
        # Criar playlist
        self.playlist = Playlist.objects.create(
            name='Hip Hop PlayHit',
            is_active=True
        )
        self.playlist.musics.add(self.music1, self.music2)
    
    def test_playlist_list_endpoint(self):
        """Testa o endpoint de lista de playlists"""
        url = reverse('playlists:playlist-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Hip Hop PlayHit')
    
    def test_playlist_detail_endpoint(self):
        """Testa o endpoint de detalhes da playlist"""
        url = reverse('playlists:playlist-detail', kwargs={'pk': self.playlist.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Hip Hop PlayHit')
        self.assertEqual(response.data['musics_count'], 2)
        self.assertEqual(len(response.data['musics_data']), 2)
    
    def test_playlist_create_endpoint(self):
        """Testa o endpoint de criação de playlist"""
        url = reverse('playlists:playlist-create')
        data = {
            'name': 'New PlayHit',
            'is_active': True
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New PlayHit')
        self.assertTrue(Playlist.objects.filter(name='New PlayHit').exists())
    
    def test_playlist_add_music_endpoint(self):
        """Testa o endpoint de adicionar música à playlist"""
        # Criar nova música
        new_music = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='New Track',
            duration=150,
            is_active=True
        )
        
        url = reverse('playlists:add-music', kwargs={'pk': self.playlist.pk})
        data = {'music_id': new_music.pk}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.playlist.refresh_from_db()
        self.assertEqual(self.playlist.musics.count(), 3)
        self.assertIn(new_music, self.playlist.musics.all())
    
    # def test_playlist_remove_music_endpoint(self):
    #     """Testa o endpoint de remover música da playlist"""
    #     url = reverse('playlists:remove-music', kwargs={
    #         'pk': self.playlist.pk,
    #         'music_id': self.music1.pk
    #     })
    #     response = self.client.post(url)
    #     
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.playlist.refresh_from_db()
    #     self.assertEqual(self.playlist.musics.count(), 1)
    #     self.assertNotIn(self.music1, self.playlist.musics.all())
    
    # def test_playlist_reorder_musics_endpoint(self):
    #     """Testa o endpoint de reordenar músicas da playlist"""
    #     url = reverse('playlists:reorder-musics', kwargs={'pk': self.playlist.pk})
    #     data = {
    #         'music_ids': [self.music2.pk, self.music1.pk]  # Inverter ordem
    #     }
    #     response = self.client.post(url, data, format='json')
    #     
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.playlist.refresh_from_db()
    #     musics = list(self.playlist.musics.all())
    #     self.assertEqual(musics[0], self.music2)
    #     self.assertEqual(musics[1], self.music1)
    
    def test_active_playhits_endpoint(self):
        """Testa o endpoint de PlayHits ativos"""
        url = reverse('playlists:active-playhits')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('playhits', response.data)
        self.assertEqual(len(response.data['playhits']), 1)
        self.assertEqual(response.data['playhits'][0]['name'], 'Hip Hop PlayHit')
    
    def test_playlist_search_by_name(self):
        """Testa busca de playlists por nome"""
        url = reverse('playlists:playlist-list')
        response = self.client.get(url, {'search': 'Hip Hop'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Hip Hop PlayHit')
    
    def test_playlist_filter_by_active(self):
        """Testa filtro de playlists por status ativo"""
        # Criar playlist inativa
        inactive_playlist = Playlist.objects.create(
            name='Inactive PlayHit',
            is_active=False
        )
        
        url = reverse('playlists:playlist-list')
        response = self.client.get(url, {'is_active': 'true'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Hip Hop PlayHit')


class PlaylistModelTestCase(TestCase):
    """Testes para o modelo Playlist"""
    
    def setUp(self):
        """Configuração inicial"""
        self.genre = Genre.objects.create(
            name='Reggae',
            slug='reggae',
            description='Reggae music',
            is_active=True
        )
        
        self.artist = Artist.objects.create(
            stage_name='Reggae Artist',
            genre=self.genre,
            is_active=True
        )
        
        self.album = Album.objects.create(
            artist=self.artist,
            name='Reggae Album',
            is_active=True
        )
        
        self.music1 = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Reggae Track 1',
            duration=180,
            is_active=True
        )
        
        self.music2 = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Reggae Track 2',
            duration=200,
            is_active=True
        )
    
    def test_playlist_creation(self):
        """Testa criação de playlist"""
        playlist = Playlist.objects.create(
            name='Reggae PlayHit',
            is_active=True
        )
        
        self.assertEqual(playlist.name, 'Reggae PlayHit')
        self.assertTrue(playlist.is_active)
        self.assertIsNotNone(playlist.created_at)
    
    def test_playlist_str_representation(self):
        """Testa representação string da playlist"""
        playlist = Playlist.objects.create(
            name='Test PlayHit'
        )
        
        self.assertEqual(str(playlist), 'Test PlayHit')
    
    def test_playlist_add_musics(self):
        """Testa adicionar músicas à playlist"""
        playlist = Playlist.objects.create(
            name='Test PlayHit'
        )
        
        playlist.musics.add(self.music1, self.music2)
        
        self.assertEqual(playlist.musics.count(), 2)
        self.assertIn(self.music1, playlist.musics.all())
        self.assertIn(self.music2, playlist.musics.all())
    
    def test_playlist_get_musics_count(self):
        """Testa contagem de músicas da playlist"""
        playlist = Playlist.objects.create(
            name='Test PlayHit'
        )
        
        playlist.musics.add(self.music1, self.music2)
        
        self.assertEqual(playlist.get_musics_count(), 2)
    
    def test_playlist_remove_music(self):
        """Testa remover música da playlist"""
        playlist = Playlist.objects.create(
            name='Test PlayHit'
        )
        
        playlist.musics.add(self.music1, self.music2)
        self.assertEqual(playlist.musics.count(), 2)
        
        playlist.musics.remove(self.music1)
        self.assertEqual(playlist.musics.count(), 1)
        self.assertNotIn(self.music1, playlist.musics.all())
        self.assertIn(self.music2, playlist.musics.all())
    
    def test_playlist_clear_musics(self):
        """Testa limpar todas as músicas da playlist"""
        playlist = Playlist.objects.create(
            name='Test PlayHit'
        )
        
        playlist.musics.add(self.music1, self.music2)
        self.assertEqual(playlist.musics.count(), 2)
        
        playlist.musics.clear()
        self.assertEqual(playlist.musics.count(), 0)
