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


class AllEndpointsTest(APITestCase):
    """Testes para todos os endpoints da API"""
    
    def setUp(self):
        """Configuração inicial"""
        self.client = APIClient()
        
        # Criar usuário artista
        self.artist_user = User.objects.create_user(
            username='artistuser',
            email='artist@example.com',
            password='pass123',
            user_type='artist'
        )
        
        # Criar artista
        self.artist = Artist.objects.create(
            user=self.artist_user,
            stage_name='Test Artist',
            genre='Rock',
            verified=True
        )
        
        # Criar músicas
        self.music1 = Music.objects.create(
            artist=self.artist,
            title='Song 1',
            album='Album 1',
            genre='Rock',
            duration=240,
            streams_count=1000,
            downloads_count=100,
            likes_count=50,
            is_featured=True
        )
        
        self.music2 = Music.objects.create(
            artist=self.artist,
            title='Song 2',
            album='Album 1',
            genre='Rock',
            duration=180,
            streams_count=2000,
            downloads_count=200,
            likes_count=100,
            is_featured=False
        )
        
        # Criar usuário comum
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='pass123',
            user_type='listener'
        )
        
        # Criar playlist
        self.playlist = Playlist.objects.create(
            user=self.user,
            name='My Playlist',
            description='Test playlist',
            is_public=True,
            followers_count=10
        )
        
        # Adicionar músicas à playlist
        self.playlist.add_music(self.music1, order=0)
        self.playlist.add_music(self.music2, order=1)
        
        # Criar token para autenticação
        # self.token = Token.objects.create(user=self.user)
    
    def test_all_endpoints_exist(self):
        """Testa se todos os endpoints existem e respondem"""
        endpoints = [
            # API Index
            ('/api/', 'GET'),
            
            # Users
            ('/api/users/', 'GET'),
            ('/api/users/create/', 'POST'),
            ('/api/users/login/', 'POST'),
            ('/api/users/profile/', 'GET'),
            ('/api/users/profile/update/', 'PATCH'),
            ('/api/users/change-password/', 'POST'),
            ('/api/users/stats/', 'GET'),
            
            # Artists
            ('/api/artists/', 'GET'),
            ('/api/artists/create/', 'POST'),
            ('/api/artists/popular/', 'GET'),
            ('/api/artists/trending/', 'GET'),
            ('/api/artists/genres/', 'GET'),
            
            # Music
            ('/api/music/', 'GET'),
            ('/api/music/create/', 'POST'),
            ('/api/music/trending/', 'GET'),
            ('/api/music/popular/', 'GET'),
            ('/api/music/featured/', 'GET'),
            ('/api/music/genres/', 'GET'),
            ('/api/music/albums/', 'GET'),
            
            # Playlists
            ('/api/playlists/', 'GET'),
            ('/api/playlists/create/', 'POST'),
            ('/api/playlists/my/', 'GET'),
            ('/api/playlists/public/', 'GET'),
            ('/api/playlists/popular/', 'GET'),
            ('/api/playlists/favorites/', 'GET'),
        ]
        
        for endpoint, method in endpoints:
            if method == 'GET':
                response = self.client.get(endpoint)
            elif method == 'POST':
                response = self.client.post(endpoint, {}, format='json')
            elif method == 'PATCH':
                response = self.client.patch(endpoint, {}, format='json')
            
            # Verificar se o endpoint existe (não deve retornar 404)
            self.assertNotEqual(response.status_code, 404, 
                               f"Endpoint {endpoint} não encontrado")
            
            # Verificar se retorna um status válido
            self.assertIn(response.status_code, [200, 201, 400, 401, 405], 
                          f"Endpoint {endpoint} retornou status inválido: {response.status_code}")
    
    def test_endpoint_specific_responses(self):
        """Testa respostas específicas de cada endpoint"""
        # API Index
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('endpoints', response.data)
        
        # Users List
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        
        # Artists List
        response = self.client.get('/api/artists/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        
        # Music List
        response = self.client.get('/api/music/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        
        # Playlists List
        response = self.client.get('/api/playlists/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
    
    def test_endpoint_authentication(self):
        """Testa autenticação nos endpoints"""
        # Endpoints que requerem autenticação
        auth_required = [
            '/api/users/profile/',
            '/api/users/change-password/',
            '/api/users/stats/',
            '/api/artists/create/',
            '/api/music/create/',
            '/api/playlists/create/',
            '/api/playlists/my/',
            '/api/playlists/favorites/',
        ]
        
        for endpoint in auth_required:
            response = self.client.get(endpoint)
            self.assertEqual(response.status_code, 401, 
                           f"Endpoint {endpoint} deveria requerer autenticação")
        
        # Endpoints públicos
        public_endpoints = [
            '/api/',
            '/api/users/create/',
            '/api/users/login/',
            '/api/artists/',
            '/api/music/',
            '/api/playlists/',
            '/api/playlists/public/',
            '/api/playlists/popular/',
        ]
        
        for endpoint in public_endpoints:
            response = self.client.get(endpoint)
            self.assertIn(response.status_code, [200, 405], 
                         f"Endpoint {endpoint} deveria ser público")
    
    def test_endpoint_methods(self):
        """Testa métodos HTTP dos endpoints"""
        # Testar métodos permitidos
        methods_tests = [
            ('/api/users/', ['GET']),
            ('/api/users/create/', ['POST']),
            ('/api/users/login/', ['POST']),
            ('/api/artists/', ['GET']),
            ('/api/artists/create/', ['POST']),
            ('/api/music/', ['GET']),
            ('/api/music/create/', ['POST']),
            ('/api/playlists/', ['GET']),
            ('/api/playlists/create/', ['POST']),
        ]
        
        for endpoint, allowed_methods in methods_tests:
            for method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
                if method == 'GET':
                    response = self.client.get(endpoint)
                elif method == 'POST':
                    response = self.client.post(endpoint, {}, format='json')
                elif method == 'PUT':
                    response = self.client.put(endpoint, {}, format='json')
                elif method == 'PATCH':
                    response = self.client.patch(endpoint, {}, format='json')
                elif method == 'DELETE':
                    response = self.client.delete(endpoint)
                
                if method in allowed_methods:
                    self.assertNotEqual(response.status_code, 405, 
                                      f"Método {method} deveria ser permitido em {endpoint}")
                else:
                    self.assertEqual(response.status_code, 405, 
                                   f"Método {method} não deveria ser permitido em {endpoint}")
    
    def test_endpoint_data_structure(self):
        """Testa estrutura de dados dos endpoints"""
        # Testar estrutura de listagem
        list_endpoints = [
            '/api/users/',
            '/api/artists/',
            '/api/music/',
            '/api/playlists/',
        ]
        
        for endpoint in list_endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(response.status_code, 200)
            
            # Verificar estrutura de paginação
            self.assertIn('count', response.data)
            self.assertIn('results', response.data)
            self.assertIn('next', response.data)
            self.assertIn('previous', response.data)
            
            # Verificar que results é uma lista
            self.assertIsInstance(response.data['results'], list)
    
    def test_endpoint_error_handling(self):
        """Testa tratamento de erros nos endpoints"""
        # Testar 404 para recursos inexistentes
        not_found_tests = [
            '/api/users/999/',
            '/api/artists/999/',
            '/api/music/999/',
            '/api/playlists/999/',
        ]
        
        for endpoint in not_found_tests:
            response = self.client.get(endpoint)
            self.assertEqual(response.status_code, 404)
        
        # Testar 400 para dados inválidos
        invalid_data_tests = [
            ('/api/users/create/', {'username': '', 'password': ''}),
            ('/api/artists/create/', {'stage_name': ''}),
            ('/api/music/create/', {'title': ''}),
            ('/api/playlists/create/', {'name': ''}),
        ]
        
        for endpoint, data in invalid_data_tests:
            self.client.force_authenticate(user=self.artist_user)
            response = self.client.post(endpoint, data, format='json')
            self.assertEqual(response.status_code, 400)
    
    def test_endpoint_performance(self):
        """Testa performance dos endpoints"""
        import time
        
        # Testar tempo de resposta dos endpoints principais
        performance_tests = [
            '/api/',
            '/api/users/',
            '/api/artists/',
            '/api/music/',
            '/api/playlists/',
        ]
        
        for endpoint in performance_tests:
            start_time = time.time()
            response = self.client.get(endpoint)
            end_time = time.time()
            
            response_time = end_time - start_time
            
            # Verificar que a resposta é rápida (menos de 1 segundo)
            self.assertLess(response_time, 1.0, 
                           f"Endpoint {endpoint} demorou muito para responder: {response_time:.2f}s")
            
            # Verificar que retorna status válido
            self.assertIn(response.status_code, [200, 201, 400, 401, 405])
    
    def test_endpoint_consistency(self):
        """Testa consistência dos endpoints"""
        # Verificar que todos os endpoints de listagem têm a mesma estrutura
        list_endpoints = [
            '/api/users/',
            '/api/artists/',
            '/api/music/',
            '/api/playlists/',
        ]
        
        for endpoint in list_endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(response.status_code, 200)
            
            # Verificar campos obrigatórios
            required_fields = ['count', 'results', 'next', 'previous']
            for field in required_fields:
                self.assertIn(field, response.data, 
                             f"Campo {field} ausente em {endpoint}")
            
            # Verificar tipos de dados
            self.assertIsInstance(response.data['count'], int)
            self.assertIsInstance(response.data['results'], list)
            self.assertIsInstance(response.data['next'], (str, type(None)))
            self.assertIsInstance(response.data['previous'], (str, type(None)))
    
    def test_endpoint_security(self):
        """Testa segurança dos endpoints"""
        # Verificar que endpoints sensíveis requerem autenticação
        sensitive_endpoints = [
            '/api/users/profile/',
            '/api/users/change-password/',
            '/api/users/stats/',
            '/api/artists/create/',
            '/api/music/create/',
            '/api/playlists/create/',
            '/api/playlists/my/',
            '/api/playlists/favorites/',
        ]
        
        for endpoint in sensitive_endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(response.status_code, 401, 
                           f"Endpoint {endpoint} deveria requerer autenticação")
        
        # Verificar que endpoints públicos não expõem dados sensíveis
        public_endpoints = [
            '/api/users/',
            '/api/artists/',
            '/api/music/',
            '/api/playlists/',
        ]
        
        for endpoint in public_endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(response.status_code, 200)
            
            # Verificar que não expõe senhas ou tokens
            response_text = str(response.data)
            self.assertNotIn('password', response_text.lower())
            self.assertNotIn('token', response_text.lower())
            self.assertNotIn('secret', response_text.lower())
