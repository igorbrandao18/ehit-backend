# terraform/modules/digitalocean/main.tf
terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

# Variáveis do módulo
variable "project_name" {
  description = "Nome do projeto"
  type        = string
}

variable "environment" {
  description = "Ambiente (dev, prod)"
  type        = string
}

variable "region" {
  description = "Região do DigitalOcean"
  type        = string
  default     = "nyc3"
}

variable "droplet_size" {
  description = "Tamanho do droplet"
  type        = string
  default     = "s-2vcpu-4gb"
}

variable "domain_name" {
  description = "Nome do domínio"
  type        = string
}

variable "ssh_key_fingerprint" {
  description = "Fingerprint da chave SSH"
  type        = string
}

variable "github_token" {
  description = "Token do GitHub para registry"
  type        = string
  sensitive   = true
}

# Data sources
data "digitalocean_ssh_key" "main" {
  fingerprint = var.ssh_key_fingerprint
}

# Projeto
resource "digitalocean_project" "main" {
  name        = "${var.project_name}-${var.environment}"
  description = "Projeto ${var.project_name} para ambiente ${var.environment}"
  purpose     = "Web Application"
  environment = var.environment == "prod" ? "Production" : "Development"
}

# VPC
resource "digitalocean_vpc" "main" {
  name     = "${var.project_name}-${var.environment}-vpc"
  region   = var.region
  ip_range = "10.10.0.0/16"
}

# Database Cluster
resource "digitalocean_database_cluster" "postgres" {
  name       = "${var.project_name}-${var.environment}-db"
  engine     = "pg"
  version    = "15"
  size       = var.environment == "prod" ? "db-s-2vcpu-4gb" : "db-s-1vcpu-1gb"
  region     = var.region
  node_count = 1
  vpc_uuid   = digitalocean_vpc.main.id

  tags = [
    "${var.project_name}",
    var.environment,
    "database"
  ]
}

# Database User
resource "digitalocean_database_user" "app_user" {
  cluster_id = digitalocean_database_cluster.postgres.id
  name       = "ehit_user"
}

# Database Database
resource "digitalocean_database_db" "app_db" {
  cluster_id = digitalocean_database_cluster.postgres.id
  name       = "ehit_db"
}

# Spaces (Object Storage)
resource "digitalocean_spaces_bucket" "static_files" {
  name   = "${var.project_name}-${var.environment}-static"
  region = var.region
}

resource "digitalocean_spaces_bucket" "media_files" {
  name   = "${var.project_name}-${var.environment}-media"
  region = var.region
}

# Load Balancer
resource "digitalocean_loadbalancer" "main" {
  name   = "${var.project_name}-${var.environment}-lb"
  region = var.region
  vpc_uuid = digitalocean_vpc.main.id

  forwarding_rule {
    entry_protocol  = "http"
    entry_port      = 80
    target_protocol = "http"
    target_port     = 80
  }

  forwarding_rule {
    entry_protocol  = "https"
    entry_port      = 443
    target_protocol = "http"
    target_port     = 80
    tls_passthrough = true
  }

  healthcheck {
    protocol               = "http"
    port                   = 80
    path                   = "/health/"
    check_interval_seconds = 10
    response_timeout_seconds = 5
    unhealthy_threshold     = 3
    healthy_threshold       = 2
  }

  tags = [
    "${var.project_name}",
    var.environment,
    "loadbalancer"
  ]
}

# Droplet
resource "digitalocean_droplet" "app" {
  count    = var.environment == "prod" ? 2 : 1
  name     = "${var.project_name}-${var.environment}-app-${count.index + 1}"
  image    = "docker-20-04"
  size     = var.droplet_size
  region   = var.region
  vpc_uuid = digitalocean_vpc.main.id

  ssh_keys = [data.digitalocean_ssh_key.main.id]

  user_data = templatefile("${path.module}/cloud-init.yml", {
    project_name    = var.project_name
    environment     = var.environment
    database_url    = digitalocean_database_cluster.postgres.private_uri
    static_bucket   = digitalocean_spaces_bucket.static_files.name
    media_bucket    = digitalocean_spaces_bucket.media_files.name
    domain_name     = var.domain_name
    github_token    = var.github_token
  })

  tags = [
    "${var.project_name}",
    var.environment,
    "app-server"
  ]
}

# Firewall
resource "digitalocean_firewall" "main" {
  name = "${var.project_name}-${var.environment}-firewall"

  droplet_ids = digitalocean_droplet.app[*].id

  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "80"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "443"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "tcp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "udp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
}

# Domain
resource "digitalocean_domain" "main" {
  name = var.domain_name
}

# DNS Records
resource "digitalocean_record" "app" {
  count  = length(digitalocean_droplet.app)
  domain = digitalocean_domain.main.name
  type   = "A"
  name   = var.environment == "prod" ? "@" : var.environment
  value  = digitalocean_droplet.app[count.index].ipv4_address
  ttl    = 300
}

resource "digitalocean_record" "loadbalancer" {
  domain = digitalocean_domain.main.name
  type   = "A"
  name   = "lb"
  value  = digitalocean_loadbalancer.main.ip
  ttl    = 300
}

# Outputs
output "droplet_ips" {
  description = "IPs dos droplets"
  value       = digitalocean_droplet.app[*].ipv4_address
}

output "database_uri" {
  description = "URI do banco de dados"
  value       = digitalocean_database_cluster.postgres.private_uri
  sensitive   = true
}

output "loadbalancer_ip" {
  description = "IP do load balancer"
  value       = digitalocean_loadbalancer.main.ip
}

output "static_bucket" {
  description = "Nome do bucket de arquivos estáticos"
  value       = digitalocean_spaces_bucket.static_files.name
}

output "media_bucket" {
  description = "Nome do bucket de arquivos de mídia"
  value       = digitalocean_spaces_bucket.media_files.name
}
