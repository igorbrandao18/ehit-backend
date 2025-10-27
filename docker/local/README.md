# Docker Local - Desenvolvimento Local

Este ambiente é para desenvolvimento local usando apenas banco de dados e Redis em containers, enquanto o Django roda localmente.

## 🚀 Como usar

### Opção 1: Script de conveniência
```bash
# Iniciar apenas banco e Redis
./docker-scripts.sh local up

# Parar serviços
./docker-scripts.sh local down

# Ver logs
./docker-scripts.sh local logs

# Ver status
./docker-scripts.sh local status
```

### Opção 2: Docker Compose direto
```bash
# Iniciar serviços
docker-compose -f docker/local/docker-compose.yml up -d

# Parar serviços
docker-compose -f docker/local/docker-compose.yml down

# Ver logs
docker-compose -f docker/local/docker-compose.yml logs -f
```

## 🔧 Configuração

Após iniciar os containers, configure seu `.env` local:

```bash
# .env para desenvolvimento local com Docker
SECRET_KEY=sua-chave-secreta-local
DEBUG=True
ENVIRONMENT=development

# Ativar o uso do Docker
USE_DOCKER=True

# Configurações do PostgreSQL (docker/local)
DB_NAME=ehit_db
DB_USER=ehit_user
DB_PASSWORD=ehit_password
DB_HOST=localhost
DB_PORT=5433

# Configuração do Redis (docker/local)
REDIS_URL=redis://localhost:6380/0
```

### Opção sem Docker (SQLite + LocMemCache)
Se preferir não usar Docker, simplesmente não defina `USE_DOCKER` ou defina como `False`:
```bash
USE_DOCKER=False
# Ou não defina a variável
```

## 🏃 Executar Django localmente

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar migrações no PostgreSQL
python manage.py migrate

# 3. Criar superusuário (opcional)
python manage.py createsuperuser

# 4. Executar servidor de desenvolvimento
python manage.py runserver
```

### 🔄 Primeira vez usando Docker?

Se você já tinha dados no SQLite e quer migrar para PostgreSQL:

```bash
# 1. Backup do SQLite
cp db.sqlite3 db.sqlite3.backup

# 2. Iniciar Docker
docker-compose -f docker/local/docker-compose.yml up -d

# 3. Configurar .env com USE_DOCKER=True

# 4. Rodar migrações
python manage.py migrate

# 5. (Opcional) Carregar dados de fixtures ou scripts
```

## 📊 Portas

- **PostgreSQL**: 5433 (para não conflitar com instalação local)
- **Redis**: 6380 (para não conflitar com instalação local)
- **Django**: 8000 (rodando localmente)

## 🗂️ Volumes

- `postgres_local_data`: Dados do PostgreSQL
- `redis_local_data`: Dados do Redis

## 🔍 Troubleshooting

### Porta já em uso
```bash
# Verificar o que está usando a porta
lsof -i :5433
lsof -i :6380

# Parar containers conflitantes
docker stop ehit_postgres_local ehit_redis_local
```

### Resetar dados
```bash
# Parar e remover volumes
docker-compose -f docker/local/docker-compose.yml down -v

# Iniciar novamente
docker-compose -f docker/local/docker-compose.yml up -d
```

## ⚡ Resumo: Qual opção usar?

### SQLite (USE_DOCKER=False ou não definido)
✅ **Melhor para:** Começar rapidamente, testes rápidos, desenvolvimento simples
- Não precisa de Docker
- Setup instantâneo
- Dados ficam no arquivo `db.sqlite3`

### Docker PostgreSQL + Redis (USE_DOCKER=True)
✅ **Melhor para:** Desenvolvimento real, testar features que precisam PostgreSQL, simular ambiente de produção
- Ambiente mais próximo da produção
- PostgreSQL completo com recursos avançados
- Redis para cache e sessões
- Precisa do Docker rodando
