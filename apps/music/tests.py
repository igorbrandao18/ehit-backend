from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from apps.genres.models import Genre
from apps.artists.models import Artist, Album
from .models import Music

User = get_user_model()


class MusicModelTest(TestCase):
    """Testes para o modelo Music"""

    def setUp(self):
        self.genre = Genre.objects.create(name='Forró', slug='forro')
        self.artist = Artist.objects.create(
            stage_name='Music Artist',
            genre=self.genre
        )
        self.album = Album.objects.create(
            artist=self.artist,
            name='Music Album'
        )

    def test_music_creation(self):
        """Testa criação de música"""
        music = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Test Music',
            duration=180,
            genre=self.genre
        )
        self.assertEqual(music.title, 'Test Music')
        self.assertEqual(music.artist, self.artist)
        self.assertEqual(music.duration, 180)

    def test_music_str(self):
        """Testa representação string da música"""
        music = Music.objects.create(
            artist=self.artist,
            title='Str Music',
            duration=180
        )
        self.assertEqual(str(music), 'Str Music - Music Artist')

    def test_music_defaults(self):
        """Testa valores padrão da música"""
        music = Music.objects.create(
            artist=self.artist,
            title='Defaults Music',
            duration=180
        )
        self.assertEqual(music.streams_count, 0)
        self.assertEqual(music.downloads_count, 0)
        self.assertEqual(music.likes_count, 0)
        self.assertFalse(music.is_featured)

    def test_is_popular_property(self):
        """Testa property is_popular"""
        music = Music.objects.create(
            artist=self.artist,
            title='Popular Music',
            duration=180,
            streams_count=2000
        )
        self.assertTrue(music.is_popular)
        
        music.streams_count = 500
        music.save()
        self.assertFalse(music.is_popular)

    def test_is_trending_property(self):
        """Testa property is_trending"""
        music = Music.objects.create(
            artist=self.artist,
            title='Trending Music',
            duration=180,
            streams_count=200
        )
        # Música criada agora com mais de 100 streams deve ser trending
        self.assertTrue(music.is_trending)

    def test_increment_streams(self):
        """Testa incremento de streams"""
        music = Music.objects.create(
            artist=self.artist,
            title='Stream Test',
            duration=180
        )
        initial_count = music.streams_count
        music.increment_streams()
        music.refresh_from_db()
        self.assertEqual(music.streams_count, initial_count + 1)

    def test_increment_downloads(self):
        """Testa incremento de downloads"""
        music = Music.objects.create(
            artist=self.artist,
            title='Download Test',
            duration=180
        )
        initial_count = music.downloads_count
        music.increment_downloads()
        music.refresh_from_db()
        self.assertEqual(music.downloads_count, initial_count + 1)

    def test_increment_likes(self):
        """Testa incremento de curtidas"""
        music = Music.objects.create(
            artist=self.artist,
            title='Like Test',
            duration=180
        )
        initial_count = music.likes_count
        music.increment_likes()
        music.refresh_from_db()
        self.assertEqual(music.likes_count, initial_count + 1)

    def test_decrement_likes(self):
        """Testa decremento de curtidas"""
        music = Music.objects.create(
            artist=self.artist,
            title='Unlike Test',
            duration=180,
            likes_count=5
        )
        music.decrement_likes()
        music.refresh_from_db()
        self.assertEqual(music.likes_count, 4)

    def test_get_duration_formatted(self):
        """Testa formatação de duração"""
        music = Music.objects.create(
            artist=self.artist,
            title='Duration Test',
            duration=185
        )
        formatted = music.get_duration_formatted()
        self.assertEqual(formatted, '3:05')

    def test_get_stream_url(self):
        """Testa URL de streaming"""
        music = Music.objects.create(
            artist=self.artist,
            title='Stream URL Test',
            duration=180
        )
        self.assertEqual(music.get_stream_url(), f'/api/music/{music.id}/stream/')

    def test_get_download_url(self):
        """Testa URL de download"""
        music = Music.objects.create(
            artist=self.artist,
            title='Download URL Test',
            duration=180
        )
        self.assertEqual(music.get_download_url(), f'/api/music/{music.id}/download/')


class MusicSerializerTest(TestCase):
    """Testes para serializers de Music"""

    def setUp(self):
        self.genre = Genre.objects.create(name='Forró', slug='forro')
        self.artist = Artist.objects.create(
            stage_name='Serializer Artist',
            genre=self.genre
        )
        self.album = Album.objects.create(
            artist=self.artist,
            name='Serializer Album'
        )
        self.music = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Serializer Music',
            duration=180,
            streams_count=100
        )

    def test_music_serializer(self):
        """Testa serialização de música"""
        from .serializers import MusicSerializer
        from django.utils import timezone
        # Atualizar release_date para ser uma date ao invés de datetime
        self.music.release_date = timezone.now().date()
        self.music.save()
        
        serializer = MusicSerializer(self.music)
        data = serializer.data
        
        self.assertEqual(data['title'], 'Serializer Music')
        self.assertEqual(data['artist_name'], 'Serializer Artist')
        self.assertIn('duration_formatted', data)
        self.assertIn('stream_url', data)
        self.assertIn('download_url', data)

    def test_music_create_serializer(self):
        """Testa criação de música via serializer"""
        from .serializers import MusicCreateSerializer
        data = {
            'artist': self.artist.id,
            'title': 'New Music',
            'duration': 180
        }
        serializer = MusicCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        music = serializer.save()
        self.assertEqual(music.title, 'New Music')

    def test_music_create_serializer_validation(self):
        """Testa validação de título"""
        from .serializers import MusicCreateSerializer
        data = {
            'artist': self.artist.id,
            'title': 'A',  # Muito curto
            'duration': 180
        }
        serializer = MusicCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_music_stats_serializer(self):
        """Testa serializer de estatísticas"""
        from .serializers import MusicStatsSerializer
        serializer = MusicStatsSerializer(self.music)
        data = serializer.data
        
        self.assertEqual(data['title'], 'Serializer Music')
        self.assertIn('streams_count', data)
        self.assertIn('downloads_count', data)
        self.assertIn('likes_count', data)


class MusicIntegrationTest(TestCase):
    """Testes de integração para Music"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        self.genre = Genre.objects.create(name='Forró', slug='forro')
        self.artist = Artist.objects.create(
            stage_name='Integration Artist',
            genre=self.genre
        )
        self.album = Album.objects.create(
            artist=self.artist,
            name='Integration Album'
        )
        self.music = Music.objects.create(
            artist=self.artist,
            album=self.album,
            title='Integration Music',
            duration=180,
            streams_count=100
        )

    def test_music_with_album_relationship(self):
        """Testa relacionamento música-álbum"""
        self.assertEqual(self.music.album, self.album)
        self.assertEqual(self.music.artist, self.artist)
        
        # Via related_name
        self.assertIn(self.music, self.album.musics.all())

    def test_music_filter_by_artist_query(self):
        """Testa query de filtro por artista"""
        musics = Music.objects.filter(artist=self.artist)
        self.assertGreater(musics.count(), 0)
        
        for music in musics:
            self.assertEqual(music.artist, self.artist)

    def test_music_filter_by_featured_query(self):
        """Testa query de filtro por destaque"""
        Music.objects.create(
            artist=self.artist,
            title='Featured Test',
            duration=180,
            is_featured=True
        )
        
        featured_musics = Music.objects.filter(is_featured=True)
        self.assertGreater(featured_musics.count(), 0)

    def test_music_ordering_by_streams(self):
        """Testa ordenação de músicas por streams"""
        Music.objects.create(
            artist=self.artist,
            title='Most Streamed',
            duration=180,
            streams_count=1000
        )
        
        musics = Music.objects.all().order_by('-streams_count')
        self.assertEqual(musics.first().streams_count, 1000)

    def test_music_filter_by_album(self):
        """Testa filtro de músicas por álbum"""
        musics = Music.objects.filter(album=self.album)
        self.assertGreater(musics.count(), 0)
        
        for music in musics:
            self.assertEqual(music.album, self.album)

