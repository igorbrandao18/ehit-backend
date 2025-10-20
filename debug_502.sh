#!/bin/bash

echo "🔍 DIAGNÓSTICO DE ERRO 502 - EHIT BACKEND"
echo "=========================================="
echo ""

# 1. Verificar status dos containers
echo "📊 1. STATUS DOS CONTAINERS:"
echo "----------------------------"
docker-compose -f /opt/ehit_backend/docker/prod/docker-compose.yml ps
echo ""

# 2. Verificar logs do nginx
echo "🌐 2. LOGS DO NGINX (últimas 20 linhas):"
echo "----------------------------------------"
docker-compose -f /opt/ehit_backend/docker/prod/docker-compose.yml logs --tail=20 nginx
echo ""

# 3. Verificar logs do Django
echo "🐍 3. LOGS DO DJANGO (últimas 20 linhas):"
echo "------------------------------------------"
docker-compose -f /opt/ehit_backend/docker/prod/docker-compose.yml logs --tail=20 web
echo ""

# 4. Verificar se o Django está respondendo internamente
echo "🔗 4. TESTE DE CONECTIVIDADE INTERNA:"
echo "------------------------------------"
echo "Testando conexão direta com Django (porta 8000):"
docker-compose -f /opt/ehit_backend/docker/prod/docker-compose.yml exec -T web curl -f http://localhost:8000/health/ || echo "❌ Django não está respondendo na porta 8000"
echo ""

# 5. Verificar se o nginx consegue conectar no Django
echo "🔗 5. TESTE NGINX -> DJANGO:"
echo "----------------------------"
docker-compose -f /opt/ehit_backend/docker/prod/docker-compose.yml exec -T nginx curl -f http://web:8000/health/ || echo "❌ Nginx não consegue conectar no Django"
echo ""

# 6. Verificar configuração do nginx
echo "⚙️ 6. CONFIGURAÇÃO DO NGINX:"
echo "----------------------------"
docker-compose -f /opt/ehit_backend/docker/prod/docker-compose.yml exec -T nginx nginx -t
echo ""

# 7. Verificar portas em uso
echo "🔌 7. PORTAS EM USO:"
echo "-------------------"
netstat -tlnp | grep -E ':(80|443|8000|5432|6379)'
echo ""

# 8. Verificar recursos do sistema
echo "💻 8. RECURSOS DO SISTEMA:"
echo "-------------------------"
echo "CPU e Memória:"
top -bn1 | head -5
echo ""
echo "Espaço em disco:"
df -h
echo ""

# 9. Verificar se os certificados SSL existem
echo "🔒 9. CERTIFICADOS SSL:"
echo "----------------------"
if [ -f "/etc/letsencrypt/live/prod.ehitapp.com.br/fullchain.pem" ]; then
    echo "✅ Certificado SSL encontrado"
    ls -la /etc/letsencrypt/live/prod.ehitapp.com.br/
else
    echo "❌ Certificado SSL não encontrado"
fi
echo ""

echo "🎯 PRÓXIMOS PASSOS:"
echo "==================="
echo "1. Se Django não está respondendo: reiniciar container web"
echo "2. Se nginx não consegue conectar: verificar rede Docker"
echo "3. Se certificado SSL não existe: configurar Let's Encrypt"
echo "4. Se containers estão com problemas: rebuild completo"
echo ""
echo "✅ Diagnóstico concluído!"
