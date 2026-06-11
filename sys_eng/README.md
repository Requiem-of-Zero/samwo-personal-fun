# Systems Engineering Homelab

## Goal

Build and manage a complete infrastructure stack from scratch using Linux, Docker, cloud services, monitoring, and Infrastructure as Code.

This project uses a real Ubuntu server administered remotely from an Arch Linux workstation to simulate common Systems Engineering, Infrastructure Engineering, and Platform Engineering workflows.

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

- [ ] Docker Images
- [ ] Docker Containers
- [ ] Container Lifecycle
- [ ] Running NGINX
- [ ] Port Mapping
- [ ] Docker Networking
- [ ] Accessing Services Across Network
- [ ] Container Logs
- [ ] Persistent Data Concepts

Reference:

```text
day-02-docker-nginx.md
```

---

## Day 3 - Docker Compose

- [ ] Docker Compose
- [ ] Multi-Container Applications
- [ ] Service Discovery
- [ ] Environment Variables
- [ ] Volumes
- [ ] Custom Networks
- [ ] Application Architecture

Reference:

```text
day-03-docker-compose.md
```

---

## Day 4 - Application Deployment

- [ ] Next.js Deployment
- [ ] Reverse Proxy Concepts
- [ ] Application Configuration
- [ ] Environment Management
- [ ] Containerized Workflows

Reference:

```text
day-04-nextjs-deployment.md
```

---

## Day 5 - Database Infrastructure

- [ ] PostgreSQL Container
- [ ] Persistent Storage
- [ ] Database Backups
- [ ] Database Networking
- [ ] Application Connectivity

Reference:

```text
day-05-postgresql.md
```

---

## Day 6 - Monitoring and Observability

- [ ] Grafana
- [ ] Prometheus
- [ ] Metrics Collection
- [ ] Dashboards
- [ ] Uptime Monitoring
- [ ] Alerting Concepts

Reference:

```text
day-06-monitoring.md
```

---

## Day 7 - Cloud Infrastructure

- [ ] Cloud VM
- [ ] Security Groups
- [ ] Cloud Networking
- [ ] SSH Access
- [ ] Public vs Private Networking

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
- [ ] Docker Images
- [ ] Docker Containers
- [ ] Docker Compose

## Applications

- [ ] NGINX
- [ ] Next.js
- [ ] PostgreSQL

## Monitoring

- [ ] Grafana
- [ ] Prometheus
- [ ] Uptime Monitoring

## Cloud

- [ ] Cloud VM
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
