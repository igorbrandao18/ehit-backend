# README - ehit_backend

## 🚀 Projeto Django com Docker

Este é um projeto Django configurado com Docker, PostgreSQL e Redis para cache.

## 📋 Pré-requisitos

- Docker
- Docker Compose

## 🛠️ Configuração

1. **Clone o repositório e navegue até o diretório:**
   ```bash
   cd ehit_backend
   ```

2. **Copie o arquivo de variáveis de ambiente:**
   ```bash
   cp .env.example .env
   ```

3. **Edite o arquivo `.env` com suas configurações:**
   ```bash
   nano .env
   ```

4. **Execute o projeto com Docker Compose:**
   ```bash
   docker-compose up --build
   ```

## 🐳 Serviços Docker

- **PostgreSQL**: Banco de dados principal (porta 5432)
- **Redis**: Cache e broker para Celery (porta 6379)
- **Django**: Aplicação web (porta 8000)

## 📁 Estrutura do Projeto

```
ehit_backend/
├── docker-compose.yml      # Configuração dos serviços Docker
├── Dockerfile             # Imagem Docker para Django
├── requirements.txt       # Dependências Python
├── .env.example          # Exemplo de variáveis de ambiente
├── .gitignore            # Arquivos ignorados pelo Git
├── manage.py             # Script de gerenciamento Django
└── ehit_backend/         # Diretório principal do projeto
    ├── settings.py       # Configurações do Django
    ├── urls.py          # Roteamento de URLs
    ├── wsgi.py          # Configuração WSGI
    └── asgi.py          # Configuração ASGI
```

## 🔧 Comandos Úteis

### Desenvolvimento
```bash
# Subir os serviços
docker-compose up

# Subir em background
docker-compose up -d

# Parar os serviços
docker-compose down

# Ver logs
docker-compose logs -f

# Executar comandos Django
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic
```

### Banco de Dados
```bash
# Acessar PostgreSQL
docker-compose exec db psql -U ehit_user -d ehit_db

# Fazer backup
docker-compose exec db pg_dump -U ehit_user ehit_db > backup.sql
```

### Redis
```bash
# Acessar Redis CLI
docker-compose exec redis redis-cli

# Monitorar Redis
docker-compose exec redis redis-cli monitor
```

## 🌐 Acessos

- **Django Admin**: http://localhost:8000/admin/
- **API**: http://localhost:8000/api/
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## 📦 Tecnologias

- **Django 5.2.7**: Framework web
- **PostgreSQL 15**: Banco de dados
- **Redis 7**: Cache e broker
- **Django REST Framework**: API REST
- **Celery**: Tarefas assíncronas
- **Docker**: Containerização

## 🔒 Variáveis de Ambiente

Configure as seguintes variáveis no arquivo `.env`:

```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://ehit_user:ehit_password@db:5432/ehit_db
REDIS_URL=redis://redis:6379/0
```

## 🚀 Deploy

Para produção, certifique-se de:

1. Alterar `DEBUG=False`
2. Configurar `ALLOWED_HOSTS` adequadamente
3. Usar uma `SECRET_KEY` segura
4. Configurar SSL/TLS
5. Usar um banco de dados externo se necessário

## 📝 Licença

Este projeto está sob a licença MIT.
