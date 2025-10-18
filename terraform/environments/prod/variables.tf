# terraform/environments/prod/variables.tf
variable "digitalocean_token" {
  description = "Token de API do DigitalOcean"
  type        = string
  sensitive   = true
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
