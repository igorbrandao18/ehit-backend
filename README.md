# EHIT Backend - Sistema de Música

Sistema backend para plataforma de música com Django, PostgreSQL, Redis e Docker.

## 🚀 Setup Simplificado

### Desenvolvimento Local

```bash
# Usar apenas banco e Redis
docker-compose --profile development up -d

# Executar Django localmente
python manage.py runserver
```

### Produção

```bash
# Deploy completo com Nginx
docker-compose --profile production up -d --build
```

## 📁 Estrutura Simplificada

- **`docker-compose.yml`** - Um arquivo para tudo (dev + prod)
- **`Dockerfile`** - Multi-stage build (dev + prod)
- **`nginx.conf`** - Configuração do Nginx
- **`.github/workflows/`** - CI/CD automatizado

## 🔧 Comandos Úteis

### Desenvolvimento
```bash
# Iniciar serviços de desenvolvimento
docker-compose --profile development up -d

# Parar serviços
docker-compose --profile development down

# Ver logs
docker-compose --profile development logs -f
```

### Produção
```bash
# Deploy completo
docker-compose --profile production up -d --build

# Migrações
docker-compose --profile production exec web python manage.py migrate

# Superusuário
docker-compose --profile production exec web python manage.py createsuperuser

# Logs
docker-compose --profile production logs -f web
```

## 🌐 URLs

- **Aplicação**: https://prod.ehitapp.com.br
- **Admin**: https://prod.ehitapp.com.br/admin
- **API**: https://prod.ehitapp.com.br/api/
- **Health Check**: https://prod.ehitapp.com.br/health/

## 📊 Monitoramento

- Health check automático no Docker
- Logs centralizados
- Métricas de performance
- SSL automático com Let's Encrypt

## 🔐 Credenciais Padrão

- **Admin**: admin / admin123
- **Banco**: ehit_user / ehit_password
- **Redis**: porta 6379

## 🚀 Deploy Automático

O GitHub Actions faz deploy automático quando você faz push para `main`:

1. ✅ Testes automatizados
2. 🐳 Build da imagem Docker
3. 📤 Push para GitHub Container Registry
4. 🚀 Deploy no servidor DigitalOcean
5. 🔒 SSL automático com Let's Encrypt
6. 🏥 Health checks

## 📝 Logs

```bash
# Ver logs em tempo real
docker-compose --profile production logs -f

# Logs específicos
docker-compose --profile production logs web
docker-compose --profile production logs nginx
docker-compose --profile production logs db
```

## 🛠️ Troubleshooting

### Problemas Comuns

1. **Porta 80 em uso**: `sudo systemctl stop nginx`
2. **Migrações falhando**: Verificar conexão com banco
3. **SSL não funciona**: Aguardar propagação DNS (até 24h)

### Comandos de Debug

```bash
# Status dos containers
docker-compose --profile production ps

# Entrar no container
docker-compose --profile production exec web bash

# Verificar logs do Nginx
docker-compose --profile production logs nginx

# Testar conectividade
curl -I https://prod.ehitapp.com.br/health/
```

## 📈 Performance

- **Nginx**: Proxy reverso com cache
- **Gunicorn**: 3 workers para produção
- **PostgreSQL**: Otimizado para produção
- **Redis**: Cache e sessões
- **SSL**: Let's Encrypt automático

## 🔄 CI/CD

O pipeline GitHub Actions inclui:

- ✅ Testes automatizados
- 🐳 Build multi-stage Docker
- 📦 Push para registry
- 🚀 Deploy zero-downtime
- 🔒 SSL automático
- 🏥 Health checks
- 📊 Monitoramento

## 📞 Suporte

Para problemas ou dúvidas:

1. Verificar logs: `docker-compose logs -f`
2. Health check: `curl https://prod.ehitapp.com.br/health/`
3. Status containers: `docker-compose ps`
4. GitHub Issues para bugs
5. Documentação completa na pasta `docs/`