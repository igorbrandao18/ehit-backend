#!/bin/bash

# Scripts de conveniência para Docker EHIT
# Uso: ./docker-scripts.sh [local|dev|prod] [up|down|logs|shell]

ENVIRONMENT=${1:-local}
ACTION=${2:-up}

case $ENVIRONMENT in
    "local")
        COMPOSE_FILE="docker/local/docker-compose.yml"
        ;;
    "dev")
        COMPOSE_FILE="docker/dev/docker-compose.yml"
        ;;
    "prod")
        COMPOSE_FILE="docker/prod/docker-compose.yml"
        ;;
    *)
        echo "❌ Ambiente inválido. Use: local, dev ou prod"
        exit 1
        ;;
esac

case $ACTION in
    "up")
        echo "🚀 Iniciando ambiente $ENVIRONMENT..."
        docker-compose -f $COMPOSE_FILE up -d
        ;;
    "down")
        echo "🛑 Parando ambiente $ENVIRONMENT..."
        docker-compose -f $COMPOSE_FILE down
        ;;
    "logs")
        echo "📋 Mostrando logs do ambiente $ENVIRONMENT..."
        docker-compose -f $COMPOSE_FILE logs -f
        ;;
    "shell")
        echo "🐚 Entrando no shell do ambiente $ENVIRONMENT..."
        docker-compose -f $COMPOSE_FILE exec web bash
        ;;
    "build")
        echo "🔨 Construindo ambiente $ENVIRONMENT..."
        docker-compose -f $COMPOSE_FILE up -d --build
        ;;
    "status")
        echo "📊 Status do ambiente $ENVIRONMENT..."
        docker-compose -f $COMPOSE_FILE ps
        ;;
    *)
        echo "❌ Ação inválida. Use: up, down, logs, shell, build, status"
        exit 1
        ;;
esac
