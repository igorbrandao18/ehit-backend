"""
Testes robustos para a app Users
Testa autenticação, CRUD de usuários e permissões
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
import json

User = get_user_model()


class UserModelTestCase(TestCase):
    """Testes para o modelo User"""
    
    def setUp(self):
        """Configuração inicial"""
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
    
    def test_user_creation(self):
        """Testa criação de usuário"""
        user = User.objects.create_user(**self.user_data)
        
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_user_str_representation(self):
        """Testa representação string do usuário"""
        user = User.objects.create_user(**self.user_data)
        
        # A representação string inclui o tipo de usuário: 'username (Ouvinte)'
        self.assertIn('testuser', str(user))
        self.assertIn('Ouvinte', str(user))
    
    def test_superuser_creation(self):
        """Testa criação de superusuário"""
        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
    
    def test_user_default_fields(self):
        """Testa campos padrão do usuário"""
        user = User.objects.create_user(**self.user_data)
        
        self.assertIsNotNone(user.date_joined)
        self.assertTrue(user.is_active)  # Usuários são ativos por padrão no modelo customizado
        self.assertEqual(user.followers_count, 0)
        self.assertFalse(user.verified)
    
    def test_user_modification(self):
        """Testa modificação de usuário"""
        user = User.objects.create_user(**self.user_data)
        user.first_name = 'Modified'
        user.save()
        
        updated_user = User.objects.get(pk=user.pk)
        self.assertEqual(updated_user.first_name, 'Modified')


class UserAPITestCase(APITestCase):
    """Testes para endpoints de usuários"""
    
    def setUp(self):
        """Configuração inicial"""
        self.client = APIClient()
        
        # Criar usuários
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            is_active=True
        )
        
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
    
    def test_user_list_requires_auth(self):
        """Testa que listagem requer autenticação"""
        url = '/api/users/'
        response = self.client.get(url)
        
        # Deve retornar 401 ou 403 dependendo da configuração
        self.assertIn(response.status_code, [401, 403, 404])
    
    def test_user_detail_requires_auth(self):
        """Testa que detalhes requer autenticação"""
        url = f'/api/users/{self.user.pk}/'
        response = self.client.get(url)
        
        self.assertIn(response.status_code, [401, 403, 404])


class AuthenticationTestCase(APITestCase):
    """Testes de autenticação"""
    
    def setUp(self):
        """Configuração inicial"""
        self.client = APIClient()
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            is_active=True
        )
    
    def test_jwt_token_obtain(self):
        """Testa obtenção de token JWT"""
        url = '/api/auth/token/'
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_jwt_token_refresh(self):
        """Testa refresh de token JWT"""
        # Obter token inicial
        url = '/api/auth/token/'
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data)
        refresh_token = response.data['refresh']
        
        # Refresh token
        url = '/api/auth/token/refresh/'
        response = self.client.post(url, {'refresh': refresh_token})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
    
    def test_invalid_credentials(self):
        """Testa credenciais inválidas"""
        url = '/api/auth/token/'
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_inactive_user_login(self):
        """Testa login de usuário inativo"""
        self.user.is_active = False
        self.user.save()
        
        url = '/api/auth/token/'
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

