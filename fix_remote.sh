#!/bin/bash

SERVER="165.227.180.118"
echo "🔧 EHIT BACKEND - CORREÇÃO AUTOMÁTICA VIA SSH"
echo "=============================================="
echo ""

echo "📡 Conectando ao servidor $SERVER..."
echo ""

# 1. Verificar status atual
echo "📊 1. STATUS ATUAL DOS CONTAINERS:"
ssh root@$SERVER "cd /opt/ehit_backend && docker-compose -f docker/prod/docker-compose.yml ps"
echo ""

# 2. Ver logs de erro
echo "🔍 2. LOGS DE ERRO:"
ssh root@$SERVER "cd /opt/ehit_backend && echo '---WEB LOGS---' && docker-compose -f docker/prod/docker-compose.yml logs --tail=10 web && echo '---NGINX LOGS---' && docker-compose -f docker/prod/docker-compose.yml logs --tail=10 nginx"
echo ""

# 3. Parar containers
echo "🛑 3. PARANDO CONTAINERS..."
ssh root@$SERVER "cd /opt/ehit_backend && docker-compose -f docker/prod/docker-compose.yml down"
echo ""

# 4. Limpar sistema
echo "🗑️ 4. LIMPANDO SISTEMA..."
ssh root@$SERVER "docker system prune -f"
echo ""

# 5. Atualizar código
echo "📥 5. ATUALIZANDO CÓDIGO..."
ssh root@$SERVER "cd /opt/ehit_backend && git pull origin main"
echo ""

# 6. Rebuild completo
echo "🔨 6. REBUILD COMPLETO..."
ssh root@$SERVER "cd /opt/ehit_backend && docker-compose -f docker/prod/docker-compose.yml up -d --build --force-recreate --no-deps"
echo ""

# 7. Aguardar inicialização
echo "⏳ 7. AGUARDANDO INICIALIZAÇÃO..."
sleep 30
echo ""

# 8. Verificar status final
echo "📊 8. STATUS FINAL:"
ssh root@$SERVER "cd /opt/ehit_backend && docker-compose -f docker/prod/docker-compose.yml ps"
echo ""

# 9. Teste final
echo "🌐 9. TESTE FINAL:"
ssh root@$SERVER "curl -f http://prod.ehitapp.com.br/health/ && echo '✅ SITE FUNCIONANDO!' || echo '❌ AINDA COM PROBLEMAS'"
echo ""

echo "🎉 CORREÇÃO CONCLUÍDA!"
echo "Se ainda houver problemas, execute: ssh root@$SERVER './debug_502.sh'"
