#!/usr/bin/env python3
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ehit_backend.settings')
django.setup()

from apps.users.models import User
from apps.artists.models import Artist

# Criar os artistas restantes
artists_data = [
    {
        'stage_name': 'Ariana Grande',
        'bio': 'Cantora americana conhecida por sua voz poderosa e hits pop',
        'genre': 'pop',
        'verified': True,
        'location': 'Boca Raton, USA',
        'user': User.objects.get(username='user6')
    },
    {
        'stage_name': 'Post Malone',
        'bio': 'Rapper e cantor americano conhecido por Sunflower e Circles',
        'genre': 'hip_hop',
        'verified': True,
        'location': 'Syracuse, USA',
        'user': User.objects.get(username='user7')
    },
    {
        'stage_name': 'Dua Lipa',
        'bio': 'Cantora britânica conhecida por Levitating e Don\'t Start Now',
        'genre': 'pop',
        'verified': True,
        'location': 'London, UK',
        'user': User.objects.get(username='user8')
    },
    {
        'stage_name': 'Bad Bunny',
        'bio': 'Rapper porto-riquenho, um dos maiores nomes do reggaeton',
        'genre': 'latin',
        'verified': True,
        'location': 'San Juan, Puerto Rico',
        'user': User.objects.get(username='user9')
    },
    {
        'stage_name': 'Olivia Rodrigo',
        'bio': 'Cantora americana conhecida por Drivers License e Good 4 U',
        'genre': 'pop',
        'verified': True,
        'location': 'Temecula, USA',
        'user': User.objects.get(username='user10')
    }
]

for artist_data in artists_data:
    artist, created = Artist.objects.get_or_create(
        stage_name=artist_data['stage_name'],
        defaults=artist_data
    )
    if created:
        print(f'✅ Artista criado: {artist.stage_name}')
    else:
        print(f'ℹ️ Artista já existe: {artist.stage_name}')
