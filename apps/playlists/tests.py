from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import Playlist, PlaylistMusic, UserFavorite
from apps.artists.models import Artist
from apps.music.models import Music

User = get_user_model()


class PlaylistModelTest(TestCase):
    """Testes para o modelo Playlist"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        # Criar usuário
        self.user = User.objects.create_user(
            username='testuser',
            email='user@test.com',
            password='pass123',
            user_type='listener'
        )
        
        # Criar artista e música
        self.artist_user = User.objects.create_user(
            username='artist',
            email='artist@test.com',
            password='pass123',
            user_type='artist'
        )
        
        self.artist = Artist.objects.create(
            user=self.artist_user,
            stage_name='Test Artist',
            genre='Rock'
        )
        
        self.music = Music.objects.create(
            artist=self.artist,
            title='Test Song',
            duration=240
        )
        
        self.playlist_data = {
            'user': self.user,
            'name': 'My Playlist',
            'description': 'A test playlist',
            'is_public': True,
            'followers_count': 0
        }
    
    def test_create_playlist(self):
        """Testa criação de playlist"""
        playlist = Playlist.objects.create(**self.playlist_data)
        
        self.assertEqual(playlist.user, self.user)
        self.assertEqual(playlist.name, 'My Playlist')
        self.assertEqual(playlist.description, 'A test playlist')
        self.assertTrue(playlist.is_public)
        self.assertEqual(playlist.followers_count, 0)
        self.assertTrue(playlist.is_active)
    
    def test_playlist_str_representation(self):
        """Testa representação string da playlist"""
        playlist = Playlist.objects.create(**self.playlist_data)
        expected = f"{playlist.name} - {playlist.user.username}"
        self.assertEqual(str(playlist), expected)
    
    def test_playlist_ordering(self):
        """Testa ordenação padrão das playlists"""
        # Criar segunda playlist com menos seguidores
        playlist1 = Playlist.objects.create(**self.playlist_data)
        playlist2 = Playlist.objects.create(
            user=self.user,
            name='Second Playlist',
            followers_count=500
        )
        
        playlists = Playlist.objects.all()
        # Deve estar ordenado por -followers_count, -created_at
        self.assertEqual(playlists[0], playlist2)  # Mais seguidores
        self.assertEqual(playlists[1], playlist1)  # Menos seguidores
    
    def test_playlist_required_fields(self):
        """Testa campos obrigatórios"""
        # Name é obrigatório - testar com save() que valida
        playlist = Playlist(user=self.user)
        with self.assertRaises(ValidationError):
            playlist.full_clean()
    
    def test_playlist_methods(self):
        """Testa métodos da playlist"""
        playlist = Playlist.objects.create(**self.playlist_data)
        
        # Testar get_total_duration (sem músicas)
        self.assertEqual(playlist.get_total_duration(), 0)
        self.assertEqual(playlist.get_total_duration_formatted(), "0:00")
        
        # Testar get_musics_count (sem músicas)
        self.assertEqual(playlist.get_musics_count(), 0)
        
        # Adicionar música à playlist
        playlist.add_music(self.music)
        
        # Testar get_total_duration com música
        self.assertEqual(playlist.get_total_duration(), 240)
        self.assertEqual(playlist.get_total_duration_formatted(), "4:00")
        
        # Testar get_musics_count com música
        self.assertEqual(playlist.get_musics_count(), 1)
        
        # Testar remove_music
        playlist.remove_music(self.music)
        self.assertEqual(playlist.get_musics_count(), 0)
    
    def test_playlist_add_music(self):
        """Testa adição de música à playlist"""
        playlist = Playlist.objects.create(**self.playlist_data)
        
        # Adicionar música
        playlist.add_music(self.music)
        
        # Verificar se música foi adicionada
        self.assertEqual(playlist.get_musics_count(), 1)
        self.assertIn(self.music, playlist.musics.all())
        
        # Verificar PlaylistMusic foi criado
        playlist_music = PlaylistMusic.objects.get(playlist=playlist, music=self.music)
        self.assertEqual(playlist_music.order, 0)
    
    def test_playlist_add_music_with_order(self):
        """Testa adição de música com ordem específica"""
        playlist = Playlist.objects.create(**self.playlist_data)
        
        # Adicionar música com ordem específica
        playlist.add_music(self.music, order=5)
        
        # Verificar ordem
        playlist_music = PlaylistMusic.objects.get(playlist=playlist, music=self.music)
        self.assertEqual(playlist_music.order, 5)
    
    def test_playlist_remove_music(self):
        """Testa remoção de música da playlist"""
        playlist = Playlist.objects.create(**self.playlist_data)
        
        # Adicionar música
        playlist.add_music(self.music)
        self.assertEqual(playlist.get_musics_count(), 1)
        
        # Remover música
        playlist.remove_music(self.music)
        self.assertEqual(playlist.get_musics_count(), 0)
        self.assertNotIn(self.music, playlist.musics.all())
    
    def test_playlist_reorder_musics(self):
        """Testa reordenação de músicas"""
        playlist = Playlist.objects.create(**self.playlist_data)
        
        # Criar segunda música
        music2 = Music.objects.create(
            artist=self.artist,
            title='Second Song',
            duration=180
        )
        
        # Adicionar músicas
        playlist.add_music(self.music, order=0)
        playlist.add_music(music2, order=1)
        
        # Reordenar
        music_orders = {
            self.music.id: 1,
            music2.id: 0
        }
        playlist.reorder_musics(music_orders)
        
        # Verificar nova ordem
        playlist_music1 = PlaylistMusic.objects.get(playlist=playlist, music=self.music)
        playlist_music2 = PlaylistMusic.objects.get(playlist=playlist, music=music2)
        
        self.assertEqual(playlist_music1.order, 1)
        self.assertEqual(playlist_music2.order, 0)
    
    def test_playlist_duration_formats(self):
        """Testa diferentes formatos de duração"""
        playlist = Playlist.objects.create(**self.playlist_data)
        
        # Criar músicas com diferentes durações
        music1 = Music.objects.create(artist=self.artist, title='Song 1', duration=60)   # 1 min
        music2 = Music.objects.create(artist=self.artist, title='Song 2', duration=90)   # 1:30
        music3 = Music.objects.create(artist=self.artist, title='Song 3', duration=3661) # 1:01:01
        
        # Adicionar músicas
        playlist.add_music(music1)
        playlist.add_music(music2)
        playlist.add_music(music3)
        
        # Testar formato com horas (60 + 90 + 3661 = 3811 segundos = 1:03:31)
        self.assertEqual(playlist.get_total_duration_formatted(), "1:03:31")
        
        # Remover música longa e testar formato sem horas
        playlist.remove_music(music3)
        self.assertEqual(playlist.get_total_duration_formatted(), "2:30")
    
    def test_playlist_privacy(self):
        """Testa configurações de privacidade"""
        playlist = Playlist.objects.create(**self.playlist_data)
        
        # Inicialmente pública
        self.assertTrue(playlist.is_public)
        
        # Deve permitir tornar privada
        playlist.is_public = False
        playlist.save()
        self.assertFalse(playlist.is_public)
    
    def test_playlist_followers_count(self):
        """Testa contador de seguidores"""
        playlist = Playlist.objects.create(**self.playlist_data)
        
        # Inicialmente deve ser 0
        self.assertEqual(playlist.followers_count, 0)
        
        # Deve permitir incrementar
        playlist.followers_count = 100
        playlist.save()
        self.assertEqual(playlist.followers_count, 100)


class PlaylistMusicModelTest(TestCase):
    """Testes para o modelo PlaylistMusic"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        # Criar usuário
        self.user = User.objects.create_user(
            username='testuser',
            email='user@test.com',
            password='pass123'
        )
        
        # Criar artista e música
        self.artist_user = User.objects.create_user(
            username='artist',
            email='artist@test.com',
            password='pass123',
            user_type='artist'
        )
        
        self.artist = Artist.objects.create(
            user=self.artist_user,
            stage_name='Test Artist',
            genre='Rock'
        )
        
        self.music = Music.objects.create(
            artist=self.artist,
            title='Test Song',
            duration=240
        )
        
        # Criar playlist
        self.playlist = Playlist.objects.create(
            user=self.user,
            name='Test Playlist'
        )
    
    def test_create_playlist_music(self):
        """Testa criação de PlaylistMusic"""
        playlist_music = PlaylistMusic.objects.create(
            playlist=self.playlist,
            music=self.music,
            order=1
        )
        
        self.assertEqual(playlist_music.playlist, self.playlist)
        self.assertEqual(playlist_music.music, self.music)
        self.assertEqual(playlist_music.order, 1)
        self.assertIsNotNone(playlist_music.added_at)
    
    def test_playlist_music_str_representation(self):
        """Testa representação string de PlaylistMusic"""
        playlist_music = PlaylistMusic.objects.create(
            playlist=self.playlist,
            music=self.music,
            order=1
        )
        expected = f"{self.playlist.name} - {self.music.title}"
        self.assertEqual(str(playlist_music), expected)
    
    def test_playlist_music_ordering(self):
        """Testa ordenação de PlaylistMusic"""
        # Criar segunda música
        music2 = Music.objects.create(
            artist=self.artist,
            title='Second Song',
            duration=180
        )
        
        # Criar PlaylistMusic com diferentes ordens
        playlist_music1 = PlaylistMusic.objects.create(
            playlist=self.playlist,
            music=self.music,
            order=2
        )
        
        playlist_music2 = PlaylistMusic.objects.create(
            playlist=self.playlist,
            music=music2,
            order=1
        )
        
        # Verificar ordenação
        playlist_musics = PlaylistMusic.objects.all()
        self.assertEqual(playlist_musics[0], playlist_music2)  # Ordem 1
        self.assertEqual(playlist_musics[1], playlist_music1)  # Ordem 2
    
    def test_playlist_music_unique_together(self):
        """Testa constraint unique_together"""
        # Criar primeiro PlaylistMusic
        PlaylistMusic.objects.create(
            playlist=self.playlist,
            music=self.music,
            order=1
        )
        
        # Não deve permitir criar outro com mesma playlist e música
        with self.assertRaises(IntegrityError):
            PlaylistMusic.objects.create(
                playlist=self.playlist,
                music=self.music,
                order=2
            )


class UserFavoriteModelTest(TestCase):
    """Testes para o modelo UserFavorite"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        # Criar usuário
        self.user = User.objects.create_user(
            username='testuser',
            email='user@test.com',
            password='pass123'
        )
        
        # Criar artista e música
        self.artist_user = User.objects.create_user(
            username='artist',
            email='artist@test.com',
            password='pass123',
            user_type='artist'
        )
        
        self.artist = Artist.objects.create(
            user=self.artist_user,
            stage_name='Test Artist',
            genre='Rock'
        )
        
        self.music = Music.objects.create(
            artist=self.artist,
            title='Test Song',
            duration=240
        )
    
    def test_create_user_favorite(self):
        """Testa criação de favorito"""
        favorite = UserFavorite.objects.create(
            user=self.user,
            music=self.music
        )
        
        self.assertEqual(favorite.user, self.user)
        self.assertEqual(favorite.music, self.music)
        self.assertIsNotNone(favorite.added_at)
    
    def test_user_favorite_str_representation(self):
        """Testa representação string de UserFavorite"""
        favorite = UserFavorite.objects.create(
            user=self.user,
            music=self.music
        )
        expected = f"{self.user.username} - {self.music.title}"
        self.assertEqual(str(favorite), expected)
    
    def test_user_favorite_ordering(self):
        """Testa ordenação de UserFavorite"""
        # Criar segunda música
        music2 = Music.objects.create(
            artist=self.artist,
            title='Second Song',
            duration=180
        )
        
        # Criar favoritos
        favorite1 = UserFavorite.objects.create(user=self.user, music=self.music)
        favorite2 = UserFavorite.objects.create(user=self.user, music=music2)
        
        # Verificar ordenação (mais recente primeiro)
        favorites = UserFavorite.objects.all()
        self.assertEqual(favorites[0], favorite2)  # Mais recente
        self.assertEqual(favorites[1], favorite1)  # Mais antigo
    
    def test_user_favorite_unique_together(self):
        """Testa constraint unique_together"""
        # Criar primeiro favorito
        UserFavorite.objects.create(user=self.user, music=self.music)
        
        # Não deve permitir criar outro com mesmo usuário e música
        with self.assertRaises(IntegrityError):
            UserFavorite.objects.create(user=self.user, music=self.music)
    
    def test_user_favorite_relationships(self):
        """Testa relacionamentos de UserFavorite"""
        favorite = UserFavorite.objects.create(user=self.user, music=self.music)
        
        # Verificar relacionamento com usuário
        self.assertIn(favorite, self.user.favorites.all())
        
        # Verificar relacionamento com música
        self.assertIn(favorite, self.music.favorited_by.all())


class PlaylistIntegrationTest(TestCase):
    """Testes de integração para Playlist"""
    
    def test_playlist_with_multiple_musics(self):
        """Testa playlist com múltiplas músicas"""
        # Criar usuário
        user = User.objects.create_user(
            username='testuser',
            email='user@test.com',
            password='pass123'
        )
        
        # Criar artista
        artist_user = User.objects.create_user(
            username='artist',
            email='artist@test.com',
            password='pass123',
            user_type='artist'
        )
        
        artist = Artist.objects.create(
            user=artist_user,
            stage_name='Test Artist',
            genre='Rock'
        )
        
        # Criar músicas
        music1 = Music.objects.create(artist=artist, title='Song 1', duration=240)
        music2 = Music.objects.create(artist=artist, title='Song 2', duration=180)
        music3 = Music.objects.create(artist=artist, title='Song 3', duration=300)
        
        # Criar playlist
        playlist = Playlist.objects.create(
            user=user,
            name='Test Playlist'
        )
        
        # Adicionar músicas
        playlist.add_music(music1, order=0)
        playlist.add_music(music2, order=1)
        playlist.add_music(music3, order=2)
        
        # Verificar estatísticas
        self.assertEqual(playlist.get_musics_count(), 3)
        self.assertEqual(playlist.get_total_duration(), 720)  # 240 + 180 + 300
        self.assertEqual(playlist.get_total_duration_formatted(), "12:00")
        
        # Verificar músicas na playlist
        self.assertIn(music1, playlist.musics.all())
        self.assertIn(music2, playlist.musics.all())
        self.assertIn(music3, playlist.musics.all())
    
    def test_playlist_ordering_by_followers(self):
        """Testa ordenação de playlists por seguidores"""
        # Criar usuário
        user = User.objects.create_user(
            username='testuser',
            email='user@test.com',
            password='pass123'
        )
        
        # Criar playlists com diferentes números de seguidores
        playlist1 = Playlist.objects.create(
            user=user,
            name='Playlist 1',
            followers_count=1000
        )
        
        playlist2 = Playlist.objects.create(
            user=user,
            name='Playlist 2',
            followers_count=3000
        )
        
        playlist3 = Playlist.objects.create(
            user=user,
            name='Playlist 3',
            followers_count=2000
        )
        
        # Verificar ordenação
        playlists = Playlist.objects.all()
        self.assertEqual(playlists[0], playlist2)  # Mais seguidores
        self.assertEqual(playlists[1], playlist3)  # Segundo lugar
        self.assertEqual(playlists[2], playlist1)  # Menos seguidores
