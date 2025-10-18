# terraform/environments/prod/outputs.tf
output "app_servers" {
  description = "Informações dos servidores de aplicação"
  value = {
    ips = module.infrastructure.droplet_ips
    count = length(module.infrastructure.droplet_ips)
  }
}

output "loadbalancer" {
  description = "Informações do load balancer"
  value = {
    ip = module.infrastructure.loadbalancer_ip
    endpoint = "https://${module.infrastructure.loadbalancer_ip}"
  }
}

output "database" {
  description = "Informações do banco de dados"
  value = {
    uri = module.infrastructure.database_uri
    endpoint = "Private endpoint (VPC only)"
  }
  sensitive = true
}

output "storage" {
  description = "Informações do armazenamento"
  value = {
    static_bucket = module.infrastructure.static_bucket
    media_bucket = module.infrastructure.media_bucket
  }
}

output "domain" {
  description = "Informações do domínio"
  value = {
    name = "ehitapp.com.br"
    admin_url = "https://ehitapp.com.br/admin/"
    api_url = "https://ehitapp.com.br/api/"
  }
}
