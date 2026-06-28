# Day 07 - Cloud Infrastructure

## Objective

Understand how modern cloud infrastructure works by mapping cloud concepts to a real Ubuntu server running a Dockerized application stack.

Rather than immediately deploying to AWS, the Ubuntu homelab server was used to simulate common cloud infrastructure patterns including:

- Virtual Machines
- Firewalls / Security Groups
- Public vs Private Services
- Route Tables
- Subnets
- NAT
- Cloud Networking Concepts

---

# Cloud VM Fundamentals

A cloud virtual machine is fundamentally the same as a physical Linux server.

Ubuntu Homelab:

```text
Ubuntu Server
CPU
RAM
Storage
Network Interfaces
SSH Access
Docker
```

Cloud VM:

```text
Ubuntu VM
CPU
RAM
Storage
Network Interfaces
SSH Access
Docker
```

The primary difference is location:

```text
Homelab:
192.168.x.x

Cloud:
Public Internet IP
```

System information was gathered using:

```bash
hostnamectl
free -h
df -h
ip addr
```

Concepts learned:

- Hostname
- Memory utilization
- Storage utilization
- Network interfaces
- IP addressing

---

# SSH Access

SSH remains the primary administration method for cloud infrastructure.

Example:

```bash
ssh user@server
```

SSH is used for:

- Server administration
- Docker management
- Log analysis
- Application deployments
- Configuration changes
- Troubleshooting

Even in cloud environments, engineers spend most of their time connected through SSH rather than web dashboards.

---

# Public vs Private Networking

A major infrastructure principle is minimizing exposed services.

Initial stack:

```text
NGINX
Grafana
Prometheus
Node Exporter
Blackbox Exporter
```

were reachable from the LAN.

Docker Compose originally exposed:

```yaml
ports:
  - "3001:3000"
  - "9090:9090"
  - "9100:9100"
  - "9115:9115"
```

Result:

```text
Any device on the LAN
      ↓
Could access Grafana
Prometheus
Node Exporter
Blackbox
```

These ports were removed.

Current exposure:

```text
NGINX
SSH
```

Internal-only services:

```text
Next.js
PostgreSQL
Prometheus
Grafana
Node Exporter
Blackbox Exporter
```

Verification was performed using:

```bash
curl 192.168.1.58:8080
curl 192.168.1.58:3001
curl 192.168.1.58:9090
curl 192.168.1.58:9100
curl 192.168.1.58:9115
```

Only NGINX remained accessible.

---

# Understanding 127.0.0.1 vs 0.0.0.0

Localhost:

```text
127.0.0.1
```

Means:

```text
Only this machine can access the service.
```

Example:

```text
127.0.0.1:3001
```

All Interfaces:

```text
0.0.0.0
```

Means:

```text
Listen on every available network interface.
```

Example:

```text
0.0.0.0:8080
```

allows access from:

```text
localhost
LAN devices
Public Internet (if routed)
```

---

# Security Groups and Firewalls

Cloud providers use Security Groups.

Linux uses firewalls such as UFW.

Conceptual equivalence:

```text
AWS Security Group
=
Linux Firewall (UFW)
```

UFW was initially inactive:

```bash
sudo ufw status
```

Output:

```text
Status: inactive
```

Rules were configured:

```bash
sudo ufw allow 22/tcp
sudo ufw allow 8080/tcp
```

Firewall enabled:

```bash
sudo ufw enable
```

Result:

```text
Default: deny (incoming)
```

Allowed:

```text
22/tcp
8080/tcp
3389/tcp
```

Blocked:

```text
Everything else
```

Current security posture:

```text
Allow SSH
Allow NGINX
Deny all other inbound traffic
```

This mirrors production cloud firewall practices.

---

# Route Tables

Routing determines where traffic should be sent.

Current routing table:

```bash
ip route
```

Key entries:

```text
default via 192.168.1.1
```

Meaning:

```text
Unknown destinations
      ↓
Send to router
```

Local subnet:

```text
192.168.1.0/24
```

Meaning:

```text
Local devices communicate directly
without using the router.
```

Examples:

```text
Ubuntu -> Arch
```

Direct communication.

Example:

```text
Ubuntu -> Google
```

Traffic flow:

```text
Ubuntu
   ↓
Router
   ↓
Internet
```

---

# NAT

Network Address Translation (NAT) allows private devices to access the Internet.

Example:

```text
192.168.1.47
```

cannot exist on the public Internet.

Flow:

```text
Ubuntu
   ↓
Router NAT
   ↓
Public IP
   ↓
Internet
```

The router maintains a translation table allowing responses to return to the correct internal device.

---

# Docker Networks and Cloud Networking

Docker networks behave similarly to cloud subnets.

Example:

```text
172.20.0.0/16
172.21.0.0/16
```

These networks contain:

```text
NGINX
Next.js
PostgreSQL
Prometheus
Grafana
```

Docker acts as a miniature network environment with:

- Subnets
- DNS
- Routing
- Service discovery

---

# Cloud Networking Mapping

Home Network:

```text
Internet
    |
Router
    |
192.168.1.0/24
    |
Arch
Ubuntu
Phone
```

AWS:

```text
Internet
    |
Internet Gateway
    |
VPC
    |
Subnets
    |
EC2
RDS
Load Balancer
```

Equivalent concepts:

| Home Network   | AWS              |
| -------------- | ---------------- |
| Router         | Internet Gateway |
| LAN            | VPC              |
| Subnet         | Subnet           |
| Firewall       | Security Group   |
| Ubuntu Server  | EC2              |
| Docker Network | Private Subnet   |

---

# Public vs Private Subnets

Given:

```text
VPC
10.0.0.0/16

Public Subnet
10.0.1.0/24

Private Subnet
10.0.2.0/24
```

Recommended architecture:

```text
Public Subnet
 └─ NGINX

Private Subnet
 ├─ Next.js
 └─ PostgreSQL
```

Traffic flow:

```text
Internet
    ↓
NGINX
    ↓
Next.js
    ↓
PostgreSQL
```

Benefits:

- Database not Internet accessible
- Application protected from direct access
- Single public entry point
- Reduced attack surface

This is a standard production architecture pattern.

---

# Key Takeaways

- Cloud VMs are Linux servers running elsewhere.
- SSH is the primary administration mechanism.
- Services should be private by default.
- Only required services should be public.
- Firewalls and Security Groups provide layered security.
- Route tables determine packet paths.
- NAT enables private devices to access the Internet.
- Docker networking closely mirrors cloud networking.
- Production applications typically expose only a reverse proxy while keeping applications and databases private.

---

# Day 07 Completion

```text
[x] Cloud VM
[x] Security Groups
[x] Cloud Networking
[x] SSH Access
[x] Public vs Private Networking
```
