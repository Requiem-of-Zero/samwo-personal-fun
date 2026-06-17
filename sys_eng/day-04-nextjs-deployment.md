# Day 4 - Next.js Deployment and Application Architecture

## Objective

Deploy a production-style Next.js application behind an NGINX reverse proxy using Docker Compose while learning application configuration, environment management, and containerized workflows.

---

## Architecture

```text
Browser
   ↓
NGINX Reverse Proxy
   ↓
Next.js Application
```

NGINX serves as the public entry point while the Next.js application remains accessible only through the internal Docker network.

---

## Topics Covered

### Next.js Deployment

Built and deployed a production Next.js application using Docker.

Workflow:

```text
Source Code
    ↓
Docker Build
    ↓
Docker Image
    ↓
Container
```

Learned that containers are created from immutable images built from source code.

---

### Reverse Proxy Concepts

Configured NGINX as a reverse proxy.

```nginx
proxy_pass http://pos-app:3000;
```

Request flow:

```text
Client
   ↓
NGINX
   ↓
Next.js
```

Benefits:

- Single public entry point
- Hide application containers
- Route traffic to multiple services
- Future support for SSL/TLS termination
- Load balancing capabilities

---

### Docker Networking and Service Discovery

Created multiple Docker networks:

```yaml
frontend-net
app-net
```

Learned that Docker automatically provides DNS between services.

Example:

```text
Service Name: pos-app
DNS Hostname: pos-app
```

NGINX can reach the application using:

```text
http://pos-app:3000
```

without manually configuring IP addresses.

---

### Troubleshooting Reverse Proxy Failures

Encountered:

```text
502 Bad Gateway
```

Learned that:

```text
Client -> NGINX = Working
NGINX -> Application = Failing
```

A 502 error often indicates that the reverse proxy is operational but the backend service is unavailable or not yet ready.

---

### Application Configuration

Configured application deployment using:

```yaml
ports:
volumes:
depends_on:
networks:
environment:
```

Learned how Compose defines the relationships between services and infrastructure components.

---

### Environment Management

Created environment configuration files:

```env
NODE_ENV=production
PORT=3000
NEXT_PUBLIC_APP_NAME=Restaurant POS Homelab
NEXT_PUBLIC_DEPLOYMENT_ENV=docker-compose
```

---

### Build-Time vs Runtime Variables

One of the most important lessons learned.

Build Time:

```text
Docker Build
    ↓
yarn build
    ↓
Next.js Production Bundle
```

Runtime:

```text
Docker Container Starts
    ↓
Environment Variables Injected
```

Discovered that:

```text
NEXT_PUBLIC_* variables
```

must be available during the build process because they are embedded into the browser JavaScript bundle.

Runtime environment variables alone are insufficient for client-side Next.js variables.

---

### Docker Build Arguments

Implemented:

```dockerfile
ARG NEXT_PUBLIC_APP_NAME
ARG NEXT_PUBLIC_DEPLOYMENT_ENV

ENV NEXT_PUBLIC_APP_NAME=$NEXT_PUBLIC_APP_NAME
ENV NEXT_PUBLIC_DEPLOYMENT_ENV=$NEXT_PUBLIC_DEPLOYMENT_ENV
```

and supplied values through Docker Compose build arguments.

This allowed Next.js to correctly embed deployment configuration during the build process.

---

### Containerized Workflows

Frequently used commands:

```bash
docker compose up -d
docker compose down
docker compose build
docker compose ps
docker compose logs
docker compose exec
docker exec
```

Learned how to inspect running containers, troubleshoot services, rebuild images, and verify application health.

---

## Key Lessons

- Reverse proxies sit between clients and backend services.
- Docker service names become DNS hostnames.
- Internal services do not need exposed ports.
- 502 errors usually indicate backend communication problems.
- Build-time and runtime variables serve different purposes.
- Next.js client variables must be available during the build process.
- Docker Compose defines complete application architecture.
- Container troubleshooting is a core systems engineering skill.

---

## Outcome

Successfully deployed a production-style containerized application stack:

```text
Browser
   ↓
NGINX
   ↓
Next.js
```

This deployment established the foundation for Day 5, where PostgreSQL will be integrated into the application architecture to create a complete multi-tier system.
