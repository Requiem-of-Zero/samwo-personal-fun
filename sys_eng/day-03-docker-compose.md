# Day 3 - Docker Compose

## Objective

Learn how Docker Compose allows infrastructure to be defined declaratively rather than through manual Docker commands.

The goal was to transition from manually creating containers and networks to managing an entire application stack through a single configuration file.

---

# Why Docker Compose?

Before Docker Compose:

```bash
docker network create homelab-net

docker run ...

docker run ...

docker run ...
```

Infrastructure was created manually.

After Docker Compose:

```bash
docker compose up -d
```

The entire stack is defined in code.

This is the first step toward Infrastructure as Code.

---

# Multi-Container Applications

Created a stack containing:

```text
NGINX
Backend Service (httpbin)
```

Defined in:

```text
docker-compose.yml
```

Both services are started and managed together.

---

# Service Discovery

Configured NGINX to communicate with the backend using:

```nginx
proxy_pass http://backend:80;
```

instead of hardcoded IP addresses.

Verified Docker DNS functionality:

```bash
docker exec -it homelab-nginx sh
getent hosts backend
```

Result:

```text
172.x.x.x backend
```

Docker automatically resolves service names to container IP addresses.

---

# Environment Variables

Added runtime configuration:

```yaml
environment:
  - APP_ENV=homelab
  - SERVICE_NAME=backend
```

Verified:

```bash
docker compose exec backend env
```

Learned that containers can receive configuration without modifying the image itself.

Examples:

```text
Development
Staging
Production
```

can all use the same image with different environment variables.

---

# Custom Networks

Created separate networks:

```yaml
networks:
  frontend_net:
  backend_net:
```

Architecture:

```text
frontend_net
    |
    └── nginx

backend_net
    |
    ├── nginx
    └── backend
```

Learned that services can be attached to multiple networks.

NGINX acts as the bridge between public-facing traffic and private backend services.

---

# Application Architecture

Current architecture:

```text
Client
   |
   | Port 8080
   v
NGINX
   |
   | Docker DNS
   v
Backend
```

Responsibilities:

```text
NGINX
    - Public Entry Point
    - Reverse Proxy

Backend
    - Internal Service
    - No Published Ports
```

Only NGINX is exposed to clients.

The backend remains private.

---

# Infrastructure as Code

One of the biggest lessons from Day 3.

Instead of:

```bash
docker run ...
docker run ...
docker network create ...
```

infrastructure is now defined through:

```yaml
docker-compose.yml
```

The configuration becomes:

```text
Version Controlled
Repeatable
Portable
```

and can be stored in Git alongside application code.

---

# Key Takeaways

- Docker Compose defines infrastructure declaratively.
- Services can communicate through Docker DNS.
- Environment variables separate configuration from code.
- Networks control service communication.
- Infrastructure can be version controlled just like software.
- NGINX can expose public services while keeping backend services private.
- Docker Compose is a stepping stone toward Infrastructure as Code tools such as Terraform.

---

# Next Steps

- Deploy a real application with Next.js
- Connect an application to PostgreSQL
- Persist data using Docker volumes
- Introduce monitoring with Grafana and Prometheus
- Deploy services to cloud infrastructure
