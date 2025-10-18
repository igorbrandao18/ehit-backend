#!/usr/bin/env python3
"""
Script para popular o banco de dados com dados de teste
"""

import os
import sys
import django
from django.utils import timezone
from datetime import timedelta
import random

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ehit_backend.settings')
django.setup()

from apps.users.models import User
from apps.artists.models import Artist
from apps.music.models import Music
from apps.playlists.models import Playlist
from apps.constants import GENRE_CHOICES

def create_test_users():
    """Criar usuários de teste"""
    print("👤 Criando usuários de teste...")
    
    users_data = [
        {'username': 'admin', 'email': 'admin@ehitapp.com.br', 'is_staff': True, 'is_superuser': True},
        {'username': 'user1', 'email': 'user1@test.com', 'first_name': 'João', 'last_name': 'Silva'},
        {'username': 'user2', 'email': 'user2@test.com', 'first_name': 'Maria', 'last_name': 'Santos'},
        {'username': 'user3', 'email': 'user3@test.com', 'first_name': 'Pedro', 'last_name': 'Costa'},
        {'username': 'user4', 'email': 'user4@test.com', 'first_name': 'Ana', 'last_name': 'Lima'},
        {'username': 'user5', 'email': 'user5@test.com', 'first_name': 'Carlos', 'last_name': 'Oliveira'},
    ]
    
    created_users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'first_name': user_data.get('first_name', ''),
                'last_name': user_data.get('last_name', ''),
                'is_staff': user_data.get('is_staff', False),
                'is_superuser': user_data.get('is_superuser', False),
            }
        )
        if created:
            user.set_password('test123')
            user.save()
            created_users.append(user)
            print(f"✅ Usuário criado: {user.username}")
        else:
            print(f"ℹ️ Usuário já existe: {user.username}")
    
    return created_users

def create_test_artists():
    """Criar artistas de teste"""
    print("🎤 Criando artistas de teste...")
    
    # Pegar usuários para associar aos artistas (cada artista precisa de um usuário único)
    users = list(User.objects.filter(is_superuser=False))
    if not users:
        users = [User.objects.first()]
    
    artists_data = [
        {
            'stage_name': 'Drake',
            'bio': 'Rapper canadense conhecido por hits como "God\'s Plan" e "Hotline Bling"',
            'genre': 'hip_hop',
            'verified': True,
            'location': 'Toronto, Canada'
        },
        {
            'stage_name': 'Taylor Swift',
            'bio': 'Cantora e compositora americana, uma das artistas mais vendidas da história',
            'genre': 'pop',
            'verified': True,
            'location': 'Nashville, USA'
        },
        {
            'stage_name': 'Ed Sheeran',
            'bio': 'Cantor e compositor britânico conhecido por "Shape of You" e "Perfect"',
            'genre': 'pop',
            'verified': True,
            'location': 'Halifax, UK'
        },
        {
            'stage_name': 'Billie Eilish',
            'bio': 'Cantora americana conhecida por seu estilo único e hits como "Bad Guy"',
            'genre': 'alternative',
            'verified': True,
            'location': 'Los Angeles, USA'
        },
        {
            'stage_name': 'The Weeknd',
            'bio': 'Cantor canadense conhecido por "Blinding Lights" e "Starboy"',
            'genre': 'rnb',
            'verified': True,
            'location': 'Toronto, Canada'
        },
        {
            'stage_name': 'Ariana Grande',
            'bio': 'Cantora americana conhecida por sua voz poderosa e hits pop',
            'genre': 'pop',
            'verified': True,
            'location': 'Boca Raton, USA'
        },
        {
            'stage_name': 'Post Malone',
            'bio': 'Rapper e cantor americano conhecido por "Sunflower" e "Circles"',
            'genre': 'hip_hop',
            'verified': True,
            'location': 'Syracuse, USA'
        },
        {
            'stage_name': 'Dua Lipa',
            'bio': 'Cantora britânica conhecida por "Levitating" e "Don\'t Start Now"',
            'genre': 'pop',
            'verified': True,
            'location': 'London, UK'
        },
        {
            'stage_name': 'Bad Bunny',
            'bio': 'Rapper porto-riquenho, um dos maiores nomes do reggaeton',
            'genre': 'latin',
            'verified': True,
            'location': 'San Juan, Puerto Rico'
        },
        {
            'stage_name': 'Olivia Rodrigo',
            'bio': 'Cantora americana conhecida por "Drivers License" e "Good 4 U"',
            'genre': 'pop',
            'verified': True,
            'location': 'Temecula, USA'
        }
    ]
    
    created_artists = []
    for i, artist_data in enumerate(artists_data):
        # Usar usuário diferente para cada artista
        user = users[i % len(users)]
        artist_data['user'] = user
        
        artist, created = Artist.objects.get_or_create(
            stage_name=artist_data['stage_name'],
            defaults=artist_data
        )
        if created:
            created_artists.append(artist)
            print(f"✅ Artista criado: {artist.stage_name}")
        else:
            print(f"ℹ️ Artista já existe: {artist.stage_name}")
    
    return created_artists

def create_test_music():
    """Criar músicas de teste"""
    print("🎵 Criando músicas de teste...")
    
    artists = Artist.objects.all()
    if not artists.exists():
        print("❌ Nenhum artista encontrado. Execute create_test_artists() primeiro.")
        return []
    
    music_data = [
        # Drake
        {'title': 'God\'s Plan', 'artist': 'Drake', 'duration': 198, 'genre': 'hip_hop', 'release_date': '2018-01-19'},
        {'title': 'Hotline Bling', 'artist': 'Drake', 'duration': 267, 'genre': 'hip_hop', 'release_date': '2015-07-31'},
        {'title': 'One Dance', 'artist': 'Drake', 'duration': 173, 'genre': 'hip_hop', 'release_date': '2016-04-05'},
        {'title': 'In My Feelings', 'artist': 'Drake', 'duration': 217, 'genre': 'hip_hop', 'release_date': '2018-07-10'},
        
        # Taylor Swift
        {'title': 'Anti-Hero', 'artist': 'Taylor Swift', 'duration': 201, 'genre': 'pop', 'release_date': '2022-10-21'},
        {'title': 'Shake It Off', 'artist': 'Taylor Swift', 'duration': 219, 'genre': 'pop', 'release_date': '2014-08-18'},
        {'title': 'Blank Space', 'artist': 'Taylor Swift', 'duration': 231, 'genre': 'pop', 'release_date': '2014-11-10'},
        {'title': 'Love Story', 'artist': 'Taylor Swift', 'duration': 237, 'genre': 'country', 'release_date': '2008-09-12'},
        
        # Ed Sheeran
        {'title': 'Shape of You', 'artist': 'Ed Sheeran', 'duration': 233, 'genre': 'pop', 'release_date': '2017-01-06'},
        {'title': 'Perfect', 'artist': 'Ed Sheeran', 'duration': 263, 'genre': 'pop', 'release_date': '2017-03-03'},
        {'title': 'Thinking Out Loud', 'artist': 'Ed Sheeran', 'duration': 281, 'genre': 'pop', 'release_date': '2014-09-24'},
        {'title': 'Photograph', 'artist': 'Ed Sheeran', 'duration': 258, 'genre': 'pop', 'release_date': '2015-05-11'},
        
        # Billie Eilish
        {'title': 'Bad Guy', 'artist': 'Billie Eilish', 'duration': 194, 'genre': 'alternative', 'release_date': '2019-03-29'},
        {'title': 'Happier Than Ever', 'artist': 'Billie Eilish', 'duration': 298, 'genre': 'alternative', 'release_date': '2021-07-30'},
        {'title': 'Therefore I Am', 'artist': 'Billie Eilish', 'duration': 174, 'genre': 'alternative', 'release_date': '2020-11-12'},
        {'title': 'Everything I Wanted', 'artist': 'Billie Eilish', 'duration': 247, 'genre': 'alternative', 'release_date': '2019-11-13'},
        
        # The Weeknd
        {'title': 'Blinding Lights', 'artist': 'The Weeknd', 'duration': 200, 'genre': 'rnb', 'release_date': '2019-11-29'},
        {'title': 'Starboy', 'artist': 'The Weeknd', 'duration': 230, 'genre': 'rnb', 'release_date': '2016-09-21'},
        {'title': 'Save Your Tears', 'artist': 'The Weeknd', 'duration': 215, 'genre': 'rnb', 'release_date': '2020-08-09'},
        {'title': 'The Hills', 'artist': 'The Weeknd', 'duration': 195, 'genre': 'rnb', 'release_date': '2015-05-27'},
        
        # Ariana Grande
        {'title': 'Thank U, Next', 'artist': 'Ariana Grande', 'duration': 207, 'genre': 'pop', 'release_date': '2018-11-03'},
        {'title': '7 Rings', 'artist': 'Ariana Grande', 'duration': 179, 'genre': 'pop', 'release_date': '2019-01-18'},
        {'title': 'Positions', 'artist': 'Ariana Grande', 'duration': 172, 'genre': 'pop', 'release_date': '2020-10-23'},
        {'title': 'Side to Side', 'artist': 'Ariana Grande', 'duration': 226, 'genre': 'pop', 'release_date': '2016-08-30'},
        
        # Post Malone
        {'title': 'Sunflower', 'artist': 'Post Malone', 'duration': 158, 'genre': 'hip_hop', 'release_date': '2018-10-19'},
        {'title': 'Circles', 'artist': 'Post Malone', 'duration': 215, 'genre': 'hip_hop', 'release_date': '2019-08-30'},
        {'title': 'Rockstar', 'artist': 'Post Malone', 'duration': 218, 'genre': 'hip_hop', 'release_date': '2017-09-15'},
        {'title': 'Better Now', 'artist': 'Post Malone', 'duration': 231, 'genre': 'hip_hop', 'release_date': '2018-04-27'},
        
        # Dua Lipa
        {'title': 'Levitating', 'artist': 'Dua Lipa', 'duration': 203, 'genre': 'pop', 'release_date': '2020-10-01'},
        {'title': 'Don\'t Start Now', 'artist': 'Dua Lipa', 'duration': 183, 'genre': 'pop', 'release_date': '2019-10-31'},
        {'title': 'Physical', 'artist': 'Dua Lipa', 'duration': 194, 'genre': 'pop', 'release_date': '2020-01-31'},
        {'title': 'New Rules', 'artist': 'Dua Lipa', 'duration': 209, 'genre': 'pop', 'release_date': '2017-07-07'},
        
        # Bad Bunny
        {'title': 'Dakiti', 'artist': 'Bad Bunny', 'duration': 233, 'genre': 'latin', 'release_date': '2020-10-30'},
        {'title': 'MIA', 'artist': 'Bad Bunny', 'duration': 209, 'genre': 'latin', 'release_date': '2018-10-11'},
        {'title': 'Yo Perreo Sola', 'artist': 'Bad Bunny', 'duration': 156, 'genre': 'latin', 'release_date': '2020-03-20'},
        {'title': 'Callaita', 'artist': 'Bad Bunny', 'duration': 251, 'genre': 'latin', 'release_date': '2019-05-31'},
        
        # Olivia Rodrigo
        {'title': 'Drivers License', 'artist': 'Olivia Rodrigo', 'duration': 242, 'genre': 'pop', 'release_date': '2021-01-08'},
        {'title': 'Good 4 U', 'artist': 'Olivia Rodrigo', 'duration': 178, 'genre': 'pop', 'release_date': '2021-05-14'},
        {'title': 'Deja Vu', 'artist': 'Olivia Rodrigo', 'duration': 215, 'genre': 'pop', 'release_date': '2021-04-01'},
        {'title': 'Traitor', 'artist': 'Olivia Rodrigo', 'duration': 229, 'genre': 'pop', 'release_date': '2021-05-21'},
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
                print(f"✅ Música criada: {music.title} - {music.artist.stage_name}")
            else:
                print(f"ℹ️ Música já existe: {music.title} - {music.artist.stage_name}")
        except Artist.DoesNotExist:
            print(f"❌ Artista não encontrado: {music_info['artist']}")
    
    return created_music

def create_test_playlists():
    """Criar playlists de teste"""
    print("📋 Criando playlists de teste...")
    
    users = User.objects.filter(is_superuser=False)[:3]  # Usuários não-admin
    if not users.exists():
        print("❌ Nenhum usuário encontrado. Execute create_test_users() primeiro.")
        return []
    
    music = Music.objects.all()
    if not music.exists():
        print("❌ Nenhuma música encontrada. Execute create_test_music() primeiro.")
        return []
    
    playlist_data = [
        {
            'name': 'Top Hits 2024',
            'description': 'Os maiores hits do ano de 2024',
            'is_public': True,
            'user': users[0] if users.count() > 0 else None
        },
        {
            'name': 'Hip Hop Classics',
            'description': 'Clássicos do hip hop que marcaram época',
            'is_public': True,
            'user': users[1] if users.count() > 1 else users[0]
        },
        {
            'name': 'Pop Favorites',
            'description': 'Minhas músicas pop favoritas',
            'is_public': False,
            'user': users[2] if users.count() > 2 else users[0]
        },
        {
            'name': 'Workout Mix',
            'description': 'Músicas para treinar e se exercitar',
            'is_public': True,
            'user': users[0] if users.count() > 0 else None
        },
        {
            'name': 'Chill Vibes',
            'description': 'Músicas relaxantes para momentos de calma',
            'is_public': True,
            'user': users[1] if users.count() > 1 else users[0]
        }
    ]
    
    created_playlists = []
    for playlist_info in playlist_data:
        if playlist_info['user']:
            playlist, created = Playlist.objects.get_or_create(
                name=playlist_info['name'],
                user=playlist_info['user'],
                defaults={
                    'description': playlist_info['description'],
                    'is_public': playlist_info['is_public']
                }
            )
            if created:
                # Adicionar algumas músicas aleatórias
                random_music = music.order_by('?')[:random.randint(5, 15)]
                playlist.music.set(random_music)
                created_playlists.append(playlist)
                print(f"✅ Playlist criada: {playlist.name} ({playlist.music.count()} músicas)")
            else:
                print(f"ℹ️ Playlist já existe: {playlist.name}")
    
    return created_playlists

def main():
    """Função principal para executar todos os testes"""
    print("🚀 Iniciando população do banco de dados com dados de teste...")
    print("=" * 60)
    
    try:
        # Criar dados de teste
        users = create_test_users()
        artists = create_test_artists()
        music = create_test_music()
        playlists = create_test_playlists()
        
        print("=" * 60)
        print("📊 Resumo da população:")
        print(f"👤 Usuários criados: {len(users)}")
        print(f"🎤 Artistas criados: {len(artists)}")
        print(f"🎵 Músicas criadas: {len(music)}")
        print(f"📋 Playlists criadas: {len(playlists)}")
        
        print("\n🎉 População do banco concluída com sucesso!")
        print("🌐 Acesse: http://prod.ehitapp.com.br/admin/")
        print("👤 Login: admin / admin123")
        
    except Exception as e:
        print(f"❌ Erro durante a população: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()