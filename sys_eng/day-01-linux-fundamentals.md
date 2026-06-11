# Day 1 - Linux Fundamentals, SSH Security, Networking, and Docker Foundations

## Objective

Learn the foundational Linux concepts required to administer a server remotely and prepare it for running infrastructure services.

Environment:

```text
Arch Linux Workstation
        |
        | SSH
        |
Ubuntu 24.04 Server (Zotac)
```

---

# Linux User and Group Management

Learned how Linux identifies users using:

```bash
whoami
id
```

Example:

```text
uid=1000(sungjinwong)
gid=1000(sungjinwong)
```

Key concepts:

- UID (User ID) uniquely identifies a user.
- GID (Group ID) identifies a user's primary group.
- Linux internally uses numeric identifiers rather than usernames.

---

## User Database

Examined:

```bash
cat /etc/passwd
```

Learned that user accounts are stored in the format:

```text
username:x:UID:GID:comment:home:shell
```

Example:

```text
sungjinwong:x:1000:1000:/home/sungjinwong:/bin/bash
```

Important observations:

- Password hashes are not stored in `/etc/passwd`.
- Password hashes are stored separately in `/etc/shadow`.
- Service accounts such as `sshd`, `www-data`, and `systemd-network` exist to run services with limited privileges.

---

## Group Database

Examined:

```bash
getent group
```

Learned that group entries follow:

```text
groupname:x:GID:members
```

Example:

```text
sudo:x:27:sungjinwong
```

This revealed which groups grant additional permissions to a user.

---

# Creating Users and Groups

Created a new engineering group:

```bash
sudo groupadd engineers
```

Created a test user:

```bash
sudo adduser developer
```

Learned that Linux automatically:

- Creates a UID
- Creates a matching primary group
- Creates a home directory
- Copies template files from `/etc/skel`

Added the user to the engineering group:

```bash
sudo usermod -aG engineers developer
```

Important lesson:

```text
-a = append
-G = supplementary groups
```

Without `-a`, existing group memberships may be overwritten.

---

# Authentication vs Authorization

One of the most important concepts learned today.

Authentication answers:

```text
Who are you?
```

Authorization answers:

```text
What are you allowed to do?
```

Example:

```bash
su - developer
```

Successfully logging in authenticated the user.

Attempting:

```bash
sudo usermod -aG engineers developer
```

failed because the user was not authorized to perform administrative actions.

---

# Linux Permissions

Examined permissions using:

```bash
ls -l
```

Example:

```text
drwxr-x---
```

Linux evaluates permissions in three categories:

```text
Owner
Group
Others
```

Permission values:

```text
r = 4
w = 2
x = 1
```

Examples:

```text
7 = rwx
6 = rw-
5 = r-x
0 = ---
```

---

## Shared Directory

Created a shared engineering directory:

```bash
sudo mkdir /shared
sudo chown root:engineers /shared
sudo chmod 770 /shared
```

Result:

```text
rwxrwx---
```

Learned that ownership and permissions determine access to resources.

---

# SSH Administration

Verified existing SSH key pair:

```text
~/.ssh/id_ed25519
~/.ssh/id_ed25519.pub
```

Installed the public key on the Ubuntu server:

```bash
ssh-copy-id
```

This added the key to:

```text
~/.ssh/authorized_keys
```

---

## SSH Authentication Flow

Learned how SSH public key authentication works:

```text
Private Key (Client)
        |
        | Cryptographic Proof
        v
Public Key (Server)
```

The private key never leaves the client machine.

The server verifies identity using the stored public key.

---

## SSH Hardening

Reviewed:

```text
PermitRootLogin
PasswordAuthentication
PubkeyAuthentication
```

Validated the effective SSH configuration using:

```bash
sudo sshd -T
```

Important lesson:

```text
Configuration File
    ≠
Running Configuration
```

Always verify the effective configuration being used by a service.

---

# Linux Networking

Examined network interfaces:

```bash
ip addr
```

Identified:

```text
lo      -> Loopback
enp2s0  -> Ethernet
wlp1s0  -> WiFi
```

---

## Routing

Examined routing tables:

```bash
ip route
```

Example:

```text
default via 192.168.1.1 dev enp2s0 metric 100
default via 192.168.1.1 dev wlp1s0 metric 600
```

Key concepts:

- Routing tables determine where traffic is sent.
- Lower metrics have higher priority.
- DHCP can automatically install routes.
- Ethernet was preferred over WiFi because it had a lower metric.

---

# Docker Foundations

Installed and configured Docker.

Initial attempt:

```bash
docker run hello-world
```

Failed with:

```text
permission denied while trying to connect to docker.sock
```

---

## Docker Security Model

Learned that Docker communicates through:

```text
/var/run/docker.sock
```

which is protected using standard Linux permissions.

Added the user to the Docker group:

```bash
sudo usermod -aG docker sungjinwong
```

Refreshed the login session and verified access:

```bash
docker run hello-world
```

---

# Major Takeaways

- Linux security is fundamentally based on users, groups, and permissions.
- Authentication and authorization are separate concepts.
- SSH public key authentication is more secure than password-based authentication.
- Group membership changes require a new login session to take effect.
- Effective service configuration should always be verified.
- Routing tables determine network behavior.
- Docker access is controlled using the same Linux permission model used throughout the operating system.

---

# Next Session

- Docker Images vs Containers
- Running NGINX in Docker
- Port Mapping
- Container Networking
- Exposing Services Across the Network
