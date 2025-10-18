#!/usr/bin/env python3
import os
import sys
import requests
import json
from datetime import date

# Configuração da API
BASE_URL = "http://prod.ehitapp.com.br/api"
ARTISTS_URL = f"{BASE_URL}/artists/"
MUSIC_URL = f"{BASE_URL}/music/"
TOKEN_URL = f"{BASE_URL}/auth/token/"

def login():
    """Fazer login na API e obter JWT token"""
    login_data = {
        'username': 'rai_saia_rodada',
        'password': 'test123'
    }
    
    try:
        response = requests.post(TOKEN_URL, json=login_data)
        if response.status_code == 200:
            data = response.json()
            print(f'✅ Login realizado com sucesso!')
            print(f'🔑 Access Token obtido (válido por 60 minutos)')
            return data.get('access_token')
        else:
            print(f'❌ Erro no login: {response.status_code} - {response.text}')
            return None
    except Exception as e:
        print(f'❌ Erro na requisição de login: {e}')
        return None

def get_artist():
    """Buscar o artista Rai Saia Rodada"""
    try:
        # Buscar todos os artistas
        response = requests.get(ARTISTS_URL)
        if response.status_code == 200:
            artists = response.json().get('results', [])
            for artist in artists:
                if artist['stage_name'] == 'Rai Saia Rodada':
                    print(f'✅ Artista encontrado: {artist["stage_name"]} (ID: {artist["id"]})')
                    return artist
            
            print('❌ Artista Rai Saia Rodada não encontrado')
            return None
        else:
            print(f'❌ Erro ao buscar artistas: {response.status_code}')
            return None
    except Exception as e:
        print(f'❌ Erro na requisição: {e}')
        return None

def upload_music_file(file_path, music_data, token):
    """Fazer upload de uma música via API"""
    try:
        # Preparar dados da música
        music_payload = {
            'title': music_data['title'],
            'album': music_data['album'],
            'genre': music_data['genre'],
            'duration': music_data['duration'],
            'release_date': music_data['release_date']
        }
        
        # Preparar headers com autenticação
        headers = {}
        if token:
            headers['Authorization'] = f'Bearer {token}'
        
        # Preparar arquivo
        with open(file_path, 'rb') as audio_file:
            files = {
                'file': (os.path.basename(file_path), audio_file, 'audio/mpeg')
            }
            
            # Fazer upload
            response = requests.post(
                f"{MUSIC_URL}create/",
                data=music_payload,
                files=files,
                headers=headers
            )
            
            if response.status_code == 201:
                print(f'✅ Música enviada: {music_data["title"]}')
                return response.json()
            else:
                print(f'❌ Erro ao enviar música {music_data["title"]}: {response.status_code} - {response.text}')
                return None
                
    except Exception as e:
        print(f'❌ Erro no upload da música {music_data["title"]}: {e}')
        return None

def main():
    print("🔐 Fazendo login...")
    token = login()
    
    if not token:
        print("❌ Não foi possível fazer login. Abortando.")
        return
    
    print("🎤 Buscando artista Rai Saia Rodada...")
    artist = get_artist()
    
    if not artist:
        print("❌ Não foi possível encontrar o artista. Abortando.")
        return
    
    print(f"🎤 Artista ID: {artist['id']}")
    
    # Músicas do álbum "E FORRO PRONTO"
    music_data = [
        {
            'title': 'Lágrimas De Chuva',
            'duration': 468,  # 7:48 em segundos
            'genre': 'folk',
            'release_date': '2024-01-01',
            'album': 'E FORRO PRONTO',
            'file_path': '/opt/ehit_backend/media/albums/Rai Saia Rodada - E FORRO PRONTO/01 - Lágrimas De Chuva.mp3'
        },
        {
            'title': 'Adultério',
            'duration': 258,  # 4:18 em segundos
            'genre': 'folk',
            'release_date': '2024-01-01',
            'album': 'E FORRO PRONTO',
            'file_path': '/opt/ehit_backend/media/albums/Rai Saia Rodada - E FORRO PRONTO/02 - Adultério.mp3'
        },
        {
            'title': 'Tá Comigo Pra quê?',
            'duration': 354,  # 5:54 em segundos
            'genre': 'folk',
            'release_date': '2024-01-01',
            'album': 'E FORRO PRONTO',
            'file_path': '/opt/ehit_backend/media/albums/Rai Saia Rodada - E FORRO PRONTO/03 - Tá Comigo Pra quê-.mp3'
        },
        {
            'title': 'Me Deixou Doidin',
            'duration': 228,  # 3:48 em segundos
            'genre': 'folk',
            'release_date': '2024-01-01',
            'album': 'E FORRO PRONTO',
            'file_path': '/opt/ehit_backend/media/albums/Rai Saia Rodada - E FORRO PRONTO/04 - Me Deixou Doidin.mp3'
        },
        {
            'title': 'Adoro Me Amarro',
            'duration': 438,  # 7:18 em segundos
            'genre': 'folk',
            'release_date': '2024-01-01',
            'album': 'E FORRO PRONTO',
            'file_path': '/opt/ehit_backend/media/albums/Rai Saia Rodada - E FORRO PRONTO/05 - Adoro Me Amarro.mp3'
        },
        {
            'title': 'Boca Rodada',
            'duration': 324,  # 5:24 em segundos
            'genre': 'folk',
            'release_date': '2024-01-01',
            'album': 'E FORRO PRONTO',
            'file_path': '/opt/ehit_backend/media/albums/Rai Saia Rodada - E FORRO PRONTO/06 - Boca Rodada.mp3'
        },
        {
            'title': 'Motelzim',
            'duration': 504,  # 8:24 em segundos
            'genre': 'folk',
            'release_date': '2024-01-01',
            'album': 'E FORRO PRONTO',
            'file_path': '/opt/ehit_backend/media/albums/Rai Saia Rodada - E FORRO PRONTO/07 - Motelzim.mp3'
        },
        {
            'title': 'Tô Sossegado',
            'duration': 414,  # 6:54 em segundos
            'genre': 'folk',
            'release_date': '2024-01-01',
            'album': 'E FORRO PRONTO',
            'file_path': '/opt/ehit_backend/media/albums/Rai Saia Rodada - E FORRO PRONTO/08 - Tô Sossegado.mp3'
        },
        {
            'title': 'Nasci Pra Ser Vaqueiro',
            'duration': 366,  # 6:06 em segundos
            'genre': 'folk',
            'release_date': '2024-01-01',
            'album': 'E FORRO PRONTO',
            'file_path': '/opt/ehit_backend/media/albums/Rai Saia Rodada - E FORRO PRONTO/09 - Nasci Pra Ser Vaqueiro.mp3'
        },
        {
            'title': 'Cor Morena',
            'duration': 360,  # 6:00 em segundos
            'genre': 'folk',
            'release_date': '2024-01-01',
            'album': 'E FORRO PRONTO',
            'file_path': '/opt/ehit_backend/media/albums/Rai Saia Rodada - E FORRO PRONTO/10 - Cor Morena.mp3'
        },
        {
            'title': 'Voando Baixo',
            'duration': 576,  # 9:36 em segundos
            'genre': 'folk',
            'release_date': '2024-01-01',
            'album': 'E FORRO PRONTO',
            'file_path': '/opt/ehit_backend/media/albums/Rai Saia Rodada - E FORRO PRONTO/11 - Voando Baixo.mp3'
        },
        {
            'title': 'Tô Rico',
            'duration': 324,  # 5:24 em segundos
            'genre': 'folk',
            'release_date': '2024-01-01',
            'album': 'E FORRO PRONTO',
            'file_path': '/opt/ehit_backend/media/albums/Rai Saia Rodada - E FORRO PRONTO/12 - Tô Rico.mp3'
        },
        {
            'title': 'Pra quê?',
            'duration': 408,  # 6:48 em segundos
            'genre': 'folk',
            'release_date': '2024-01-01',
            'album': 'E FORRO PRONTO',
            'file_path': '/opt/ehit_backend/media/albums/Rai Saia Rodada - E FORRO PRONTO/13 - Pra quê-.mp3'
        }
    ]
    
    print(f"\n🎵 Fazendo upload de {len(music_data)} músicas...")
    
    uploaded_count = 0
    for music_info in music_data:
        if os.path.exists(music_info['file_path']):
            result = upload_music_file(music_info['file_path'], music_info, token)
            if result:
                uploaded_count += 1
        else:
            print(f"❌ Arquivo não encontrado: {music_info['file_path']}")
    
    print(f"\n🎉 Upload concluído!")
    print(f"📊 Músicas enviadas: {uploaded_count}/{len(music_data)}")
    print(f"🌐 Acesse: http://prod.ehitapp.com.br/api/music/")

if __name__ == '__main__':
    main()
