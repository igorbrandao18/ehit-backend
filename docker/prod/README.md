# Docker Prod - Produção

Este ambiente é para produção com Nginx, Gunicorn e otimizações de segurança.

## 🚀 Como usar

### Opção 1: Script de conveniência
```bash
# Deploy completo para produção
./docker-scripts.sh prod build

# Parar ambiente de produção
./docker-scripts.sh prod down

# Ver logs
./docker-scripts.sh prod logs

# Ver status
./docker-scripts.sh prod status

# Entrar no shell do container
./docker-scripts.sh prod shell
```

### Opção 2: Docker Compose direto
```bash
# Deploy completo
docker-compose -f docker/prod/docker-compose.yml up -d --build

# Parar ambiente
docker-compose -f docker/prod/docker-compose.yml down

# Ver logs
docker-compose -f docker/prod/docker-compose.yml logs -f

# Ver logs específicos
docker-compose -f docker/prod/docker-compose.yml logs web
docker-compose -f docker/prod/docker-compose.yml logs nginx
```

## 🔧 Configuração

### Variáveis de ambiente necessárias

Crie um arquivo `.env` na raiz do projeto:

```bash
# .env para produção
SECRET_KEY=sua-chave-secreta-super-segura
DEBUG=False
DATABASE_URL=postgresql://ehit_user:ehit_password@db:5432/ehit_db
REDIS_URL=redis://redis:6379/0
ALLOWED_HOSTS=prod.ehitapp.com.br,165.227.180.118,localhost
SECURE_SSL_REDIRECT=True
SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## 📊 Portas

- **Nginx**: 80 (HTTP), 443 (HTTPS)
- **PostgreSQL**: 5432 (interno)
- **Redis**: 6379 (interno)
- **Django**: 8000 (interno, via Nginx)

## 🗂️ Volumes

- `postgres_prod_data`: Dados do PostgreSQL
- `redis_prod_data`: Dados do Redis
- `static_prod_volume`: Arquivos estáticos
- `media_prod_volume`: Arquivos de mídia
- `/etc/letsencrypt`: Certificados SSL

## 🔒 Segurança

- Usuário não-root (`appuser`)
- Headers de segurança no Nginx
- SSL/TLS obrigatório
- Rate limiting
- Health checks automáticos

## 🛠️ Comandos úteis

```bash
# Executar migrações
docker-compose -f docker/prod/docker-compose.yml exec web python manage.py migrate

# Criar superusuário
docker-compose -f docker/prod/docker-compose.yml exec web python manage.py createsuperuser

# Coletar arquivos estáticos
docker-compose -f docker/prod/docker-compose.yml exec web python manage.py collectstatic --noinput

# Verificar logs do Nginx
docker-compose -f docker/prod/docker-compose.yml logs nginx

# Testar configuração do Nginx
docker-compose -f docker/prod/docker-compose.yml exec nginx nginx -t

# Recarregar Nginx
docker-compose -f docker/prod/docker-compose.yml exec nginx nginx -s reload
```

## 🔍 Monitoramento

### Health Checks

```bash
# Health check interno
curl http://localhost:8000/health/

# Health check via Nginx
curl https://prod.ehitapp.com.br/health/

# Status dos containers
docker-compose -f docker/prod/docker-compose.yml ps
```

### Logs

```bash
# Logs em tempo real
docker-compose -f docker/prod/docker-compose.yml logs -f

# Logs específicos
docker-compose -f docker/prod/docker-compose.yml logs web --tail=100
docker-compose -f docker/prod/docker-compose.yml logs nginx --tail=100
```

## 🔄 Deploy

### Deploy manual

```bash
# 1. Parar ambiente atual
docker-compose -f docker/prod/docker-compose.yml down

# 2. Fazer backup dos volumes (opcional)
docker run --rm -v ehit_backend_postgres_prod_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz -C /data .

# 3. Deploy novo
docker-compose -f docker/prod/docker-compose.yml up -d --build

# 4. Executar migrações
docker-compose -f docker/prod/docker-compose.yml exec web python manage.py migrate

# 5. Coletar estáticos
docker-compose -f docker/prod/docker-compose.yml exec web python manage.py collectstatic --noinput
```

### Deploy automático via GitHub Actions

O deploy automático está configurado no GitHub Actions e executa:

1. ✅ Testes automatizados
2. 🐳 Build da imagem Docker
3. 📤 Push para GitHub Container Registry
4. 🚀 Deploy no servidor
5. 🔒 SSL automático com Let's Encrypt
6. 🏥 Health checks

## 🔍 Troubleshooting

### Container não inicia
```bash
# Ver logs detalhados
docker-compose -f docker/prod/docker-compose.yml logs web

# Verificar configuração
docker-compose -f docker/prod/docker-compose.yml config

# Rebuild completo
docker-compose -f docker/prod/docker-compose.yml down
docker-compose -f docker/prod/docker-compose.yml up -d --build
```

### Problemas de SSL
```bash
# Verificar certificados
ls -la /etc/letsencrypt/live/prod.ehitapp.com.br/

# Renovar certificados
certbot renew --nginx

# Testar SSL
curl -I https://prod.ehitapp.com.br
```

### Problemas de performance
```bash
# Verificar recursos
docker stats

# Verificar logs de erro
docker-compose -f docker/prod/docker-compose.yml logs nginx | grep error

# Verificar configuração do Nginx
docker-compose -f docker/prod/docker-compose.yml exec nginx nginx -T
```
