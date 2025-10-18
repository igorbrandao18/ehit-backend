# EHIT Backend - Sistema de Música

Sistema backend para plataforma de música com Django, PostgreSQL, Redis e Docker.

## 🚀 Setup Simplificado com Ambientes Separados

### 📁 Estrutura de Ambientes

```
docker/
├── local/          # Desenvolvimento local (apenas DB + Redis)
├── dev/            # Desenvolvimento com containers
└── prod/           # Produção com Nginx
```

### 🛠️ Scripts de Conveniência

```bash
# Tornar executável (apenas uma vez)
chmod +x docker-scripts.sh

# Usar os scripts
./docker-scripts.sh [ambiente] [ação]

# Exemplos:
./docker-scripts.sh local up      # Iniciar ambiente local
./docker-scripts.sh dev build     # Build ambiente dev
./docker-scripts.sh prod logs     # Ver logs produção
```

## 🎯 Ambientes Disponíveis

### 1. **Local** - Desenvolvimento Local
```bash
# Apenas banco e Redis em containers, Django local
./docker-scripts.sh local up
python manage.py runserver
```
- **Portas**: PostgreSQL (5433), Redis (6380)
- **Uso**: Desenvolvimento com Django local
- **Docs**: [docker/local/README.md](docker/local/README.md)

### 2. **Dev** - Desenvolvimento com Containers
```bash
# Todos os serviços em containers
./docker-scripts.sh dev up
```
- **Portas**: PostgreSQL (5432), Redis (6379), Django (8000)
- **Uso**: Desenvolvimento completo com containers
- **Docs**: [docker/dev/README.md](docker/dev/README.md)

### 3. **Prod** - Produção
```bash
# Ambiente completo de produção
./docker-scripts.sh prod build
```
- **Portas**: Nginx (80/443), serviços internos
- **Uso**: Deploy em produção
- **Docs**: [docker/prod/README.md](docker/prod/README.md)

## 🔧 Comandos Rápidos

### Desenvolvimento Local
```bash
# Iniciar banco e Redis
./docker-scripts.sh local up

# Executar Django localmente
python manage.py runserver

# Parar serviços
./docker-scripts.sh local down
```

### Desenvolvimento com Containers
```bash
# Ambiente completo
./docker-scripts.sh dev up

# Entrar no container
./docker-scripts.sh dev shell

# Ver logs
./docker-scripts.sh dev logs
```

### Produção
```bash
# Deploy completo
./docker-scripts.sh prod build

# Ver status
./docker-scripts.sh prod status

# Ver logs
./docker-scripts.sh prod logs
```

## 🌐 URLs

- **Aplicação**: https://prod.ehitapp.com.br
- **Admin**: https://prod.ehitapp.com.br/admin
- **API**: https://prod.ehitapp.com.br/api/
- **Health Check**: https://prod.ehitapp.com.br/health/

## 📊 Monitoramento

- Health check automático no Docker
- Logs centralizados por ambiente
- Métricas de performance
- SSL automático com Let's Encrypt

## 🔐 Credenciais Padrão

- **Admin**: admin / admin123
- **Banco**: ehit_user / ehit_password
- **Redis**: porta padrão por ambiente

## 🚀 Deploy Automático

O GitHub Actions faz deploy automático quando você faz push para `main`:

1. ✅ Testes automatizados
2. 🐳 Build da imagem Docker
3. 📤 Push para GitHub Container Registry
4. 🚀 Deploy no servidor DigitalOcean
5. 🔒 SSL automático com Let's Encrypt
6. 🏥 Health checks

## 📝 Logs por Ambiente

```bash
# Logs específicos por ambiente
./docker-scripts.sh local logs
./docker-scripts.sh dev logs
./docker-scripts.sh prod logs

# Logs específicos de serviços
docker-compose -f docker/prod/docker-compose.yml logs nginx
docker-compose -f docker/prod/docker-compose.yml logs web
```

## 🛠️ Troubleshooting

### Problemas Comuns

1. **Porta em uso**: Verificar com `lsof -i :PORTA`
2. **Migrações falhando**: Verificar conexão com banco
3. **SSL não funciona**: Aguardar propagação DNS (até 24h)

### Comandos de Debug

```bash
# Status dos containers
./docker-scripts.sh [ambiente] status

# Entrar no container
./docker-scripts.sh [ambiente] shell

# Verificar logs
./docker-scripts.sh [ambiente] logs

# Resetar ambiente
./docker-scripts.sh [ambiente] down
./docker-scripts.sh [ambiente] up
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

1. Verificar logs: `./docker-scripts.sh [ambiente] logs`
2. Health check: `curl https://prod.ehitapp.com.br/health/`
3. Status containers: `./docker-scripts.sh [ambiente] status`
4. GitHub Issues para bugs
5. Documentação completa nas pastas `docker/[ambiente]/README.md`