#!/usr/bin/env python3
import os
import sys
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ehit_backend.settings')
django.setup()

from apps.artists.models import Artist
from apps.music.models import Music

# Criar algumas músicas de teste
music_data = [
    {'title': 'God\'s Plan', 'artist': 'Drake', 'duration': 198, 'genre': 'hip_hop', 'release_date': '2018-01-19'},
    {'title': 'Anti-Hero', 'artist': 'Taylor Swift', 'duration': 201, 'genre': 'pop', 'release_date': '2022-10-21'},
    {'title': 'Shape of You', 'artist': 'Ed Sheeran', 'duration': 233, 'genre': 'pop', 'release_date': '2017-01-06'},
    {'title': 'Bad Guy', 'artist': 'Billie Eilish', 'duration': 194, 'genre': 'alternative', 'release_date': '2019-03-29'},
    {'title': 'Blinding Lights', 'artist': 'The Weeknd', 'duration': 200, 'genre': 'rnb', 'release_date': '2019-11-29'},
    {'title': 'Thank U, Next', 'artist': 'Ariana Grande', 'duration': 207, 'genre': 'pop', 'release_date': '2018-11-03'},
    {'title': 'Sunflower', 'artist': 'Post Malone', 'duration': 158, 'genre': 'hip_hop', 'release_date': '2018-10-19'},
    {'title': 'Levitating', 'artist': 'Dua Lipa', 'duration': 203, 'genre': 'pop', 'release_date': '2020-10-01'},
    {'title': 'Dakiti', 'artist': 'Bad Bunny', 'duration': 233, 'genre': 'latin', 'release_date': '2020-10-30'},
    {'title': 'Drivers License', 'artist': 'Olivia Rodrigo', 'duration': 242, 'genre': 'pop', 'release_date': '2021-01-08'},
]

created_music = []
for music_info in music_data:
    try:
        artist = Artist.objects.get(stage_name=music_info['artist'])
        music, created = Music.objects.get_or_create(
            title=music_info['title'],
            artist=artist,
            defaults={
                'duration': music_info['duration'],
                'genre': music_info['genre'],
                'release_date': music_info['release_date'],
                'streams_count': random.randint(1000, 10000000),
                'downloads_count': random.randint(100, 1000000),
                'likes_count': random.randint(50, 500000),
            }
        )
        if created:
            created_music.append(music)
            print(f'✅ Música criada: {music.title} - {music.artist.stage_name}')
        else:
            print(f'ℹ️ Música já existe: {music.title} - {music.artist.stage_name}')
    except Artist.DoesNotExist:
        print(f'❌ Artista não encontrado: {music_info["artist"]}')

print(f'\n📊 Total de músicas criadas: {len(created_music)}')
