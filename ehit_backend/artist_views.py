from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q
import json

from apps.artists.models import Artist
from apps.music.models import Music
from apps.users.models import User


@login_required
def artist_dashboard(request):
    """Dashboard do artista - área administrativa simplificada"""
    try:
        artist = request.user.artist_profile
    except Artist.DoesNotExist:
        messages.error(request, 'Você precisa ser um artista para acessar esta área.')
        return redirect('home')
    
    # Estatísticas do artista
    total_musics = Music.objects.filter(artist=artist, is_active=True).count()
    total_streams = artist.get_total_streams()
    total_downloads = artist.get_total_downloads()
    total_likes = artist.get_total_likes()
    
    # Músicas recentes
    recent_musics = Music.objects.filter(artist=artist, is_active=True).order_by('-created_at')[:5]
    
    # Músicas mais populares
    popular_musics = Music.objects.filter(artist=artist, is_active=True).order_by('-streams_count')[:5]
    
    context = {
        'artist': artist,
        'total_musics': total_musics,
        'total_streams': total_streams,
        'total_downloads': total_downloads,
        'total_likes': total_likes,
        'recent_musics': recent_musics,
        'popular_musics': popular_musics,
    }
    
    return render(request, 'artist/dashboard.html', context)


@login_required
def artist_music_list(request):
    """Lista de músicas do artista"""
    try:
        artist = request.user.artist_profile
    except Artist.DoesNotExist:
        messages.error(request, 'Você precisa ser um artista para acessar esta área.')
        return redirect('home')
    
    # Filtros
    search = request.GET.get('search', '')
    album_filter = request.GET.get('album', '')
    genre_filter = request.GET.get('genre', '')
    
    musics = Music.objects.filter(artist=artist, is_active=True)
    
    if search:
        musics = musics.filter(
            Q(title__icontains=search) |
            Q(album__icontains=search) |
            Q(lyrics__icontains=search)
        )
    
    if album_filter:
        musics = musics.filter(album__icontains=album_filter)
    
    if genre_filter:
        musics = musics.filter(genre__icontains=genre_filter)
    
    # Paginação
    paginator = Paginator(musics.order_by('-created_at'), 20)
    page_number = request.GET.get('page')
    musics_page = paginator.get_page(page_number)
    
    # Lista de álbuns para filtro
    albums = Music.objects.filter(artist=artist, is_active=True).values_list('album', flat=True).distinct()
    albums = [album for album in albums if album]  # Remove valores vazios
    
    # Lista de gêneros para filtro
    genres = Music.objects.filter(artist=artist, is_active=True).values_list('genre', flat=True).distinct()
    genres = [genre for genre in genres if genre]  # Remove valores vazios
    
    context = {
        'artist': artist,
        'musics': musics_page,
        'albums': albums,
        'genres': genres,
        'search': search,
        'album_filter': album_filter,
        'genre_filter': genre_filter,
    }
    
    return render(request, 'artist/music_list.html', context)


@login_required
def artist_music_create(request):
    """Criar nova música"""
    try:
        artist = request.user.artist_profile
    except Artist.DoesNotExist:
        messages.error(request, 'Você precisa ser um artista para acessar esta área.')
        return redirect('home')
    
    if request.method == 'POST':
        try:
            # Dados do formulário
            title = request.POST.get('title', '').strip()
            album = request.POST.get('album', '').strip()
            genre = request.POST.get('genre', '').strip()
            duration = request.POST.get('duration', '')
            lyrics = request.POST.get('lyrics', '').strip()
            
            # Validações
            if not title:
                messages.error(request, 'Título é obrigatório.')
                return render(request, 'artist/music_create.html', {'artist': artist})
            
            if not duration or not duration.isdigit():
                messages.error(request, 'Duração deve ser um número válido.')
                return render(request, 'artist/music_create.html', {'artist': artist})
            
            duration = int(duration)
            if duration <= 0 or duration > 3600:
                messages.error(request, 'Duração deve estar entre 1 e 3600 segundos.')
                return render(request, 'artist/music_create.html', {'artist': artist})
            
            # Criar música
            music = Music.objects.create(
                artist=artist,
                title=title,
                album=album or 'Single',
                genre=genre or 'Não especificado',
                duration=duration,
                lyrics=lyrics,
                is_featured=False
            )
            
            messages.success(request, f'Música "{title}" criada com sucesso!')
            return redirect('artist_music_list')
            
        except Exception as e:
            messages.error(request, f'Erro ao criar música: {str(e)}')
    
    context = {
        'artist': artist,
    }
    
    return render(request, 'artist/music_create.html', context)


@login_required
def artist_music_edit(request, music_id):
    """Editar música"""
    try:
        artist = request.user.artist_profile
    except Artist.DoesNotExist:
        messages.error(request, 'Você precisa ser um artista para acessar esta área.')
        return redirect('home')
    
    music = get_object_or_404(Music, id=music_id, artist=artist, is_active=True)
    
    if request.method == 'POST':
        try:
            # Dados do formulário
            music.title = request.POST.get('title', '').strip()
            music.album = request.POST.get('album', '').strip()
            music.genre = request.POST.get('genre', '').strip()
            music.lyrics = request.POST.get('lyrics', '').strip()
            
            duration = request.POST.get('duration', '')
            if duration and duration.isdigit():
                music.duration = int(duration)
            
            # Validações
            if not music.title:
                messages.error(request, 'Título é obrigatório.')
                return render(request, 'artist/music_edit.html', {'artist': artist, 'music': music})
            
            music.save()
            messages.success(request, f'Música "{music.title}" atualizada com sucesso!')
            return redirect('artist_music_list')
            
        except Exception as e:
            messages.error(request, f'Erro ao atualizar música: {str(e)}')
    
    context = {
        'artist': artist,
        'music': music,
    }
    
    return render(request, 'artist/music_edit.html', context)


@login_required
def artist_music_delete(request, music_id):
    """Deletar música (soft delete)"""
    try:
        artist = request.user.artist_profile
    except Artist.DoesNotExist:
        messages.error(request, 'Você precisa ser um artista para acessar esta área.')
        return redirect('home')
    
    music = get_object_or_404(Music, id=music_id, artist=artist, is_active=True)
    
    if request.method == 'POST':
        music.is_active = False
        music.save()
        messages.success(request, f'Música "{music.title}" removida com sucesso!')
        return redirect('artist_music_list')
    
    context = {
        'artist': artist,
        'music': music,
    }
    
    return render(request, 'artist/music_delete.html', context)


@login_required
def artist_albums(request):
    """Lista de álbuns do artista"""
    try:
        artist = request.user.artist_profile
    except Artist.DoesNotExist:
        messages.error(request, 'Você precisa ser um artista para acessar esta área.')
        return redirect('home')
    
    # Agrupar músicas por álbum
    albums_data = {}
    musics = Music.objects.filter(artist=artist, is_active=True).order_by('album', 'title')
    
    for music in musics:
        album_name = music.album or 'Single'
        if album_name not in albums_data:
            albums_data[album_name] = {
                'name': album_name,
                'musics': [],
                'total_duration': 0,
                'total_streams': 0,
                'total_downloads': 0,
                'total_likes': 0,
            }
        
        albums_data[album_name]['musics'].append(music)
        albums_data[album_name]['total_duration'] += music.duration
        albums_data[album_name]['total_streams'] += music.streams_count
        albums_data[album_name]['total_downloads'] += music.downloads_count
        albums_data[album_name]['total_likes'] += music.likes_count
    
    context = {
        'artist': artist,
        'albums': albums_data.values(),
    }
    
    return render(request, 'artist/albums.html', context)


@login_required
def artist_stats(request):
    """Estatísticas detalhadas do artista"""
    try:
        artist = request.user.artist_profile
    except Artist.DoesNotExist:
        messages.error(request, 'Você precisa ser um artista para acessar esta área.')
        return redirect('home')
    
    # Estatísticas gerais
    total_musics = Music.objects.filter(artist=artist, is_active=True).count()
    total_streams = artist.get_total_streams()
    total_downloads = artist.get_total_downloads()
    total_likes = artist.get_total_likes()
    
    # Músicas mais populares
    popular_musics = Music.objects.filter(artist=artist, is_active=True).order_by('-streams_count')[:10]
    
    # Músicas mais curtidas
    liked_musics = Music.objects.filter(artist=artist, is_active=True).order_by('-likes_count')[:10]
    
    # Músicas mais baixadas
    downloaded_musics = Music.objects.filter(artist=artist, is_active=True).order_by('-downloads_count')[:10]
    
    # Estatísticas por gênero
    genre_stats = {}
    musics = Music.objects.filter(artist=artist, is_active=True)
    for music in musics:
        genre = music.genre or 'Não especificado'
        if genre not in genre_stats:
            genre_stats[genre] = {
                'count': 0,
                'streams': 0,
                'downloads': 0,
                'likes': 0
            }
        genre_stats[genre]['count'] += 1
        genre_stats[genre]['streams'] += music.streams_count
        genre_stats[genre]['downloads'] += music.downloads_count
        genre_stats[genre]['likes'] += music.likes_count
    
    context = {
        'artist': artist,
        'total_musics': total_musics,
        'total_streams': total_streams,
        'total_downloads': total_downloads,
        'total_likes': total_likes,
        'popular_musics': popular_musics,
        'liked_musics': liked_musics,
        'downloaded_musics': downloaded_musics,
        'genre_stats': genre_stats,
    }
    
    return render(request, 'artist/stats.html', context)
