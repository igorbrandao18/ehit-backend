# 🎵 Ehit Backend API - Documentação Simplificada

## 📋 Visão Geral

API REST simplificada com apenas endpoints essenciais para a aplicação mobile.

**Base URL:** `https://prod.ehitapp.com.br/api/`

---

## 🎤 Endpoints de Artistas

### 1. Listar Todos os Artistas
**GET** `/api/artists/`

Retorna lista paginada de todos os artistas ativos.

**Query Parameters:**
- `search` - Buscar por nome do artista
- `ordering` - Ordenação (default: `-created_at`)
- `page_size` - Itens por página (default: 20, máximo: 100)
- `page` - Número da página

**Exemplo:**
```bash
curl "https://prod.ehitapp.com.br/api/artists/"
```

**Resposta:**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 5,
      "stage_name": "Natanzinho Lima",
      "photo": "https://prod.ehitapp.com.br/media/artists/photos/...",
      "genre": 4,
      "genre_data": {
        "id": 4,
        "name": "Arrocha",
        "slug": "arrocha",
        "color": "#FF6B6B"
      },
      "albums_count": 1,
      "is_active": true,
      "created_at": "2025-10-21T13:47:03.426729Z"
    }
  ]
}
```

---

### 2. Detalhes do Artista
**GET** `/api/artists/<id>/`

Retorna informações detalhadas de um artista específico.

**Exemplo:**
```bash
curl "https://prod.ehitapp.com.br/api/artists/5/"
```

---

### 3. Álbuns do Artista (⭐ Importante)
**GET** `/api/artists/<id>/albums/`

Retorna **todos os álbuns** de um artista específico. Use este endpoint para buscar 100% dos álbuns quando o usuário clicar no artista.

**Exemplo:**
```bash
curl "https://prod.ehitapp.com.br/api/artists/5/albums/"
```

**Resposta:**
```json
{
  "artist": {
    "id": 5,
    "stage_name": "Natanzinho Lima",
    "photo": "/media/artists/photos/..."
  },
  "albums": [
    {
      "id": 1,
      "name": "Cortando Chão",
      "cover": "/media/albums/covers/...",
      "release_date": "2025-10-21",
      "featured": false,
      "musics_count": 0,
      "artist": 5,
      "artist_name": "Natanzinho Lima",
      "is_active": true
    }
  ],
  "count": 1
}
```

---

### 4. Músicas do Álbum (⭐ Para Adicionar Músicas)
**GET** `/api/artists/albums/<album_id>/musics/`

Retorna **todas as músicas** de um álbum específico. Use este endpoint para ver as músicas de um álbum.

**Query Parameters:**
- `page` - Número da página (default: 1)
- `page_size` - Itens por página (default: 20)

**Exemplo:**
```bash
curl "https://prod.ehitapp.com.br/api/artists/albums/1/musics/"
```

**Resposta:**
```json
{
  "musics": [
    {
      "id": 6,
      "title": "Chuva de Arroz",
      "artist": 5,
      "artist_name": "Natanzinho Lima",
      "duration": 180,
      "duration_formatted": "3:00",
      "file": "https://prod.ehitapp.com.br/media/music/...",
      "cover": "https://prod.ehitapp.com.br/media/covers/...",
      "stream_url": "/api/music/6/stream/",
      "is_active": true
    }
  ],
  "count": 1,
  "page": 1,
  "page_size": 20,
  "total_pages": 1
}
```

---

## 🎧 Endpoints de PlayHits (Playlists)

### 1. Listar PlayHits
**GET** `/api/playlists/`

Retorna lista paginada de todas as playlists (PlayHits).

**Query Parameters:**
- `featured` - Mostrar apenas em destaque (use `true`)
- `search` - Buscar por nome da playlist
- `ordering` - Ordenação (default: `-created_at`)
- `page_size` - Itens por página (default: 20)
- `page` - Número da página

**Exemplo - Todas as PlayHits:**
```bash
curl "https://prod.ehitapp.com.br/api/playlists/"
```

**Exemplo - PlayHits em Destaque:**
```bash
curl "https://prod.ehitapp.com.br/api/playlists/?featured=true"
```

---

### 2. Detalhes da PlayHit com Músicas (⭐ Importante)
**GET** `/api/playlists/<id>/`

Retorna a playlist completa com **todas as músicas**. Use este endpoint quando o usuário clicar na PlayHit para ver as músicas.

**Exemplo:**
```bash
curl "https://prod.ehitapp.com.br/api/playlists/1/"
```

**Resposta:**
```json
{
  "id": 1,
  "name": "FORRÓ",
  "cover": "https://prod.ehitapp.com.br/media/playlist_covers/...",
  "musics_count": 1,
  "is_featured": false,
  "is_active": true,
  "musics_data": [
    {
      "id": 1,
      "title": "Seis Cordas - Baião de Dois - Cavalo Lampião",
      "artist": 1,
      "artist_name": "Wesley Safadão",
      "genre": 1,
      "genre_data": {
        "id": 1,
        "name": "Forró",
        "slug": "forro",
        "color": "#FF6B6B"
      },
      "duration": 1,
      "duration_formatted": "0:01",
      "file": "https://prod.ehitapp.com.br/media/music/...",
      "cover": "https://prod.ehitapp.com.br/media/covers/...",
      "stream_url": "/api/music/1/stream/",
      "download_url": "/api/music/1/download/",
      "is_active": true
    }
  ],
  "created_at": "2025-10-20T02:23:16.201419Z"
}
```

---

## 🎯 Fluxo de Uso no App

### Cenário 1: Ver Álbuns de um Artista
```
1. Usuário clica no artista
2. App faz: GET /api/artists/<id>/albums/
3. App exibe os álbuns do artista
```

### Cenário 2: Ver Músicas de um Álbum
```
1. Usuário clica no álbum
2. App faz: GET /api/artists/albums/<id>/musics/
3. App exibe as músicas com stream_url para cada uma
```

### Cenário 3: Ver Músicas de uma PlayHit
```
1. Usuário clica na PlayHit
2. App faz: GET /api/playlists/<id>/
3. App pega o array 'musics_data'
4. App exibe as músicas com stream_url para cada uma
```

---

## 🔑 Endpoints Essenciais para o App

| Endpoint | Descrição | Quando Usar |
|----------|-----------|------------|
| `GET /api/artists/` | Lista todos artistas | Tela de artistas |
| `GET /api/artists/<id>/albums/` | Álbuns do artista | Quando clicar no artista |
| `GET /api/artists/albums/<id>/musics/` | Músicas do álbum | Para ver músicas do álbum |
| `GET /api/playlists/` | Lista PlayHits | Tela de PlayHits |
| `GET /api/playlists/?featured=true` | PlayHits em destaque | Tela principal |
| `GET /api/playlists/<id>/` | PlayHit com músicas | Quando clicar na PlayHit |

---

## 📱 Exemplos de Implementação

### React Native / JavaScript

**Listar Artistas:**
```javascript
const getArtists = async () => {
  const response = await fetch('https://prod.ehitapp.com.br/api/artists/');
  const data = await response.json();
  return data.results; // Array de artistas
};
```

**Buscar Álbuns do Artista:**
```javascript
const getArtistAlbums = async (artistId) => {
  const response = await fetch(`https://prod.ehitapp.com.br/api/artists/${artistId}/albums/`);
  const data = await response.json();
  return data.albums; // Array de álbuns
};
```

**Buscar Músicas do Álbum:**
```javascript
const getAlbumMusics = async (albumId) => {
  const response = await fetch(`https://prod.ehitapp.com.br/api/artists/albums/${albumId}/musics/`);
  const data = await response.json();
  return data.musics; // Array de músicas
};
```

**Buscar Músicas da PlayHit:**
```javascript
const getPlaylistMusics = async (playlistId) => {
  const response = await fetch(`https://prod.ehitapp.com.br/api/playlists/${playlistId}/`);
  const data = await response.json();
  return data.musics_data; // Array de músicas
};
```

**PlayHits em Destaque:**
```javascript
const getFeaturedPlaylists = async () => {
  const response = await fetch('https://prod.ehitapp.com.br/api/playlists/?featured=true');
  const data = await response.json();
  return data.results; // Array de PlayHits em destaque
};
```

---

## 🚀 Features

- ✅ Paginação automática
- ✅ Cache Redis (15-30 minutos)
- ✅ URLs absolutas para arquivos de mídia
- ✅ Informações completas (artistas, gêneros, etc.)
- ✅ Filtros por destaque, busca, ordenação
- ✅ Endpoints simplificados

---

## 📞 Suporte

**Documentação completa:** `/api/`

**Admin:** https://prod.ehitapp.com.br/admin/

**Health Check:** https://prod.ehitapp.com.br/health/

