# terraform/environments/prod/main.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

# Provider configuration
provider "digitalocean" {
  token = var.digitalocean_token
}

# Módulo principal
module "infrastructure" {
  source = "../../modules/digitalocean"

  project_name        = "ehit"
  environment        = "prod"
  region            = "nyc3"
  droplet_size      = "s-4vcpu-8gb"
  domain_name       = "ehitapp.com.br"
  ssh_key_fingerprint = var.ssh_key_fingerprint
  github_token      = var.github_token
}

# Outputs
output "app_ips" {
  description = "IPs dos servidores de aplicação"
  value       = module.infrastructure.droplet_ips
}

output "loadbalancer_ip" {
  description = "IP do load balancer"
  value       = module.infrastructure.loadbalancer_ip
}

output "database_uri" {
  description = "URI do banco de dados"
  value       = module.infrastructure.database_uri
  sensitive   = true
}
