# Systems Engineering Homelab

# Goal

Build, deploy, and operate a complete web application infrastructure stack from scratch using Linux, Docker, networking, monitoring, cloud services, and Infrastructure as Code.

This project uses a real Ubuntu server administered remotely from an Arch Linux workstation to simulate common Systems Engineering, Infrastructure Engineering, Platform Engineering, and DevOps workflows.

The objective is not only to deploy applications, but to understand how modern services are packaged, networked, secured, monitored, and maintained in production environments.

By the end of the project, the environment will include:

- Linux server administration
- SSH and remote management
- Docker containerization
- NGINX reverse proxying
- Multi-container applications with Docker Compose
- Next.js application hosting
- PostgreSQL database infrastructure
- Monitoring and observability with Grafana and Prometheus
- Cloud infrastructure deployment
- Infrastructure as Code with Terraform

The final result will be a production-style service stack that demonstrates the full lifecycle of deploying, operating, monitoring, and maintaining modern web services.

---

# Environment

## Workstation

- Arch Linux
- Hyprland
- SSH Client

## Server

- Ubuntu 24.04 LTS
- Zotac ZBOX
- Docker

---

# Architecture Evolution

## Current

```text
Arch Desktop
     |
     | SSH
     |
Ubuntu Server
```

## Target

```text
Arch Desktop
     |
     | SSH
     |
Ubuntu Server
     |
Docker Compose
├── NGINX
├── Next.js
├── PostgreSQL
└── Grafana
     |
Cloud Infrastructure
     |
Terraform
```

---

# Learning Roadmap

## Day 1 - Linux Fundamentals and SSH

- [x] User Identification (UID/GID)
- [x] User Management
- [x] Group Management
- [x] Authentication vs Authorization
- [x] File Ownership
- [x] Linux Permissions
- [x] Shared Directories
- [x] SSH Keys
- [x] SSH Authentication Flow
- [x] SSH Hardening
- [x] Network Interfaces
- [x] Routing Tables
- [x] Docker Installation
- [x] Docker Permissions

Reference:

```text
day-01-linux-fundamentals.md
```

---

## Day 2 - Docker and NGINX

- [x] Docker Images
- [x] Docker Containers
- [x] Container Lifecycle
- [x] Running NGINX
- [x] Port Mapping
- [x] Docker Networking
- [x] Accessing Services Across Network
- [x] Container Logs
- [x] Persistent Data Concepts
- [x] Docker Volumes
- [x] Reverse Proxy Fundamentals
- [x] Container DNS
- [x] Public vs Private Services

Reference:

```text
day-02-docker-nginx.md
```

---

## Day 3 - Docker Compose

- [x] Docker Compose
- [x] Multi-Container Applications
- [x] Service Discovery
- [x] Environment Variables
- [x] Volumes
- [x] Custom Networks
- [x] Application Architecture

Reference:

```text
day-03-docker-compose.md
```

---

## Day 4 - Application Deployment

- [x] Next.js Deployment
- [x] Reverse Proxy Concepts
- [x] Application Configuration
- [x] Environment Management
- [x] Containerized Workflows

Reference:

```text
day-04-nextjs-deployment.md
```

---

## Day 5 - Database Infrastructure

- [x] PostgreSQL Container
- [x] Persistent Storage
- [x] Database Backups
- [x] Database Networking
- [x] Application Connectivity

Reference:

```text
day-05-postgresql.md
```

---

## Day 6 - Monitoring and Observability

- [x] Grafana
- [x] Prometheus
- [x] Metrics Collection
- [x] Dashboards
- [x] Uptime Monitoring
- [x] Alerting Concepts

Reference:

```text
day-06-monitoring.md
```

---

## Day 7 - Cloud Infrastructure

- [x] Cloud VM
- [x] Security Groups
- [x] Cloud Networking
- [x] SSH Access
- [x] Public vs Private Networking

Reference:

```text
day-07-cloud-vm.md
```

---

## Day 8 - Infrastructure as Code

- [ ] Terraform Fundamentals
- [ ] Providers
- [ ] Resources
- [ ] Variables
- [ ] State Files
- [ ] Infrastructure Deployment

Reference:

```text
day-08-terraform.md
```

---

# Progress

## Linux

- [x] Linux Fundamentals
- [x] User and Group Management
- [x] File Permissions
- [x] SSH Administration
- [x] Networking Fundamentals

## Containers

- [x] Docker Installation
- [x] Docker Images
- [x] Docker Containers
- [x] Container Lifecycle
- [x] Port Mapping
- [x] Docker Volumes
- [x] Docker Networking
- [x] Container DNS
- [x] Docker Compose

## Applications

- [x] NGINX
- [x] Next.js
- [x] PostgreSQL

## Monitoring

- [x] Grafana
- [x] Prometheus
- [x] Uptime Monitoring

## Cloud

- [x] Cloud VM
- [ ] Cloud Networking
- [ ] Security Groups

## Infrastructure as Code

- [ ] Terraform
- [ ] Automated Infrastructure Deployment

---

# Long-Term Goal

Deploy and manage a production-style environment consisting of:

- Linux Server Administration
- Docker Containers
- NGINX Reverse Proxy
- Next.js Application
- PostgreSQL Database
- Monitoring Stack
- Cloud Infrastructure
- Terraform Automation

while documenting the entire journey from foundational Linux administration to modern infrastructure management.
