# 🎵 Ehit Backend

Backend completo do sistema Ehit - Plataforma de música inspirada no Sua Música, desenvolvida com Django, PostgreSQL, Redis e APIs REST.

## 🚀 Tecnologias

- **Django 5.2.7** - Framework web Python
- **PostgreSQL** - Banco de dados principal
- **Redis** - Cache e sessões
- **Django REST Framework** - APIs REST
- **Docker & Docker Compose** - Containerização
- **Celery** - Tarefas assíncronas
- **Pillow** - Processamento de imagens

## 📁 Estrutura do Projeto

```
ehit_backend/
├── apps/
│   ├── users/          # Sistema de usuários
│   ├── artists/        # Gestão de artistas
│   ├── music/          # Sistema de músicas
│   └── playlists/      # Playlists e favoritos
├── ehit_backend/       # Configurações Django
├── docs/               # Documentação
├── docker-compose.yml  # Serviços Docker
├── requirements.txt    # Dependências Python
└── manage.py          # Script de gerenciamento
```

## 🛠️ Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/igorbrandao18/ehit-backend.git
cd ehit-backend
```

### 2. Configure o ambiente
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite as variáveis no .env
nano .env
```

### 3. Execute com Docker Compose
```bash
# Inicie os serviços (PostgreSQL + Redis)
docker-compose up -d

# Instale dependências Python
pip install -r requirements.txt

# Execute migrações
python manage.py migrate

# Crie superusuário
python manage.py createsuperuser

# Execute os testes
python manage.py test

# Inicie o servidor
python manage.py runserver
```

## 🌐 Acesso

- **Admin Django**: http://localhost:8000/admin/
- **APIs REST**: http://localhost:8000/api/
- **PostgreSQL**: localhost:5433
- **Redis**: localhost:6379

## 📊 APIs Disponíveis

### 👤 Users API (`/api/users/`)
- `GET /users/` - Lista usuários
- `POST /users/create/` - Criar usuário
- `POST /users/login/` - Login
- `GET /users/profile/` - Meu perfil
- `PUT /users/profile/update/` - Atualizar perfil

### 🎵 Artists API (`/api/artists/`)
- `GET /artists/` - Lista artistas
- `POST /artists/create/` - Criar artista
- `GET /artists/{id}/` - Detalhes do artista
- `POST /artists/{id}/follow/` - Seguir artista
- `GET /artists/popular/` - Artistas populares

### 🎶 Music API (`/api/music/`)
- `GET /music/` - Lista músicas
- `POST /music/create/` - Criar música
- `POST /music/{id}/stream/` - Contar stream
- `POST /music/{id}/like/` - Curtir música
- `GET /music/trending/` - Músicas em alta

### 📋 Playlists API (`/api/playlists/`)
- `GET /playlists/` - Lista playlists
- `POST /playlists/create/` - Criar playlist
- `POST /playlists/{id}/add-music/` - Adicionar música
- `GET /playlists/favorites/` - Meus favoritos
- `GET /playlists/popular/` - Playlists populares

## 🧪 Testes

O projeto possui **60 testes automatizados** cobrindo todos os modelos:

```bash
# Executar todos os testes
python manage.py test

# Testes com verbosidade
python manage.py test --verbosity=2

# Testes específicos
python manage.py test apps.users
python manage.py test apps.users.tests.UserModelTest
```

**Cobertura:**
- ✅ 12 testes - Users
- ✅ 12 testes - Artists  
- ✅ 12 testes - Music
- ✅ 24 testes - Playlists

## 📈 Funcionalidades

### 🎯 Sistema de Usuários
- Usuários customizados (listener, artist, venue, admin)
- Sistema de verificação
- Perfis completos com avatar e bio
- Contadores de seguidores

### 🎵 Gestão de Artistas
- Perfis artísticos completos
- Links sociais (Instagram, YouTube, etc.)
- Estatísticas (streams, downloads, curtidas)
- Sistema de verificação

### 🎶 Sistema de Músicas
- Upload de arquivos de áudio
- Metadados completos (título, álbum, gênero)
- Sistema de capas e letras
- Contadores de reprodução
- Músicas em destaque e trending

### 📋 Playlists e Favoritos
- Playlists personalizadas
- Sistema de favoritos
- Reordenação de músicas
- Playlists públicas e privadas
- Seguir playlists

### ⚡ Performance
- **Cache Redis** para dados frequentes
- **Paginação** para listas grandes
- **Filtros otimizados** com Django ORM
- **Serializers eficientes**

## 🔧 Configuração

### Variáveis de Ambiente (.env)
```env
SECRET_KEY=sua_chave_secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://user:pass@localhost:5433/ehit_db
REDIS_URL=redis://localhost:6379/1
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Docker Compose
```yaml
services:
  db:
    image: postgres:15
    ports:
      - "5433:5432"
    environment:
      POSTGRES_DB: ehit_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

## 📚 Documentação

- **[API.md](API.md)** - Documentação completa das APIs
- **[TESTES.md](TESTES.md)** - Documentação dos testes
- **[docs/rules.mdc](docs/rules.mdc)** - Padrões de desenvolvimento

## 🚀 Deploy

### Produção
```bash
# Configurar variáveis de produção
export DEBUG=False
export DATABASE_URL=postgresql://user:pass@host:port/db
export REDIS_URL=redis://host:port/db

# Instalar dependências
pip install -r requirements.txt

# Executar migrações
python manage.py migrate

# Coletar arquivos estáticos
python manage.py collectstatic

# Iniciar com Gunicorn
gunicorn ehit_backend.wsgi:application
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Add nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

**Igor Brandão**
- GitHub: [@igorbrandao18](https://github.com/igorbrandao18)

---

**🎵 Sistema Ehit - Backend completo e funcional!**