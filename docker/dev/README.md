# Docker Dev - Desenvolvimento com Containers

Este ambiente é para desenvolvimento usando containers para todos os serviços, incluindo Django.

## 🚀 Como usar

### Opção 1: Script de conveniência
```bash
# Iniciar ambiente de desenvolvimento
./docker-scripts.sh dev up

# Parar ambiente
./docker-scripts.sh dev down

# Ver logs
./docker-scripts.sh dev logs

# Entrar no shell do container
./docker-scripts.sh dev shell

# Rebuild completo
./docker-scripts.sh dev build

# Ver status
./docker-scripts.sh dev status
```

### Opção 2: Docker Compose direto
```bash
# Iniciar ambiente
docker-compose -f docker/dev/docker-compose.yml up -d

# Parar ambiente
docker-compose -f docker/dev/docker-compose.yml down

# Rebuild com mudanças
docker-compose -f docker/dev/docker-compose.yml up -d --build

# Ver logs
docker-compose -f docker/dev/docker-compose.yml logs -f

# Entrar no container Django
docker-compose -f docker/dev/docker-compose.yml exec web bash
```

## 🔧 Configuração

O ambiente usa as seguintes configurações:

```bash
# Variáveis de ambiente automáticas
DEBUG=True
DATABASE_URL=postgresql://ehit_user:ehit_password@db:5432/ehit_db
REDIS_URL=redis://redis:6379/0
```

## 📊 Portas

- **PostgreSQL**: 5432
- **Redis**: 6379
- **Django**: 8000

## 🗂️ Volumes

- `postgres_dev_data`: Dados do PostgreSQL
- `redis_dev_data`: Dados do Redis
- `static_dev_volume`: Arquivos estáticos
- `media_dev_volume`: Arquivos de mídia
- `../../:/app`: Código fonte (bind mount para desenvolvimento)

## 🔄 Hot Reload

O código fonte é montado como volume, então mudanças são refletidas automaticamente.

## 🛠️ Comandos úteis

```bash
# Executar migrações
docker-compose -f docker/dev/docker-compose.yml exec web python manage.py migrate

# Criar superusuário
docker-compose -f docker/dev/docker-compose.yml exec web python manage.py createsuperuser

# Executar testes
docker-compose -f docker/dev/docker-compose.yml exec web python manage.py test

# Coletar arquivos estáticos
docker-compose -f docker/dev/docker-compose.yml exec web python manage.py collectstatic

# Shell do Django
docker-compose -f docker/dev/docker-compose.yml exec web python manage.py shell
```

## 🔍 Troubleshooting

### Container não inicia
```bash
# Ver logs detalhados
docker-compose -f docker/dev/docker-compose.yml logs web

# Rebuild completo
docker-compose -f docker/dev/docker-compose.yml down
docker-compose -f docker/dev/docker-compose.yml up -d --build
```

### Problemas de permissão
```bash
# Verificar permissões dos volumes
docker-compose -f docker/dev/docker-compose.yml exec web ls -la /app

# Resetar volumes
docker-compose -f docker/dev/docker-compose.yml down -v
docker-compose -f docker/dev/docker-compose.yml up -d
```

### Banco de dados não conecta
```bash
# Verificar se PostgreSQL está rodando
docker-compose -f docker/dev/docker-compose.yml exec db pg_isready

# Testar conexão
docker-compose -f docker/dev/docker-compose.yml exec web python manage.py dbshell
```
