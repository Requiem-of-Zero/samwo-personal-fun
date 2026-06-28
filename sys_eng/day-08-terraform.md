# Day 08 - Infrastructure as Code

## Objective

Learn the fundamentals of Infrastructure as Code using Terraform.

The goal of this lesson was to understand how infrastructure can be described, versioned, planned, created, destroyed, and recreated from code instead of being configured manually.

This lab used Terraform with the Docker provider so the concepts could be learned locally without needing AWS or another cloud provider.

---

# Infrastructure as Code

Infrastructure as Code means defining infrastructure using configuration files.

Instead of manually running:

```bash
docker network create terraform-app-net
```

Terraform allows the desired infrastructure to be written as code:

```hcl
resource "docker_network" "app_net" {
  name = var.network_name
}
```

Then Terraform creates the infrastructure with:

```bash
terraform apply
```

---

# Terraform Mental Model

Terraform follows this workflow:

```text
Write configuration
        ↓
Initialize providers
        ↓
Preview changes
        ↓
Apply changes
        ↓
Track state
        ↓
Destroy or update infrastructure
```

Common commands:

```bash
terraform init
terraform plan
terraform apply
terraform destroy
```

---

# Providers

A provider is a plugin that allows Terraform to talk to another system.

Examples:

```text
Docker Provider     → Docker API
AWS Provider        → AWS API
Cloudflare Provider → Cloudflare API
GitHub Provider     → GitHub API
```

This lab used the Docker provider:

```hcl
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}
```

---

# Resources

A resource is a piece of infrastructure managed by Terraform.

Examples:

```text
Docker Network
Docker Volume
Docker Container
AWS EC2 Instance
AWS Security Group
Cloudflare DNS Record
```

The first managed resource was a Docker network:

```hcl
resource "docker_network" "app_net" {
  name = var.network_name
}
```

Terraform resource name:

```text
docker_network.app_net
```

Actual Docker network name:

```text
terraform-app-net
```

---

# Terraform Plan

`terraform plan` previews what Terraform will do before making changes.

Example output:

```text
Plan: 1 to add, 0 to change, 0 to destroy.
```

This means Terraform compared:

```text
Desired configuration
Terraform state
Real Docker infrastructure
```

and determined that one resource needed to be created.

Important concept:

```text
terraform plan does not change infrastructure.
```

It only previews changes.

---

# Terraform Apply

`terraform apply` executes the planned infrastructure changes.

Terraform created the Docker network:

```text
terraform-app-net
```

Verification:

```bash
docker network ls | grep terraform
```

Example result:

```text
terraform-app-net    bridge    local
```

---

# Variables

Variables make Terraform reusable.

Instead of hardcoding:

```hcl
name = "terraform-app-net"
```

the network name was moved into a variable:

```hcl
variable "network_name" {
  description = "Docker network name"
  type        = string
  default     = "terraform-app-net"
}
```

Then used in the resource:

```hcl
resource "docker_network" "app_net" {
  name = var.network_name
}
```

This allows the same Terraform code to deploy different environments later.

Example future use:

```bash
terraform apply -var="network_name=restaurant-a-network"
terraform apply -var="network_name=restaurant-b-network"
```

---

# State Files

Terraform tracks managed infrastructure in:

```text
terraform.tfstate
```

State is Terraform's inventory database.

It records:

```text
What Terraform created
Resource IDs
Provider metadata
Mappings between code and real infrastructure
```

Example mapping:

```text
Terraform resource:
docker_network.app_net

Real Docker network:
terraform-app-net

Docker ID:
generated after apply
```

Terraform uses state to compare:

```text
Desired configuration
Stored state
Actual infrastructure
```

This allows Terraform to detect drift.

---

# Infrastructure Drift

Infrastructure drift happens when the real infrastructure no longer matches Terraform's expected state.

Example:

```bash
docker network rm terraform-app-net
```

If the network is manually deleted, Terraform can detect that the real Docker network is missing.

Next `terraform plan` would propose recreating it.

This is one of Terraform's major benefits:

```text
Terraform helps bring infrastructure back to the desired state.
```

---

# Destroy and Recreate Lifecycle

Terraform can remove infrastructure:

```bash
terraform destroy
```

Verification:

```bash
docker network ls | grep terraform
```

No result means the network was removed.

Terraform can then recreate it:

```bash
terraform apply
```

Verification:

```bash
docker network ls | grep terraform
```

The network appears again.

This proved the full infrastructure lifecycle:

```text
Create
Track
Destroy
Recreate
```

---

# Self-Hosting Use Case

Terraform does not require AWS.

For a self-hosted restaurant platform, Terraform can help standardize infrastructure across multiple physical or virtual servers.

Example future architecture:

```text
Restaurant Server
        ↓
Ubuntu
        ↓
Docker
        ↓
Terraform
        ↓
Networks
Volumes
Containers
Monitoring
Firewall rules
Backups
```

This supports a repeatable deployment model:

```text
Restaurant A
Restaurant B
Restaurant C
```

Each environment can be provisioned consistently from code.

---

# Terraform vs Docker Compose

Docker Compose is excellent for managing containers on one server.

Terraform becomes useful when infrastructure must be repeated, standardized, or managed across environments.

Docker Compose manages:

```text
Containers
Networks
Volumes
```

Terraform can manage:

```text
Docker resources
Cloud resources
DNS records
Firewall rules
Monitoring infrastructure
Multi-environment deployments
```

For this project:

```text
Docker Compose = application stack
Terraform = infrastructure template
```

---

# Key Takeaways

- Terraform turns infrastructure into code.
- Providers let Terraform talk to external systems.
- Resources are infrastructure objects Terraform manages.
- Variables make infrastructure reusable.
- State files let Terraform remember what it manages.
- Terraform can detect infrastructure drift.
- `terraform plan` previews changes.
- `terraform apply` creates or updates infrastructure.
- `terraform destroy` removes managed infrastructure.
- Terraform can be useful for self-hosted infrastructure, not only AWS.

---

# Completed Objectives

```text
[x] Terraform Fundamentals
[x] Providers
[x] Resources
[x] Variables
[x] State Files
[x] Infrastructure Deployment
```
