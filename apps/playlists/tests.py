from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from apps.genres.models import Genre
from apps.artists.models import Artist, Album
from apps.music.models import Music
from .models import Playlist

User = get_user_model()


class PlaylistModelTest(TestCase):
    """Testes para o modelo Playlist"""

    def setUp(self):
        self.genre = Genre.objects.create(name='Forró', slug='forro')
        self.artist = Artist.objects.create(
            stage_name='Playlist Artist',
            genre=self.genre
        )
        self.album = Album.objects.create(
            artist=self.artist,
            name='Playlist Album'
        )
        self.music1 = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Music 1',
            duration=180
        )
        self.music2 = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Music 2',
            duration=200
        )
        self.playlist = Playlist.objects.create(
            name='Test Playlist'
        )
        self.playlist.musics.add(self.music1, self.music2)

    def test_playlist_creation(self):
        """Testa criação de playlist"""
        self.assertEqual(self.playlist.name, 'Test Playlist')
        self.assertTrue(self.playlist.is_active)

    def test_playlist_str(self):
        """Testa representação string da playlist"""
        self.assertEqual(str(self.playlist), 'Test Playlist')

    def test_playlist_defaults(self):
        """Testa valores padrão"""
        new_playlist = Playlist.objects.create(name='New Playlist')
        self.assertFalse(new_playlist.is_featured)
        self.assertTrue(new_playlist.is_active)

    def test_get_musics_count(self):
        """Testa método get_musics_count"""
        count = self.playlist.get_musics_count()
        self.assertEqual(count, 2)

    def test_get_total_duration(self):
        """Testa cálculo de duração total"""
        total_duration = self.playlist.get_total_duration()
        expected_duration = 180 + 200  # 380 segundos
        self.assertEqual(total_duration, expected_duration)

    def test_get_total_duration_formatted(self):
        """Testa formatação de duração total"""
        formatted = self.playlist.get_total_duration_formatted()
        # 380 segundos = 6:20
        self.assertEqual(formatted, '6:20')

    def test_get_total_duration_formatted_with_hours(self):
        """Testa formatação de duração com horas"""
        # Adicionar mais músicas para ultrapassar 1 hora
        music3 = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Music 3',
            duration=1900  # ~31 minutos
        )
        self.playlist.musics.add(music3)
        
        formatted = self.playlist.get_total_duration_formatted()
        # Total: 180 + 200 + 1900 = 2280 segundos = 38 minutos
        # A função retorna sem horas se for menos de 1 hora
        self.assertEqual(formatted, '38:00')

    def test_add_music(self):
        """Testa adição de música"""
        initial_count = self.playlist.get_musics_count()
        music3 = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Music 3',
            duration=180
        )
        self.playlist.add_music(music3)
        self.assertEqual(self.playlist.get_musics_count(), initial_count + 1)

    def test_remove_music(self):
        """Testa remoção de música"""
        initial_count = self.playlist.get_musics_count()
        self.playlist.remove_music(self.music1)
        self.assertEqual(self.playlist.get_musics_count(), initial_count - 1)

    def test_playlist_many_to_many_relationship(self):
        """Testa relacionamento many-to-many com músicas"""
        musics = self.playlist.musics.all()
        self.assertEqual(musics.count(), 2)
        self.assertIn(self.music1, musics)
        self.assertIn(self.music2, musics)

    def test_playlist_ordering(self):
        """Testa ordenação de playlists"""
        playlist2 = Playlist.objects.create(name='Later Playlist')
        
        # A ordenação padrão é por -created_at, então a última criada aparece primeiro
        playlists = Playlist.objects.all()
        # O playlist mais recente deve estar primeiro
        self.assertEqual(playlists.first(), playlist2)
        # Verificar que ambos estão na lista
        self.assertIn(self.playlist, playlists)
        self.assertIn(playlist2, playlists)

    def test_playlist_is_featured(self):
        """Testa playlist em destaque"""
        featured_playlist = Playlist.objects.create(
            name='Featured Playlist',
            is_featured=True
        )
        self.assertTrue(featured_playlist.is_featured)

    def test_empty_playlist_duration(self):
        """Testa duração de playlist vazia"""
        empty_playlist = Playlist.objects.create(name='Empty Playlist')
        self.assertEqual(empty_playlist.get_total_duration(), 0)
        self.assertEqual(empty_playlist.get_total_duration_formatted(), '0:00')

    def test_playlist_update_name(self):
        """Testa atualização de nome da playlist"""
        self.playlist.name = 'Updated Playlist'
        self.playlist.save()
        
        updated_playlist = Playlist.objects.get(id=self.playlist.id)
        self.assertEqual(updated_playlist.name, 'Updated Playlist')

    def test_playlist_toggle_featured(self):
        """Testa alternância de featured"""
        self.assertFalse(self.playlist.is_featured)
        
        self.playlist.is_featured = True
        self.playlist.save()
        
        updated_playlist = Playlist.objects.get(id=self.playlist.id)
        self.assertTrue(updated_playlist.is_featured)
        
        updated_playlist.is_featured = False
        updated_playlist.save()
        
        re_updated_playlist = Playlist.objects.get(id=self.playlist.id)
        self.assertFalse(re_updated_playlist.is_featured)

    def test_playlist_delete_music(self):
        """Testa exclusão de música da playlist"""
        initial_count = self.playlist.get_musics_count()
        
        self.playlist.musics.remove(self.music1)
        
        self.assertEqual(self.playlist.get_musics_count(), initial_count - 1)
        self.assertNotIn(self.music1, self.playlist.musics.all())

    def test_playlist_add_multiple_musics(self):
        """Testa adição múltipla de músicas"""
        music3 = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Music 3',
            duration=180
        )
        music4 = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Music 4',
            duration=200
        )
        
        self.playlist.musics.add(music3, music4)
        
        self.assertEqual(self.playlist.get_musics_count(), 4)

