from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from apps.genres.models import Genre
from .models import Artist, Album

User = get_user_model()


class ArtistModelTest(TestCase):
    """Testes para o modelo Artist"""

    def setUp(self):
        self.genre = Genre.objects.create(name='Forró', slug='forro')
        self.artist = Artist.objects.create(
            stage_name='Test Artist',
            genre=self.genre
        )

    def test_artist_creation(self):
        """Testa criação de artista"""
        self.assertEqual(self.artist.stage_name, 'Test Artist')
        self.assertEqual(self.artist.genre, self.genre)
        self.assertTrue(self.artist.is_active)

    def test_artist_str(self):
        """Testa representação string do artista"""
        self.assertEqual(str(self.artist), 'Test Artist')

    def test_artist_genre_relationship(self):
        """Testa relacionamento entre artista e gênero"""
        self.assertEqual(self.artist.genre.name, 'Forró')

    def test_artist_base_model_fields(self):
        """Testa campos do BaseModel"""
        self.assertIsNotNone(self.artist.created_at)
        self.assertIsNotNone(self.artist.updated_at)
        self.assertTrue(self.artist.is_active)

    def test_artist_is_active_default(self):
        """Testa valor padrão de is_active"""
        new_artist = Artist.objects.create(stage_name='New Artist')
        self.assertTrue(new_artist.is_active)

    def test_albums_count(self):
        """Testa contagem de álbuns"""
        Album.objects.create(artist=self.artist, name='Album 1')
        Album.objects.create(artist=self.artist, name='Album 2')
        
        # Atualizar o artista para obter a contagem atualizada
        self.artist.refresh_from_db()
        self.assertEqual(self.artist.albums.count(), 2)


class AlbumModelTest(TestCase):
    """Testes para o modelo Album"""

    def setUp(self):
        self.genre = Genre.objects.create(name='Forró', slug='forro')
        self.artist = Artist.objects.create(
            stage_name='Test Artist',
            genre=self.genre
        )
        self.album = Album.objects.create(
            artist=self.artist,
            name='Test Album'
        )

    def test_album_creation(self):
        """Testa criação de álbum"""
        self.assertEqual(self.album.name, 'Test Album')
        self.assertEqual(self.album.artist, self.artist)
        self.assertTrue(self.album.is_active)

    def test_album_str(self):
        """Testa representação string do álbum"""
        self.assertEqual(str(self.album), 'Test Album - Test Artist')

    def test_album_featured_default(self):
        """Testa valor padrão de featured"""
        self.assertFalse(self.album.featured)

    def test_album_musics_count(self):
        """Testa método get_musics_count"""
        # Nota: Este teste seria mais relevante se tivermos música criada
        # Por enquanto, apenas verifica que o método existe e retorna 0
        count = self.album.get_musics_count()
        self.assertEqual(count, 0)

    def test_album_ordering(self):
        """Testa ordenação de álbuns"""
        Album.objects.create(
            artist=self.artist,
            name='Featured Album',
            featured=True
        )
        Album.objects.create(
            artist=self.artist,
            name='Regular Album',
            featured=False
        )
        
        albums = Album.objects.filter(artist=self.artist)
        # O álbum featured deve aparecer primeiro devido à ordenação
        self.assertEqual(albums.first().featured, True)

    def test_album_artist_relationship(self):
        """Testa relacionamento entre álbum e artista"""
        self.assertEqual(self.album.artist.stage_name, 'Test Artist')
        
        # Teste via related_name
        albums = self.artist.albums.all()
        self.assertIn(self.album, albums)


class ArtistSerializerTest(TestCase):
    """Testes para serializers de Artist"""

    def setUp(self):
        self.genre = Genre.objects.create(name='Forró', slug='forro')
        self.artist = Artist.objects.create(
            stage_name='Serializer Artist',
            genre=self.genre
        )

    def test_artist_serializer(self):
        """Testa serialização de artista"""
        from .serializers import ArtistSerializer
        serializer = ArtistSerializer(self.artist)
        data = serializer.data
        
        self.assertEqual(data['stage_name'], 'Serializer Artist')
        self.assertIn('genre', data)
        self.assertIn('albums_count', data)

    def test_artist_create_serializer(self):
        """Testa criação de artista via serializer"""
        from .serializers import ArtistCreateSerializer
        data = {
            'stage_name': 'New Artist',
            'genre': self.genre.id
        }
        serializer = ArtistCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        artist = serializer.save()
        self.assertEqual(artist.stage_name, 'New Artist')

    def test_artist_create_serializer_validation(self):
        """Testa validação de nome artístico"""
        from .serializers import ArtistCreateSerializer
        data = {
            'stage_name': 'A',  # Muito curto
            'genre': self.genre.id
        }
        serializer = ArtistCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_album_serializer(self):
        """Testa serialização de álbum"""
        from .serializers import AlbumSerializer
        album = Album.objects.create(
            artist=self.artist,
            name='Serialized Album'
        )
        serializer = AlbumSerializer(album)
        data = serializer.data
        
        self.assertEqual(data['name'], 'Serialized Album')
        self.assertIn('artist_name', data)
        self.assertIn('musics_count', data)


class ArtistViewTest(TestCase):
    """Testes para views de Artist"""

    def setUp(self):
        self.client = APIClient()
        self.genre = Genre.objects.create(name='Forró', slug='forro')
        self.artist = Artist.objects.create(
            stage_name='View Artist',
            genre=self.genre
        )

    def test_artist_albums_integration(self):
        """Testa integração artista-álbuns"""
        Album.objects.create(artist=self.artist, name='Integration Album')
        
        # Verificar que o álbum foi criado
        albums = Album.objects.filter(artist=self.artist)
        self.assertEqual(albums.count(), 1)
        self.assertEqual(albums.first().name, 'Integration Album')

    def test_artist_with_album_relationship(self):
        """Testa relacionamento artista-album"""
        album = Album.objects.create(artist=self.artist, name='Relationship Album')
        
        # Via related_name
        self.assertEqual(self.artist.albums.count(), 1)
        self.assertIn(album, self.artist.albums.all())

    def test_album_featured_ordering(self):
        """Testa ordenação de álbuns por destaque"""
        Album.objects.create(artist=self.artist, name='Regular 1', featured=False)
        Album.objects.create(artist=self.artist, name='Featured 1', featured=True)
        Album.objects.create(artist=self.artist, name='Regular 2', featured=False)
        
        albums = Album.objects.filter(artist=self.artist).order_by('-featured')
        self.assertEqual(albums.first().featured, True)

    def test_artist_creation_with_genre(self):
        """Testa criação de artista com gênero"""
        artist = Artist.objects.create(
            stage_name='Genre Artist',
            genre=self.genre
        )
        
        self.assertEqual(artist.genre, self.genre)
        self.assertEqual(artist.genre.name, 'Forró')

