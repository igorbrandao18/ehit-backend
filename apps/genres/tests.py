from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Genre


class GenreModelTest(TestCase):
    """Testes para o modelo Genre"""

    def setUp(self):
        self.genre = Genre.objects.create(
            name='Forró',
            slug='forro',
            description='Gênero musical brasileiro',
            color='#FF6B6B',
            icon='music'
        )

    def test_genre_creation(self):
        """Testa criação de gênero"""
        self.assertEqual(self.genre.name, 'Forró')
        self.assertEqual(self.genre.slug, 'forro')
        self.assertTrue(self.genre.is_active)

    def test_genre_str(self):
        """Testa representação string do gênero"""
        self.assertEqual(str(self.genre), 'Forró')

    def test_genre_slug_auto_generation(self):
        """Testa geração automática de slug"""
        genre = Genre.objects.create(name='Pop Music')
        self.assertEqual(genre.slug, 'pop-music')

    def test_genre_unique_name(self):
        """Testa unicidade do nome"""
        with self.assertRaises(Exception):
            Genre.objects.create(name='Forró')

    def test_genre_unique_slug(self):
        """Testa unicidade do slug"""
        with self.assertRaises(Exception):
            Genre.objects.create(name='Different Name', slug='forro')

    def test_genre_defaults(self):
        """Testa valores padrão"""
        genre = Genre.objects.create(name='Rock')
        self.assertEqual(genre.color, '#FF6B6B')
        self.assertTrue(genre.is_active)

    def test_genre_parent_relationship(self):
        """Testa relacionamento de gênero pai"""
        parent = Genre.objects.create(name='Rock')
        child = Genre.objects.create(name='Heavy Metal', parent=parent)
        
        self.assertEqual(child.parent, parent)
        self.assertIn(child, parent.subgenres.all())

    def test_song_count_property(self):
        """Testa property song_count"""
        count = self.genre.song_count
        # Não há músicas ainda, então deve retornar 0
        self.assertEqual(count, 0)

    def test_artist_count_property(self):
        """Testa property artist_count"""
        count = self.genre.artist_count
        # Não há artistas ainda, então deve retornar 0
        self.assertEqual(count, 0)

    def test_genre_ordering(self):
        """Testa ordenação de gêneros"""
        Genre.objects.create(name='Zebra')
        Genre.objects.create(name='Apple')
        
        genres = Genre.objects.all()
        # Deve estar ordenado por nome (A-Z)
        self.assertEqual(genres[0].name, 'Apple')
        self.assertEqual(genres[1].name, 'Forró')

    def test_genre_is_active_filtering(self):
        """Testa filtro por is_active"""
        active_genre = Genre.objects.create(name='Active Genre', is_active=True)
        inactive_genre = Genre.objects.create(name='Inactive Genre', is_active=False)
        
        active_genres = Genre.objects.filter(is_active=True)
        self.assertIn(active_genre, active_genres)
        self.assertNotIn(inactive_genre, active_genres)

    def test_genre_with_subgenres(self):
        """Testa gênero com subgêneros"""
        parent = Genre.objects.create(name='Rock')
        child1 = Genre.objects.create(name='Heavy Metal', parent=parent)
        child2 = Genre.objects.create(name='Punk Rock', parent=parent)
        
        subgenres = parent.subgenres.all()
        self.assertEqual(subgenres.count(), 2)
        self.assertIn(child1, subgenres)
        self.assertIn(child2, subgenres)

    def test_genre_cascade_delete(self):
        """Testa exclusão em cascata do gênero pai"""
        parent = Genre.objects.create(name='Rock')
        child = Genre.objects.create(name='Heavy Metal', parent=parent)
        
        child_id = child.id
        parent.delete()
        
        # O subgênero deve ser deletado também
        self.assertFalse(Genre.objects.filter(id=child_id).exists())

    def test_genre_update_description(self):
        """Testa atualização de descrição"""
        self.genre.description = 'Nova descrição'
        self.genre.save()
        
        updated_genre = Genre.objects.get(id=self.genre.id)
        self.assertEqual(updated_genre.description, 'Nova descrição')

    def test_genre_color_update(self):
        """Testa atualização de cor"""
        self.genre.color = '#00FF00'
        self.genre.save()
        
        updated_genre = Genre.objects.get(id=self.genre.id)
        self.assertEqual(updated_genre.color, '#00FF00')

    def test_genre_icon_update(self):
        """Testa atualização de ícone"""
        self.genre.icon = 'guitar'
        self.genre.save()
        
        updated_genre = Genre.objects.get(id=self.genre.id)
        self.assertEqual(updated_genre.icon, 'guitar')

    def test_genre_toggle_is_active(self):
        """Testa alternância de is_active"""
        self.assertTrue(self.genre.is_active)
        
        self.genre.is_active = False
        self.genre.save()
        
        updated_genre = Genre.objects.get(id=self.genre.id)
        self.assertFalse(updated_genre.is_active)
        
        updated_genre.is_active = True
        updated_genre.save()
        
        re_updated_genre = Genre.objects.get(id=self.genre.id)
        self.assertTrue(re_updated_genre.is_active)

