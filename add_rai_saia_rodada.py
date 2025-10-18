#!/usr/bin/env python3
import os
import sys
import django
import random
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ehit_backend.settings')
django.setup()

from apps.users.models import User
from apps.artists.models import Artist
from apps.music.models import Music

# Criar usuário para Rai Saia Rodada
user, created = User.objects.get_or_create(
    username='rai_saia_rodada',
    defaults={
        'email': 'rai@raisaiarodada.com',
        'first_name': 'Rai',
        'last_name': 'Saia Rodada',
    }
)
if created:
    user.set_password('test123')
    user.save()
    print(f'✅ Usuário criado: {user.username}')
else:
    print(f'ℹ️ Usuário já existe: {user.username}')

# Criar artista Rai Saia Rodada
artist_data = {
    'stage_name': 'Rai Saia Rodada',
    'bio': 'Cantor de forró conhecido por hits como "Lágrimas De Chuva" e "Boca Rodada"',
    'genre': 'folk',  # Usando folk como gênero mais próximo do forró
    'verified': True,
    'location': 'Nordeste, Brasil',
    'user': user
}

artist, created = Artist.objects.get_or_create(
    stage_name=artist_data['stage_name'],
    defaults=artist_data
)
if created:
    print(f'✅ Artista criado: {artist.stage_name}')
else:
    print(f'ℹ️ Artista já existe: {artist.stage_name}')

# Músicas do álbum "E FORRO PRONTO"
music_data = [
    {
        'title': 'Lágrimas De Chuva',
        'duration': 468,  # 7:48 em segundos
        'genre': 'folk',
        'release_date': '2024-01-01',
        'file_path': 'albums/Rai Saia Rodada - E FORRO PRONTO/01 - Lágrimas De Chuva.mp3'
    },
    {
        'title': 'Adultério',
        'duration': 258,  # 4:18 em segundos
        'genre': 'folk',
        'release_date': '2024-01-01',
        'file_path': 'albums/Rai Saia Rodada - E FORRO PRONTO/02 - Adultério.mp3'
    },
    {
        'title': 'Tá Comigo Pra quê?',
        'duration': 354,  # 5:54 em segundos
        'genre': 'folk',
        'release_date': '2024-01-01',
        'file_path': 'albums/Rai Saia Rodada - E FORRO PRONTO/03 - Tá Comigo Pra quê-.mp3'
    },
    {
        'title': 'Me Deixou Doidin',
        'duration': 228,  # 3:48 em segundos
        'genre': 'folk',
        'release_date': '2024-01-01',
        'file_path': 'albums/Rai Saia Rodada - E FORRO PRONTO/04 - Me Deixou Doidin.mp3'
    },
    {
        'title': 'Adoro Me Amarro',
        'duration': 438,  # 7:18 em segundos
        'genre': 'folk',
        'release_date': '2024-01-01',
        'file_path': 'albums/Rai Saia Rodada - E FORRO PRONTO/05 - Adoro Me Amarro.mp3'
    },
    {
        'title': 'Boca Rodada',
        'duration': 324,  # 5:24 em segundos
        'genre': 'folk',
        'release_date': '2024-01-01',
        'file_path': 'albums/Rai Saia Rodada - E FORRO PRONTO/06 - Boca Rodada.mp3'
    },
    {
        'title': 'Motelzim',
        'duration': 504,  # 8:24 em segundos
        'genre': 'folk',
        'release_date': '2024-01-01',
        'file_path': 'albums/Rai Saia Rodada - E FORRO PRONTO/07 - Motelzim.mp3'
    },
    {
        'title': 'Tô Sossegado',
        'duration': 414,  # 6:54 em segundos
        'genre': 'folk',
        'release_date': '2024-01-01',
        'file_path': 'albums/Rai Saia Rodada - E FORRO PRONTO/08 - Tô Sossegado.mp3'
    },
    {
        'title': 'Nasci Pra Ser Vaqueiro',
        'duration': 366,  # 6:06 em segundos
        'genre': 'folk',
        'release_date': '2024-01-01',
        'file_path': 'albums/Rai Saia Rodada - E FORRO PRONTO/09 - Nasci Pra Ser Vaqueiro.mp3'
    },
    {
        'title': 'Cor Morena',
        'duration': 360,  # 6:00 em segundos
        'genre': 'folk',
        'release_date': '2024-01-01',
        'file_path': 'albums/Rai Saia Rodada - E FORRO PRONTO/10 - Cor Morena.mp3'
    },
    {
        'title': 'Voando Baixo',
        'duration': 576,  # 9:36 em segundos
        'genre': 'folk',
        'release_date': '2024-01-01',
        'file_path': 'albums/Rai Saia Rodada - E FORRO PRONTO/11 - Voando Baixo.mp3'
    },
    {
        'title': 'Tô Rico',
        'duration': 324,  # 5:24 em segundos
        'genre': 'folk',
        'release_date': '2024-01-01',
        'file_path': 'albums/Rai Saia Rodada - E FORRO PRONTO/12 - Tô Rico.mp3'
    },
    {
        'title': 'Pra quê?',
        'duration': 408,  # 6:48 em segundos
        'genre': 'folk',
        'release_date': '2024-01-01',
        'file_path': 'albums/Rai Saia Rodada - E FORRO PRONTO/13 - Pra quê-.mp3'
    }
]

created_music = []
for music_info in music_data:
    music, created = Music.objects.get_or_create(
        title=music_info['title'],
        artist=artist,
        defaults={
            'duration': music_info['duration'],
            'genre': music_info['genre'],
            'release_date': music_info['release_date'],
            'streams_count': random.randint(10000, 1000000),
            'downloads_count': random.randint(1000, 100000),
            'likes_count': random.randint(500, 50000),
            'audio_file': music_info['file_path'],  # Caminho do arquivo de áudio
        }
    )
    if created:
        created_music.append(music)
        print(f'✅ Música criada: {music.title}')
    else:
        print(f'ℹ️ Música já existe: {music.title}')

print(f'\n🎉 Álbum "E FORRO PRONTO" adicionado com sucesso!')
print(f'📊 Total de músicas criadas: {len(created_music)}')
print(f'🎤 Artista: {artist.stage_name}')
print(f'🌐 Acesse: http://prod.ehitapp.com.br/admin/')
