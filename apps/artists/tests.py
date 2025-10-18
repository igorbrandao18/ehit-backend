from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import Artist, BaseModel

User = get_user_model()


class BaseModelTest(TestCase):
    """Testes para o modelo BaseModel"""
    
    def test_base_model_fields(self):
        """Testa campos do BaseModel"""
        # Criar um artista para testar BaseModel
        user = User.objects.create_user(
            username='testartist',
            email='artist@test.com',
            password='pass123',
            user_type='artist'
        )
        
        artist = Artist.objects.create(
            user=user,
            stage_name='Test Artist',
            genre='Rock'
        )
        
        # Verificar campos do BaseModel
        self.assertIsNotNone(artist.created_at)
        self.assertIsNotNone(artist.updated_at)
        self.assertTrue(artist.is_active)
        
        # Testar ordenação padrão
        artists = Artist.objects.all()
        self.assertEqual(artists[0], artist)


class ArtistModelTest(TestCase):
    """Testes para o modelo Artist"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(
            username='testartist',
            email='artist@test.com',
            password='pass123',
            user_type='artist',
            first_name='Test',
            last_name='Artist',
            bio='Test artist bio',
            location='Test City',
            verified=True
        )
        
        self.artist_data = {
            'user': self.user,
            'stage_name': 'Test Artist',
            'real_name': 'Test Artist Real',
            'bio': 'Test artist biography',
            'genre': 'Rock',
            'location': 'Test City',
            'website': 'https://testartist.com',
            'social_links': {
                'instagram': '@testartist',
                'youtube': 'TestArtistOfficial'
            },
            'verified': True,
            'followers_count': 1000,
            'monthly_listeners': 5000
        }
    
    def test_create_artist(self):
        """Testa criação de artista"""
        artist = Artist.objects.create(**self.artist_data)
        
        self.assertEqual(artist.user, self.user)
        self.assertEqual(artist.stage_name, 'Test Artist')
        self.assertEqual(artist.real_name, 'Test Artist Real')
        self.assertEqual(artist.bio, 'Test artist biography')
        self.assertEqual(artist.genre, 'Rock')
        self.assertEqual(artist.location, 'Test City')
        self.assertEqual(artist.website, 'https://testartist.com')
        self.assertEqual(artist.social_links['instagram'], '@testartist')
        self.assertEqual(artist.social_links['youtube'], 'TestArtistOfficial')
        self.assertTrue(artist.verified)
        self.assertEqual(artist.followers_count, 1000)
        self.assertEqual(artist.monthly_listeners, 5000)
        self.assertTrue(artist.is_active)
    
    def test_artist_str_representation(self):
        """Testa representação string do artista"""
        artist = Artist.objects.create(**self.artist_data)
        self.assertEqual(str(artist), 'Test Artist')
    
    def test_artist_ordering(self):
        """Testa ordenação padrão dos artistas"""
        # Criar segundo artista com menos seguidores
        user2 = User.objects.create_user(
            username='artist2',
            email='artist2@test.com',
            password='pass123',
            user_type='artist'
        )
        
        artist1 = Artist.objects.create(**self.artist_data)
        artist2 = Artist.objects.create(
            user=user2,
            stage_name='Artist 2',
            followers_count=500
        )
        
        artists = Artist.objects.all()
        # Deve estar ordenado por -followers_count, -created_at
        self.assertEqual(artists[0], artist1)  # Mais seguidores
        self.assertEqual(artists[1], artist2)  # Menos seguidores
    
    def test_artist_required_fields(self):
        """Testa campos obrigatórios"""
        # Stage name é obrigatório - testar com save() que valida
        artist = Artist(user=self.user)
        with self.assertRaises(ValidationError):
            artist.full_clean()
    
    def test_artist_one_to_one_user(self):
        """Testa relacionamento one-to-one com User"""
        artist = Artist.objects.create(**self.artist_data)
        
        # Deve ter acesso ao perfil do artista através do user
        self.assertEqual(self.user.artist_profile, artist)
        
        # Não deve permitir criar outro artista para o mesmo user
        with self.assertRaises(IntegrityError):
            Artist.objects.create(
                user=self.user,
                stage_name='Another Artist'
            )
    
    def test_artist_methods(self):
        """Testa métodos do artista"""
        artist = Artist.objects.create(**self.artist_data)
        
        # Testar get_total_streams (sem músicas ainda)
        self.assertEqual(artist.get_total_streams(), 0)
        
        # Testar get_total_downloads (sem músicas ainda)
        self.assertEqual(artist.get_total_downloads(), 0)
        
        # Testar get_total_likes (sem músicas ainda)
        self.assertEqual(artist.get_total_likes(), 0)
        
        # Testar propriedade is_verified
        self.assertTrue(artist.is_verified)
        
        # Testar increment_followers
        initial_count = artist.followers_count
        artist.increment_followers()
        self.assertEqual(artist.followers_count, initial_count + 1)
        
        # Testar decrement_followers
        artist.decrement_followers()
        self.assertEqual(artist.followers_count, initial_count)
        
        # Testar decrement_followers quando count é 0
        artist.followers_count = 0
        artist.save()
        artist.decrement_followers()
        self.assertEqual(artist.followers_count, 0)  # Não deve ficar negativo
    
    def test_artist_verification(self):
        """Testa sistema de verificação do artista"""
        artist = Artist.objects.create(**self.artist_data)
        
        # Inicialmente verificado
        self.assertTrue(artist.verified)
        self.assertTrue(artist.is_verified)
        
        # Deve permitir desverificar
        artist.verified = False
        artist.save()
        self.assertFalse(artist.verified)
        self.assertFalse(artist.is_verified)
    
    def test_artist_social_links(self):
        """Testa links sociais do artista"""
        artist = Artist.objects.create(**self.artist_data)
        
        # Deve ter links sociais configurados
        self.assertIn('instagram', artist.social_links)
        self.assertIn('youtube', artist.social_links)
        
        # Deve permitir adicionar novos links
        artist.social_links['twitter'] = '@testartist'
        artist.save()
        self.assertIn('twitter', artist.social_links)
    
    def test_artist_statistics(self):
        """Testa estatísticas do artista"""
        artist = Artist.objects.create(**self.artist_data)
        
        # Estatísticas iniciais
        self.assertEqual(artist.followers_count, 1000)
        self.assertEqual(artist.monthly_listeners, 5000)
        
        # Deve permitir atualizar estatísticas
        artist.followers_count = 2000
        artist.monthly_listeners = 10000
        artist.save()
        
        self.assertEqual(artist.followers_count, 2000)
        self.assertEqual(artist.monthly_listeners, 10000)


class ArtistIntegrationTest(TestCase):
    """Testes de integração para Artist"""
    
    def test_artist_with_music_stats(self):
        """Testa estatísticas do artista com músicas"""
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
        
        # Criar músicas reais para testar
        from apps.music.models import Music
        
        music1 = Music.objects.create(
            artist=artist,
            title='Song 1',
            duration=240,
            streams_count=1000,
            downloads_count=100,
            likes_count=50
        )
        
        music2 = Music.objects.create(
            artist=artist,
            title='Song 2',
            duration=180,
            streams_count=2000,
            downloads_count=200,
            likes_count=100
        )
        
        # Testar métodos de estatísticas
        self.assertEqual(artist.get_total_streams(), 3000)
        self.assertEqual(artist.get_total_downloads(), 300)
        self.assertEqual(artist.get_total_likes(), 150)
    
    def test_artist_ordering_by_stats(self):
        """Testa ordenação de artistas por estatísticas"""
        # Criar usuários
        user1 = User.objects.create_user(
            username='artist1', email='artist1@test.com', password='pass123', user_type='artist'
        )
        user2 = User.objects.create_user(
            username='artist2', email='artist2@test.com', password='pass123', user_type='artist'
        )
        user3 = User.objects.create_user(
            username='artist3', email='artist3@test.com', password='pass123', user_type='artist'
        )
        
        # Criar artistas com diferentes números de seguidores
        artist1 = Artist.objects.create(user=user1, stage_name='Artist 1', followers_count=1000)
        artist2 = Artist.objects.create(user=user2, stage_name='Artist 2', followers_count=3000)
        artist3 = Artist.objects.create(user=user3, stage_name='Artist 3', followers_count=2000)
        
        # Verificar ordenação
        artists = Artist.objects.all()
        self.assertEqual(artists[0], artist2)  # Mais seguidores
        self.assertEqual(artists[1], artist3)  # Segundo lugar
        self.assertEqual(artists[2], artist1)  # Menos seguidores
