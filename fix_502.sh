#!/bin/bash

echo "🔧 CORREÇÃO RÁPIDA - ERRO 502"
echo "=============================="
echo ""

# 1. Parar todos os containers
echo "🛑 1. Parando todos os containers..."
docker-compose -f /opt/ehit_backend/docker/prod/docker-compose.yml down
echo ""

# 2. Limpar containers e imagens órfãos
echo "🗑️ 2. Limpando containers e imagens órfãos..."
docker system prune -f
docker volume prune -f
echo ""

# 3. Verificar se o código está atualizado
echo "📥 3. Atualizando código..."
cd /opt/ehit_backend
git pull origin main
echo ""

# 4. Rebuild completo dos containers
echo "🔨 4. Rebuild completo dos containers..."
docker-compose -f docker/prod/docker-compose.yml up -d --build --force-recreate --no-deps
echo ""

# 5. Aguardar containers iniciarem
echo "⏳ 5. Aguardando containers iniciarem..."
sleep 30

# 6. Verificar se Django está respondendo
echo "🔍 6. Verificando se Django está respondendo..."
for i in {1..10}; do
    if docker-compose -f /opt/ehit_backend/docker/prod/docker-compose.yml exec -T web curl -f http://localhost:8000/health/ > /dev/null 2>&1; then
        echo "✅ Django está respondendo!"
        break
    else
        echo "⏳ Tentativa $i/10 - Aguardando Django..."
        sleep 10
    fi
done
echo ""

# 7. Verificar se nginx consegue conectar
echo "🔍 7. Verificando conectividade nginx -> Django..."
if docker-compose -f /opt/ehit_backend/docker/prod/docker-compose.yml exec -T nginx curl -f http://web:8000/health/ > /dev/null 2>&1; then
    echo "✅ Nginx consegue conectar no Django!"
else
    echo "❌ Nginx ainda não consegue conectar no Django"
fi
echo ""

# 8. Status final
echo "📊 8. STATUS FINAL DOS CONTAINERS:"
docker-compose -f /opt/ehit_backend/docker/prod/docker-compose.yml ps
echo ""

# 9. Teste final
echo "🌐 9. TESTE FINAL:"
echo "Testando http://prod.ehitapp.com.br/health/"
curl -f http://prod.ehitapp.com.br/health/ && echo "✅ Site funcionando!" || echo "❌ Ainda com problemas"
echo ""

echo "🎉 Correção concluída!"
echo "Se ainda houver erro 502, execute o script de diagnóstico: ./debug_502.sh"
