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

# Data sources
data "digitalocean_ssh_key" "main" {
  fingerprint = var.ssh_key_fingerprint
}

# VPC
resource "digitalocean_vpc" "main" {
  name     = "ehit-prod-vpc"
  region   = "nyc3"
  ip_range = "10.10.0.0/16"
}

# Database Cluster
resource "digitalocean_database_cluster" "postgres" {
  name       = "ehit-prod-db"
  engine     = "pg"
  version    = "15"
  size       = "db-s-2vcpu-4gb"
  region     = "nyc3"
  node_count = 1
  vpc_uuid   = digitalocean_vpc.main.id

  tags = [
    "ehit",
    "prod",
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

# Droplet
resource "digitalocean_droplet" "app" {
  count    = 1
  name     = "ehit-prod-app-${count.index + 1}"
  image    = "docker-20-04"
  size     = "s-2vcpu-4gb"
  region   = "nyc3"
  vpc_uuid = digitalocean_vpc.main.id

  ssh_keys = [data.digitalocean_ssh_key.main.id]

  user_data = templatefile("${path.module}/../../modules/digitalocean/cloud-init.yml", {
    database_url = digitalocean_database_cluster.postgres.private_uri
    domain_name  = "ehitapp.com.br"
  })

  tags = [
    "ehit",
    "prod",
    "app-server"
  ]
}

# Firewall
resource "digitalocean_firewall" "main" {
  name = "ehit-prod-firewall"

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
  name = "ehitapp.com.br"
}

# DNS Records
resource "digitalocean_record" "app" {
  count  = length(digitalocean_droplet.app)
  domain = digitalocean_domain.main.name
  type   = "A"
  name   = "@"
  value  = digitalocean_droplet.app[count.index].ipv4_address
  ttl    = 300
}

# Outputs
output "app_ips" {
  description = "IPs dos servidores de aplicação"
  value       = digitalocean_droplet.app[*].ipv4_address
}

output "database_uri" {
  description = "URI do banco de dados"
  value       = digitalocean_database_cluster.postgres.private_uri
  sensitive   = true
}
