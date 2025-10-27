from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.test import APIRequestFactory
from unittest.mock import patch
from .models import User

User = get_user_model()


class UserModelTest(TestCase):
    """Testes para o modelo User"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            user_type='listener'
        )

    def test_user_creation(self):
        """Testa criação de usuário"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.user_type, 'listener')
        self.assertTrue(self.user.is_active)

    def test_user_str(self):
        """Testa representação string do usuário"""
        self.assertEqual(str(self.user), 'testuser (Ouvinte)')

    def test_is_artist_property(self):
        """Testa property is_artist"""
        self.assertFalse(self.user.is_artist)
        self.user.user_type = 'artist'
        self.assertTrue(self.user.is_artist)

    def test_is_venue_property(self):
        """Testa property is_venue"""
        self.assertFalse(self.user.is_venue)
        self.user.user_type = 'venue'
        self.assertTrue(self.user.is_venue)

    def test_is_admin_property(self):
        """Testa property is_admin"""
        self.assertFalse(self.user.is_admin)
        self.user.user_type = 'admin'
        self.assertTrue(self.user.is_admin)

    def test_followers_count_default(self):
        """Testa contador de seguidores padrão"""
        self.assertEqual(self.user.followers_count, 0)

    def test_verified_default(self):
        """Testa status de verificação padrão"""
        self.assertFalse(self.user.verified)


class UserSerializerTest(TestCase):
    """Testes para serializers de User"""

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password_confirm': 'newpass123',
            'first_name': 'New',
            'last_name': 'User',
            'user_type': 'listener'
        }

    def test_create_user_serializer(self):
        """Testa criação de usuário via serializer"""
        from .serializers import UserCreateSerializer
        serializer = UserCreateSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, 'newuser')
        self.assertTrue(user.check_password('newpass123'))

    def test_password_mismatch(self):
        """Testa validação de senha não coincidindo"""
        from .serializers import UserCreateSerializer
        self.user_data['password_confirm'] = 'differentpass'
        serializer = UserCreateSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())

    def test_full_name_method(self):
        """Testa método get_full_name"""
        from .serializers import UserSerializer
        user = User.objects.create_user(
            username='fullname',
            email='full@example.com',
            password='test123',
            first_name='John',
            last_name='Doe'
        )
        serializer = UserSerializer(user)
        self.assertEqual(serializer.data['full_name'], 'John Doe')


class UserSerializerIntegrationTest(TestCase):
    """Testes de integração com serializers de User"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='integration',
            email='integration@example.com',
            password='testpass123',
            user_type='listener'
        )

    def test_user_password_set_correctly(self):
        """Testa que a senha é configurada corretamente"""
        self.assertTrue(self.user.check_password('testpass123'))
        self.assertFalse(self.user.check_password('wrongpass'))

    def test_user_update_fields(self):
        """Testa atualização de campos do usuário"""
        self.user.first_name = 'Updated'
        self.user.bio = 'New bio'
        self.user.save()
        
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.first_name, 'Updated')
        self.assertEqual(updated_user.bio, 'New bio')

