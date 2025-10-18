# Terraform Infrastructure

Este diretório contém a configuração de infraestrutura como código usando Terraform para o projeto EHIT.

## 🏗️ Arquitetura

### Recursos Criados:
- **Droplets**: Servidores de aplicação (2x para produção)
- **Database Cluster**: PostgreSQL gerenciado
- **Load Balancer**: Distribuição de carga com SSL
- **Spaces**: Armazenamento de arquivos estáticos e mídia
- **VPC**: Rede privada para comunicação segura
- **Firewall**: Regras de segurança
- **Domain**: Configuração DNS automática

### Ambientes:
- **dev**: Ambiente de desenvolvimento (1 servidor)
- **prod**: Ambiente de produção (2 servidores + load balancer)

## 🚀 Como Usar

### 1. Configuração Inicial

```bash
# Instalar Terraform
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install terraform

# Instalar DigitalOcean CLI
snap install doctl
doctl auth init
```

### 2. Configurar Variáveis

```bash
# Copiar arquivo de exemplo
cp terraform/environments/prod/terraform.tfvars.example terraform/environments/prod/terraform.tfvars

# Editar com seus valores
nano terraform/environments/prod/terraform.tfvars
```

### 3. Deploy

```bash
# Usando script helper
./terraform/scripts/deploy.sh prod init
./terraform/scripts/deploy.sh prod plan
./terraform/scripts/deploy.sh prod apply

# Ou diretamente
cd terraform/environments/prod
terraform init
terraform plan
terraform apply
```

## 🔑 Variáveis Necessárias

### DigitalOcean Token
1. Acesse: https://cloud.digitalocean.com/account/api/tokens
2. Crie um novo token com permissões de leitura e escrita
3. Adicione ao `terraform.tfvars`

### SSH Key Fingerprint
```bash
# Listar chaves SSH
doctl compute ssh-key list

# Ou adicionar nova chave
doctl compute ssh-key create "ehit-key" --public-key-file ~/.ssh/id_rsa.pub
```

### GitHub Token
1. Acesse: https://github.com/settings/tokens
2. Crie um token com permissões de `packages:read`
3. Adicione ao `terraform.tfvars`

## 📊 Outputs

Após o deploy, você pode ver os outputs:

```bash
terraform output
```

### Principais URLs:
- **Admin**: https://ehitapp.com.br/admin/
- **API**: https://ehitapp.com.br/api/
- **Health Check**: https://ehitapp.com.br/health/

## 🔧 Comandos Úteis

```bash
# Ver estado atual
terraform show

# Listar recursos
terraform state list

# Importar recurso existente
terraform import digitalocean_droplet.app[0] droplet_id

# Destruir infraestrutura
terraform destroy
```

## 🏗️ Estrutura de Arquivos

```
terraform/
├── modules/
│   └── digitalocean/
│       ├── main.tf              # Recursos principais
│       └── cloud-init.yml       # Configuração dos droplets
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── prod/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       └── terraform.tfvars.example
└── scripts/
    └── deploy.sh                # Script helper
```

## 🔒 Segurança

- Todos os recursos são criados em VPC privada
- Firewall configurado com regras mínimas necessárias
- SSL/TLS automático com Let's Encrypt
- Banco de dados acessível apenas via VPC
- Chaves SSH obrigatórias para acesso

## 💰 Custos Estimados (Produção)

- **2x Droplets s-4vcpu-8gb**: ~$96/mês
- **Database Cluster**: ~$60/mês
- **Load Balancer**: ~$12/mês
- **Spaces (250GB)**: ~$5/mês
- **Total**: ~$173/mês

## 🆘 Troubleshooting

### Erro de SSH Key
```bash
# Verificar chaves disponíveis
doctl compute ssh-key list

# Adicionar nova chave
doctl compute ssh-key create "ehit-key" --public-key-file ~/.ssh/id_rsa.pub
```

### Erro de Token
```bash
# Verificar token
doctl account get

# Renovar token se necessário
```

### Erro de Domínio
```bash
# Verificar configuração DNS
dig ehitapp.com.br

# Aguardar propagação DNS (até 24h)
```
