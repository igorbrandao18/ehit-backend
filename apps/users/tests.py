from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError

User = get_user_model()


class UserModelTest(TestCase):
    """Testes para o modelo User customizado"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'user_type': 'listener',
            'first_name': 'Test',
            'last_name': 'User',
            'bio': 'Test user bio',
            'phone': '1234567890',
            'location': 'Test City',
            'verified': False
        }
    
    def test_create_user(self):
        """Testa criação de usuário comum"""
        user = User.objects.create_user(**self.user_data)
        
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.user_type, 'listener')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.bio, 'Test user bio')
        self.assertEqual(user.phone, '1234567890')
        self.assertEqual(user.location, 'Test City')
        self.assertFalse(user.verified)
        self.assertEqual(user.followers_count, 0)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser(self):
        """Testa criação de superusuário"""
        superuser_data = self.user_data.copy()
        superuser_data.update({
            'username': 'admin',
            'user_type': 'admin',
            'is_staff': True,
            'is_superuser': True
        })
        
        superuser = User.objects.create_superuser(**superuser_data)
        
        self.assertEqual(superuser.username, 'admin')
        self.assertEqual(superuser.user_type, 'admin')
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)
    
    def test_user_str_representation(self):
        """Testa representação string do usuário"""
        user = User.objects.create_user(**self.user_data)
        expected = f"{user.username} ({user.get_user_type_display()})"
        self.assertEqual(str(user), expected)
    
    def test_user_type_properties(self):
        """Testa propriedades de tipo de usuário"""
        # Teste para listener
        listener = User.objects.create_user(
            username='listener', email='listener@test.com', password='pass123'
        )
        self.assertTrue(listener.is_authenticated)
        
        # Teste para artist
        artist = User.objects.create_user(
            username='artist', email='artist@test.com', password='pass123',
            user_type='artist'
        )
        self.assertTrue(artist.is_artist)
        self.assertFalse(artist.is_venue)
        self.assertFalse(artist.is_admin)
        
        # Teste para venue
        venue = User.objects.create_user(
            username='venue', email='venue@test.com', password='pass123',
            user_type='venue'
        )
        self.assertTrue(venue.is_venue)
        self.assertFalse(venue.is_artist)
        self.assertFalse(venue.is_admin)
        
        # Teste para admin
        admin = User.objects.create_user(
            username='admin', email='admin@test.com', password='pass123',
            user_type='admin'
        )
        self.assertTrue(admin.is_admin)
        self.assertFalse(admin.is_artist)
        self.assertFalse(admin.is_venue)
    
    def test_user_type_choices(self):
        """Testa escolhas válidas de tipo de usuário"""
        valid_types = ['listener', 'artist', 'venue', 'admin']
        
        for user_type in valid_types:
            user = User.objects.create_user(
                username=f'user_{user_type}',
                email=f'{user_type}@test.com',
                password='pass123',
                user_type=user_type
            )
            self.assertEqual(user.user_type, user_type)
    
    def test_user_ordering(self):
        """Testa ordenação padrão dos usuários"""
        user1 = User.objects.create_user(
            username='user1', email='user1@test.com', password='pass123'
        )
        user2 = User.objects.create_user(
            username='user2', email='user2@test.com', password='pass123'
        )
        
        users = User.objects.all()
        # Deve estar ordenado por -date_joined (mais recente primeiro)
        self.assertEqual(users[0], user2)
        self.assertEqual(users[1], user1)
    
    def test_user_required_fields(self):
        """Testa campos obrigatórios"""
        # Testar criação de usuário com campos válidos
        user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='pass123'
        )
        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@test.com')
        
        # Testar que usuário foi criado com sucesso
        self.assertTrue(User.objects.filter(username='testuser').exists())
    
    def test_user_followers_count(self):
        """Testa contador de seguidores"""
        user = User.objects.create_user(**self.user_data)
        
        # Inicialmente deve ser 0
        self.assertEqual(user.followers_count, 0)
        
        # Deve permitir incrementar
        user.followers_count = 100
        user.save()
        self.assertEqual(user.followers_count, 100)
    
    def test_user_verification(self):
        """Testa sistema de verificação"""
        user = User.objects.create_user(**self.user_data)
        
        # Inicialmente não verificado
        self.assertFalse(user.verified)
        
        # Deve permitir verificar
        user.verified = True
        user.save()
        self.assertTrue(user.verified)


class UserManagerTest(TestCase):
    """Testes para o manager de usuários"""
    
    def test_create_user_without_password(self):
        """Testa criação de usuário sem senha"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com'
        )
        self.assertFalse(user.has_usable_password())
    
    def test_create_user_with_password(self):
        """Testa criação de usuário com senha"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertTrue(user.has_usable_password())
        self.assertTrue(user.check_password('testpass123'))
    
    def test_create_superuser_validation(self):
        """Testa validação na criação de superusuário"""
        # Deve falhar se is_staff=False
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username='admin',
                email='admin@test.com',
                password='pass123',
                is_staff=False
            )
        
        # Deve falhar se is_superuser=False
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username='admin',
                email='admin@test.com',
                password='pass123',
                is_superuser=False
            )
