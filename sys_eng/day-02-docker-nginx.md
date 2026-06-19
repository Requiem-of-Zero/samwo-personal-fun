# Day 2 - Docker, NGINX, Port Mapping, and Container Networking

## Objective

Learn how Docker containers communicate with the host, how services are exposed to a network, and how NGINX can act as a reverse proxy between clients and backend services.

---

# Docker Images vs Containers

Learned the distinction between:

```text
Image
    ↓
Blueprint / Template

Container
    ↓
Running Instance
```

Similar to:

```text
Class
    ↓
Object
```

An image can be used to create multiple containers.

---

# Container Lifecycle

Common commands:

```bash
docker run
docker stop
docker start
docker restart
docker rm
docker ps
docker ps -a
```

Learned that:

- Running containers appear in `docker ps`
- Stopped containers appear in `docker ps -a`
- Removing a container does not remove the image

---

# Running NGINX

Created an NGINX container:

```bash
docker run -d \
  --name nginx \
  -p 80:80 \
  nginx
```

Verified access from:

```text
http://192.168.1.47
```

---

# Port Mapping

Learned Docker port publishing syntax:

```bash
-p HOST_PORT:CONTAINER_PORT
```

Example:

```bash
-p 8080:80
```

means:

```text
Ubuntu Host Port 8080
         ↓
NGINX Container Port 80
```

Important observations:

- Browsers assume port 80 when no port is specified.
- Host ports must be unique.
- Container ports do not need to be unique.
- Multiple containers can listen on port 80 internally.

Example:

```text
8080 → nginx container port 80
8081 → another nginx container port 80
8082 → another nginx container port 80
```

---

# Docker Volumes

Created a custom HTML page:

```html
<h1>Samuel's Systems Engineering Homelab</h1>
```

Mounted the host directory into the container:

```bash
-v /home/sungjinwong/nginx-site:/usr/share/nginx/html:ro
```

Learned:

```text
Host Filesystem
        ↓
Docker Volume Mount
        ↓
Container Filesystem
```

The `:ro` option creates a read-only mount.

---

# Reverse Proxy Fundamentals

Created a backend service:

```bash
docker run -d \
  --name backend \
  kennethreitz/httpbin
```

Configured NGINX:

```nginx
location / {
    proxy_pass http://backend:80;
}
```

Architecture:

```text
Client
  ↓
NGINX
  ↓
Backend
```

Learned that clients communicate only with NGINX.

NGINX forwards requests to backend services.

---

# Docker Networks

Created a custom bridge network:

```bash
docker network create homelab-net
```

Connected:

```text
backend
nginx
```

to the same network.

Inspection:

```bash
docker network inspect homelab-net
```

Result:

```text
Gateway = 172.18.0.1
backend = 172.18.0.2
nginx   = 172.18.0.3
```

---

# Container DNS

One of the most important concepts learned today.

Inside the NGINX container:

```bash
getent hosts backend
```

returned:

```text
172.18.0.2 backend
```

Docker automatically provides DNS resolution between containers on the same network.

This allows services to communicate using names instead of IP addresses.

Example:

```nginx
proxy_pass http://backend:80;
```

instead of:

```nginx
proxy_pass http://172.18.0.2:80;
```

Benefits:

- Containers can be recreated without updating configuration.
- Docker automatically tracks service IP changes.
- Services communicate by logical names.

---

# Private vs Public Services

Public service:

```text
NGINX
```

Exposed through:

```bash
-p 8080:80
```

Private service:

```text
backend
```

No host port published.

Architecture:

```text
Client
  ↓
Host Port 8080
  ↓
NGINX
  ↓
Docker Network
  ↓
Backend
```

The backend is inaccessible directly from the LAN and can only be reached through NGINX.

---

# Key Takeaways

- Images are templates; containers are running instances.
- Port mapping controls how services are exposed.
- Docker networks create isolated virtual networks.
- Containers can communicate using service names through Docker DNS.
- Reverse proxies separate public-facing services from internal services.
- Most production architectures expose only the reverse proxy and keep backend services private.

---

# Next Session

- Docker Compose
- Multi-container deployments
- Service definitions
- Environment variables
- Persistent storage
- Infrastructure as code for containers
