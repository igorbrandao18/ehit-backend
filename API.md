# API REST - Ehit Backend

## 🌐 Endpoints Disponíveis

### **Base URL**: `http://127.0.0.1:8000/api/`

---

## 👤 **Users API** (`/api/users/`)

### **Endpoints:**

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| `GET` | `/users/` | Lista usuários | ✅ |
| `POST` | `/users/create/` | Criar usuário | ❌ |
| `GET` | `/users/{id}/` | Detalhes do usuário | ✅ |
| `GET` | `/users/me/` | Meu perfil | ✅ |
| `POST` | `/users/login/` | Login | ❌ |
| `GET` | `/users/profile/` | Meu perfil | ✅ |
| `PUT/PATCH` | `/users/profile/update/` | Atualizar perfil | ✅ |
| `POST` | `/users/change-password/` | Alterar senha | ✅ |
| `GET` | `/users/stats/` | Minhas estatísticas | ✅ |

### **Exemplos:**

**Criar usuário:**
```json
POST /api/users/create/
{
    "username": "novo_usuario",
    "email": "usuario@email.com",
    "password": "senha123",
    "password_confirm": "senha123",
    "first_name": "João",
    "last_name": "Silva",
    "user_type": "listener"
}
```

**Login:**
```json
POST /api/users/login/
{
    "username": "admin",
    "password": "81927d75"
}
```

---

## 🎵 **Artists API** (`/api/artists/`)

### **Endpoints:**

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| `GET` | `/artists/` | Lista artistas | ❌ |
| `POST` | `/artists/create/` | Criar artista | ✅ |
| `GET` | `/artists/{id}/` | Detalhes do artista | ❌ |
| `GET` | `/artists/{id}/stats/` | Estatísticas do artista | ❌ |
| `POST` | `/artists/{id}/follow/` | Seguir artista | ✅ |
| `GET` | `/artists/{id}/musics/` | Músicas do artista | ❌ |
| `GET` | `/artists/popular/` | Artistas populares | ❌ |
| `GET` | `/artists/trending/` | Artistas em alta | ❌ |
| `GET` | `/artists/genres/` | Lista de gêneros | ❌ |

### **Exemplos:**

**Criar artista:**
```json
POST /api/artists/create/
{
    "stage_name": "Meu Nome Artístico",
    "real_name": "Meu Nome Real",
    "bio": "Biografia do artista",
    "genre": "Rock",
    "location": "São Paulo, SP",
    "website": "https://meusite.com",
    "social_links": {
        "instagram": "@meuinstagram",
        "youtube": "MeuCanalYT"
    }
}
```

**Seguir artista:**
```json
POST /api/artists/1/follow/
{
    "action": "follow"
}
```

---

## 🎶 **Music API** (`/api/music/`)

### **Endpoints:**

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| `GET` | `/music/` | Lista músicas | ❌ |
| `POST` | `/music/create/` | Criar música | ✅ |
| `GET` | `/music/{id}/` | Detalhes da música | ❌ |
| `POST` | `/music/{id}/stream/` | Contar stream | ✅ |
| `POST` | `/music/{id}/download/` | Contar download | ✅ |
| `POST` | `/music/{id}/like/` | Curtir música | ✅ |
| `GET` | `/music/{id}/stats/` | Estatísticas da música | ❌ |
| `GET` | `/music/trending/` | Músicas em alta | ❌ |
| `GET` | `/music/popular/` | Músicas populares | ❌ |
| `GET` | `/music/featured/` | Músicas em destaque | ❌ |
| `GET` | `/music/genres/` | Lista de gêneros | ❌ |
| `GET` | `/music/albums/` | Lista de álbuns | ❌ |

### **Exemplos:**

**Criar música:**
```json
POST /api/music/create/
{
    "title": "Minha Nova Música",
    "album": "Meu Álbum",
    "genre": "Rock",
    "duration": 240,
    "lyrics": "Letra da música...",
    "release_date": "2024-01-01"
}
```

**Curtir música:**
```json
POST /api/music/1/like/
{
    "action": "like"
}
```

---

## 📋 **Playlists API** (`/api/playlists/`)

### **Endpoints:**

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| `GET` | `/playlists/` | Lista playlists | ❌ |
| `POST` | `/playlists/create/` | Criar playlist | ✅ |
| `GET` | `/playlists/{id}/` | Detalhes da playlist | ❌ |
| `GET` | `/playlists/my/` | Minhas playlists | ✅ |
| `POST` | `/playlists/{id}/add-music/` | Adicionar música | ✅ |
| `DELETE` | `/playlists/{id}/remove-music/{music_id}/` | Remover música | ✅ |
| `PUT` | `/playlists/{id}/reorder/` | Reordenar músicas | ✅ |
| `POST` | `/playlists/{id}/follow/` | Seguir playlist | ✅ |
| `GET` | `/playlists/favorites/` | Meus favoritos | ✅ |
| `POST` | `/playlists/favorites/` | Adicionar favorito | ✅ |
| `DELETE` | `/playlists/favorites/{id}/` | Remover favorito | ✅ |
| `GET` | `/playlists/public/` | Playlists públicas | ❌ |
| `GET` | `/playlists/popular/` | Playlists populares | ❌ |

### **Exemplos:**

**Criar playlist:**
```json
POST /api/playlists/create/
{
    "name": "Minha Playlist",
    "description": "Descrição da playlist",
    "is_public": true
}
```

**Adicionar música à playlist:**
```json
POST /api/playlists/1/add-music/
{
    "music_id": 1
}
```

**Reordenar músicas:**
```json
PUT /api/playlists/1/reorder/
{
    "music_orders": {
        "1": 2,
        "2": 1,
        "3": 3
    }
}
```

---

## 🔐 **Autenticação**

### **Headers necessários:**
```http
Authorization: Token <seu_token>
Content-Type: application/json
```

### **Login para obter token:**
```json
POST /api/users/login/
{
    "username": "admin",
    "password": "81927d75"
}
```

---

## 📊 **Paginação**

Todos os endpoints de lista suportam paginação:

**Parâmetros:**
- `page`: Número da página (padrão: 1)
- `page_size`: Itens por página (padrão: 20, máximo: 100)

**Exemplo:**
```
GET /api/music/?page=2&page_size=10
```

**Resposta:**
```json
{
    "count": 100,
    "next": "http://127.0.0.1:8000/api/music/?page=3&page_size=10",
    "previous": "http://127.0.0.1:8000/api/music/?page=1&page_size=10",
    "results": [...]
}
```

---

## 🔍 **Filtros e Busca**

### **Filtros comuns:**
- `search`: Busca por texto
- `ordering`: Ordenação (`-created_at`, `-streams_count`, etc.)
- `page_size`: Itens por página

### **Filtros específicos:**

**Músicas:**
- `artist`: ID do artista
- `genre`: Gênero musical
- `album`: Nome do álbum
- `featured`: Músicas em destaque (true/false)

**Artistas:**
- `genre`: Gênero musical
- `verified`: Artistas verificados (true/false)
- `location`: Localização

**Playlists:**
- `user`: ID do usuário
- `is_public`: Playlists públicas (true/false)

---

## 📈 **Cache**

Alguns endpoints usam cache Redis:

- **Músicas trending**: Cache de 30 minutos
- **Músicas populares**: Cache de 1 hora
- **Artistas populares**: Cache de 1 hora

---

## 🚀 **Testando a API**

### **Com curl:**
```bash
# Listar músicas
curl http://127.0.0.1:8000/api/music/

# Login
curl -X POST http://127.0.0.1:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "81927d75"}'

# Criar playlist (com token)
curl -X POST http://127.0.0.1:8000/api/playlists/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <seu_token>" \
  -d '{"name": "Nova Playlist", "is_public": true}'
```

### **Com Postman/Insomnia:**
1. Importe as URLs da API
2. Configure autenticação com token
3. Teste os endpoints

---

## 📝 **Status Codes**

- `200`: Sucesso
- `201`: Criado com sucesso
- `400`: Dados inválidos
- `401`: Não autenticado
- `403`: Sem permissão
- `404`: Não encontrado
- `500`: Erro interno

---

**🎵 API REST completa e funcional!**
