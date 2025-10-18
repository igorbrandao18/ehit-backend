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
# .env para desenvolvimento local
SECRET_KEY=sua-chave-secreta-local
DEBUG=True
DATABASE_URL=postgresql://ehit_user:ehit_password@localhost:5433/ehit_db
REDIS_URL=redis://localhost:6380/0
```

## 🏃 Executar Django localmente

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar migrações
python manage.py migrate

# Executar servidor de desenvolvimento
python manage.py runserver
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
