from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
# from rest_framework.authtoken.models import Token
from apps.artists.models import Artist
from apps.music.models import Music
from apps.playlists.models import Playlist, UserFavorite

User = get_user_model()


class UsersAPITest(APITestCase):
    """Testes para a API de usuários"""
    
    def setUp(self):
        """Configuração inicial"""
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'user_type': 'listener'
        }
        
        # Criar usuário para testes
        self.user = User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='pass123',
            user_type='listener'
        )
        
        # Criar token para autenticação
        # self.token = Token.objects.create(user=self.user)
    
    def test_user_create(self):
        """Testa criação de usuário"""
        url = '/api/users/create/'
        response = self.client.post(url, self.user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')
    
    def test_user_create_invalid_data(self):
        """Testa criação de usuário com dados inválidos"""
        url = '/api/users/create/'
        invalid_data = self.user_data.copy()
        invalid_data['password_confirm'] = 'different_password'
        
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
    
    def test_user_login(self):
        """Testa login de usuário"""
        url = '/api/users/login/'
        login_data = {
            'username': 'existinguser',
            'password': 'pass123'
        }
        
        response = self.client.post(url, login_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['username'], 'existinguser')
    
    def test_user_login_invalid_credentials(self):
        """Testa login com credenciais inválidas"""
        url = '/api/users/login/'
        login_data = {
            'username': 'existinguser',
            'password': 'wrong_password'
        }
        
        response = self.client.post(url, login_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
    
    def test_user_list(self):
        """Testa listagem de usuários"""
        url = '/api/users/'
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_user_profile(self):
        """Testa obtenção do perfil do usuário"""
        url = '/api/users/profile/'
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'existinguser')
        self.assertEqual(response.data['email'], 'existing@example.com')
    
    def test_user_profile_update(self):
        """Testa atualização do perfil"""
        url = '/api/users/profile/update/'
        self.client.force_authenticate(user=self.user)
        
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'bio': 'Updated bio'
        }
        
        response = self.client.patch(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Updated')
        self.assertEqual(response.data['last_name'], 'Name')
        self.assertEqual(response.data['bio'], 'Updated bio')
    
    def test_change_password(self):
        """Testa alteração de senha"""
        url = '/api/users/change-password/'
        self.client.force_authenticate(user=self.user)
        
        password_data = {
            'old_password': 'pass123',
            'new_password': 'newpass123',
            'confirm_password': 'newpass123'
        }
        
        response = self.client.post(url, password_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
    
    def test_user_stats(self):
        """Testa estatísticas do usuário"""
        url = '/api/users/stats/'
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('followers_count', response.data)
        self.assertIn('user_type', response.data)
    
    def test_user_list_with_filters(self):
        """Testa listagem com filtros"""
        url = '/api/users/'
        self.client.force_authenticate(user=self.user)
        
        # Teste com filtro de tipo
        response = self.client.get(url, {'user_type': 'listener'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Teste com busca
        response = self.client.get(url, {'search': 'existing'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_user_list_pagination(self):
        """Testa paginação na listagem"""
        url = '/api/users/'
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(url, {'page_size': 1})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
