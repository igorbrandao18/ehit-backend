#!/bin/bash
# terraform/scripts/deploy.sh

set -e

ENVIRONMENT=$1
ACTION=$2

if [ -z "$ENVIRONMENT" ] || [ -z "$ACTION" ]; then
  echo "Uso: $0 [ambiente] [ação]"
  echo "Ambientes: dev, prod"
  echo "Ações: init, plan, apply, destroy, output"
  exit 1
fi

TERRAFORM_DIR="environments/$ENVIRONMENT"

if [ ! -d "$TERRAFORM_DIR" ]; then
  echo "Ambiente $ENVIRONMENT não encontrado!"
  exit 1
fi

cd "$TERRAFORM_DIR"

case "$ACTION" in
  init)
    echo "🚀 Inicializando Terraform para $ENVIRONMENT..."
    terraform init
    ;;
  plan)
    echo "📋 Planejando mudanças para $ENVIRONMENT..."
    terraform plan
    ;;
  apply)
    echo "🏗️ Aplicando mudanças para $ENVIRONMENT..."
    terraform apply
    ;;
  destroy)
    echo "💥 Destruindo infraestrutura de $ENVIRONMENT..."
    terraform destroy
    ;;
  output)
    echo "📊 Outputs de $ENVIRONMENT:"
    terraform output
    ;;
  *)
    echo "Ação inválida: $ACTION"
    exit 1
    ;;
esac
