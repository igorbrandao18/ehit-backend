from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from datetime import timedelta
from .models import Music
from apps.artists.models import Artist

User = get_user_model()


class MusicModelTest(TestCase):
    """Testes para o modelo Music"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        # Criar usuário artista
        self.user = User.objects.create_user(
            username='testartist',
            email='artist@test.com',
            password='pass123',
            user_type='artist'
        )
        
        # Criar artista
        self.artist = Artist.objects.create(
            user=self.user,
            stage_name='Test Artist',
            genre='Rock',
            verified=True
        )
        
        self.music_data = {
            'artist': self.artist,
            'title': 'Test Song',
            'album': 'Test Album',
            'genre': 'Rock',
            'duration': 240,  # 4 minutos
            'lyrics': 'Test song lyrics...',
            'release_date': timezone.now().date(),
            'streams_count': 1000,
            'downloads_count': 100,
            'likes_count': 50,
            'is_featured': False
        }
    
    def test_create_music(self):
        """Testa criação de música"""
        music = Music.objects.create(**self.music_data)
        
        self.assertEqual(music.artist, self.artist)
        self.assertEqual(music.title, 'Test Song')
        self.assertEqual(music.album, 'Test Album')
        self.assertEqual(music.genre, 'Rock')
        self.assertEqual(music.duration, 240)
        self.assertEqual(music.lyrics, 'Test song lyrics...')
        self.assertEqual(music.streams_count, 1000)
        self.assertEqual(music.downloads_count, 100)
        self.assertEqual(music.likes_count, 50)
        self.assertFalse(music.is_featured)
        self.assertTrue(music.is_active)
    
    def test_music_str_representation(self):
        """Testa representação string da música"""
        music = Music.objects.create(**self.music_data)
        expected = f"{music.title} - {music.artist.stage_name}"
        self.assertEqual(str(music), expected)
    
    def test_music_ordering(self):
        """Testa ordenação padrão das músicas"""
        # Criar segunda música com menos streams
        music1 = Music.objects.create(**self.music_data)
        music2 = Music.objects.create(
            artist=self.artist,
            title='Second Song',
            duration=180,
            streams_count=500
        )
        
        musics = Music.objects.all()
        # Deve estar ordenado por -streams_count, -created_at
        self.assertEqual(musics[0], music1)  # Mais streams
        self.assertEqual(musics[1], music2)  # Menos streams
    
    def test_music_required_fields(self):
        """Testa campos obrigatórios"""
        # Title é obrigatório - testar com save() que valida
        music = Music(artist=self.artist, duration=240)
        with self.assertRaises(ValidationError):
            music.full_clean()
        
        # Duration é obrigatório - testar com save() que valida
        music = Music(artist=self.artist, title='Test Song')
        with self.assertRaises(ValidationError):
            music.full_clean()
    
    def test_music_methods(self):
        """Testa métodos da música"""
        music = Music.objects.create(**self.music_data)
        
        # Testar get_stream_url
        expected_url = f"/api/music/{music.id}/stream/"
        self.assertEqual(music.get_stream_url(), expected_url)
        
        # Testar get_download_url
        expected_url = f"/api/music/{music.id}/download/"
        self.assertEqual(music.get_download_url(), expected_url)
        
        # Testar get_duration_formatted
        self.assertEqual(music.get_duration_formatted(), "4:00")
        
        # Testar increment_streams
        initial_streams = music.streams_count
        music.increment_streams()
        self.assertEqual(music.streams_count, initial_streams + 1)
        
        # Testar increment_downloads
        initial_downloads = music.downloads_count
        music.increment_downloads()
        self.assertEqual(music.downloads_count, initial_downloads + 1)
        
        # Testar increment_likes
        initial_likes = music.likes_count
        music.increment_likes()
        self.assertEqual(music.likes_count, initial_likes + 1)
        
        # Testar decrement_likes
        music.decrement_likes()
        self.assertEqual(music.likes_count, initial_likes)
        
        # Testar decrement_likes quando count é 0
        music.likes_count = 0
        music.save()
        music.decrement_likes()
        self.assertEqual(music.likes_count, 0)  # Não deve ficar negativo
    
    def test_music_properties(self):
        """Testa propriedades da música"""
        # Testar música popular (mais de 1000 streams)
        popular_music = Music.objects.create(
            artist=self.artist,
            title='Popular Song',
            duration=240,
            streams_count=1500
        )
        self.assertTrue(popular_music.is_popular)
        
        # Testar música não popular
        unpopular_music = Music.objects.create(
            artist=self.artist,
            title='Unpopular Song',
            duration=240,
            streams_count=500
        )
        self.assertFalse(unpopular_music.is_popular)
        
        # Testar música trending (criada na última semana com mais de 100 streams)
        trending_music = Music.objects.create(
            artist=self.artist,
            title='Trending Song',
            duration=240,
            streams_count=200
        )
        self.assertTrue(trending_music.is_trending)
        
        # Testar música não trending (poucos streams)
        not_trending_music = Music.objects.create(
            artist=self.artist,
            title='Not Trending Song',
            duration=240,
            streams_count=50
        )
        self.assertFalse(not_trending_music.is_trending)
    
    def test_music_duration_formats(self):
        """Testa diferentes formatos de duração"""
        # Teste para diferentes durações
        test_cases = [
            (60, "1:00"),    # 1 minuto
            (90, "1:30"),    # 1 minuto e 30 segundos
            (120, "2:00"),   # 2 minutos
            (125, "2:05"),   # 2 minutos e 5 segundos
            (3661, "61:01"), # Mais de 1 hora
        ]
        
        for duration, expected_format in test_cases:
            music = Music.objects.create(
                artist=self.artist,
                title=f'Song {duration}s',
                duration=duration
            )
            self.assertEqual(music.get_duration_formatted(), expected_format)
    
    def test_music_featured_status(self):
        """Testa status de destaque da música"""
        music = Music.objects.create(**self.music_data)
        
        # Inicialmente não em destaque
        self.assertFalse(music.is_featured)
        
        # Deve permitir colocar em destaque
        music.is_featured = True
        music.save()
        self.assertTrue(music.is_featured)
    
    def test_music_release_date(self):
        """Testa data de lançamento"""
        music = Music.objects.create(**self.music_data)
        
        # Deve ter data de lançamento
        self.assertIsNotNone(music.release_date)
        
        # Deve permitir definir data específica
        specific_date = timezone.now().date() - timedelta(days=30)
        music.release_date = specific_date
        music.save()
        self.assertEqual(music.release_date, specific_date)
    
    def test_music_statistics(self):
        """Testa estatísticas da música"""
        music = Music.objects.create(**self.music_data)
        
        # Estatísticas iniciais
        self.assertEqual(music.streams_count, 1000)
        self.assertEqual(music.downloads_count, 100)
        self.assertEqual(music.likes_count, 50)
        
        # Deve permitir atualizar estatísticas
        music.streams_count = 2000
        music.downloads_count = 200
        music.likes_count = 100
        music.save()
        
        self.assertEqual(music.streams_count, 2000)
        self.assertEqual(music.downloads_count, 200)
        self.assertEqual(music.likes_count, 100)


class MusicIntegrationTest(TestCase):
    """Testes de integração para Music"""
    
    def test_music_with_artist_relationship(self):
        """Testa relacionamento música-artista"""
        # Criar usuário e artista
        user = User.objects.create_user(
            username='artist',
            email='artist@test.com',
            password='pass123',
            user_type='artist'
        )
        
        artist = Artist.objects.create(
            user=user,
            stage_name='Test Artist',
            genre='Rock'
        )
        
        # Criar música
        music = Music.objects.create(
            artist=artist,
            title='Test Song',
            duration=240
        )
        
        # Verificar relacionamento
        self.assertEqual(music.artist, artist)
        self.assertIn(music, artist.musics.all())
    
    def test_music_ordering_by_stats(self):
        """Testa ordenação de músicas por estatísticas"""
        # Criar usuário e artista
        user = User.objects.create_user(
            username='artist',
            email='artist@test.com',
            password='pass123',
            user_type='artist'
        )
        
        artist = Artist.objects.create(
            user=user,
            stage_name='Test Artist',
            genre='Rock'
        )
        
        # Criar músicas com diferentes estatísticas
        music1 = Music.objects.create(
            artist=artist,
            title='Song 1',
            duration=240,
            streams_count=1000
        )
        
        music2 = Music.objects.create(
            artist=artist,
            title='Song 2',
            duration=180,
            streams_count=3000
        )
        
        music3 = Music.objects.create(
            artist=artist,
            title='Song 3',
            duration=200,
            streams_count=2000
        )
        
        # Verificar ordenação
        musics = Music.objects.all()
        self.assertEqual(musics[0], music2)  # Mais streams
        self.assertEqual(musics[1], music3)  # Segundo lugar
        self.assertEqual(musics[2], music1)  # Menos streams
    
    def test_music_trending_logic(self):
        """Testa lógica de música trending"""
        # Criar usuário e artista
        user = User.objects.create_user(
            username='artist',
            email='artist@test.com',
            password='pass123',
            user_type='artist'
        )
        
        artist = Artist.objects.create(
            user=user,
            stage_name='Test Artist',
            genre='Rock'
        )
        
        # Música criada agora com muitos streams (deve ser trending)
        trending_music = Music.objects.create(
            artist=artist,
            title='Trending Song',
            duration=240,
            streams_count=200
        )
        self.assertTrue(trending_music.is_trending)
        
        # Música criada agora com poucos streams (não deve ser trending)
        not_trending_music = Music.objects.create(
            artist=artist,
            title='Not Trending Song',
            duration=240,
            streams_count=50
        )
        self.assertFalse(not_trending_music.is_trending)
        
        # Música criada há mais de uma semana (não deve ser trending)
        old_date = timezone.now().date() - timedelta(days=10)
        old_music = Music.objects.create(
            artist=artist,
            title='Old Song',
            duration=240,
            streams_count=200,
            release_date=old_date
        )
        # Simular música criada há mais de uma semana
        old_music.created_at = timezone.now() - timedelta(days=10)
        old_music.save()
        self.assertFalse(old_music.is_trending)
