# Day 5 - PostgreSQL Database Infrastructure

## Objective

Add PostgreSQL to the Docker Compose application stack and understand how database containers, persistent storage, networking, application connectivity, and backups work in a production-style environment.

---

## Architecture

```text
Browser
   ↓
NGINX
   ↓
Next.js API Routes
   ↓
PostgreSQL
```

PostgreSQL is not exposed directly to the host or public network. It is only reachable by containers connected to the internal Docker application network.

---

## Docker Compose PostgreSQL Service

```yaml
postgres:
  # Official PostgreSQL image
  image: postgres:17

  # Initialize database credentials on first startup
  environment:
    POSTGRES_USER: pos_user
    POSTGRES_PASSWORD: pos_password
    POSTGRES_DB: pos_db

  # Persist database files outside the container
  volumes:
    - postgres-data:/var/lib/postgresql/data

  # Internal-only database network
  networks:
    - app-net
```

Named volume:

```yaml
volumes:
  postgres-data:
```

---

## PostgreSQL Container

The database runs as its own container:

```bash
docker compose ps
```

The application can reach PostgreSQL using the Docker Compose service name:

```text
postgres:5432
```

This works because Docker provides internal DNS between services on the same network.

---

## Persistent Storage

PostgreSQL writes data inside the container at:

```text
/var/lib/postgresql/data
```

Docker maps that path to a named volume on the Ubuntu host:

```text
/var/lib/docker/volumes/docker-nextjs-pos_postgres-data/_data
```

This means:

```text
Container path:
  /var/lib/postgresql/data

Host storage:
  /var/lib/docker/volumes/docker-nextjs-pos_postgres-data/_data
```

The container can be removed and recreated while the data remains stored in the Docker volume.

---

## Container vs Data

Important lesson:

```text
Containers are temporary.
Data must persist separately.
```

`docker compose down` removes containers and networks, but keeps named volumes.

```bash
docker compose down
docker compose up -d
```

The database data remains.

Dangerous command:

```bash
docker compose down -v
```

The `-v` flag removes volumes too, which can delete the database files.

---

## Application Connectivity

The Next.js app connects to PostgreSQL using:

```env
DATABASE_URL=postgresql://pos_user:pos_password@postgres:5432/pos_db
```

Meaning:

```text
pos_user       = database user
pos_password   = database password
postgres       = Docker Compose service hostname
5432           = PostgreSQL port
pos_db         = database name
```

The app connects through the internal Docker network, not through a public database port.

---

## Database Client

Installed PostgreSQL client library:

```bash
yarn add pg
yarn add -D @types/pg
```

Created a shared database connection pool:

```ts
import { Pool } from "pg";

export const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});
```

---

## API Route

Created an API route that reads products from the database:

```ts
const result = await pool.query("SELECT * FROM products ORDER BY id ASC");
```

Verified through NGINX:

```bash
curl localhost:8080/api/products
```

Example response:

```json
[
  {
    "id": 1,
    "name": "Beef Noodle Soup",
    "price": "13.99"
  }
]
```

This confirmed:

```text
Browser/Client
   ↓
NGINX
   ↓
Next.js API
   ↓
PostgreSQL
```

---

## Database Table

Created a `products` table:

```sql
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  price NUMERIC(10,2) NOT NULL
);
```

Inserted seed data:

```sql
INSERT INTO products (name, price)
VALUES
  ('Beef Noodle Soup', 13.99),
  ('Chicken Rice Plate', 11.99),
  ('Pork Dumplings', 8.99),
  ('Milk Tea', 4.99);
```

---

## Database Backups

Persistent volumes are not the same as backups.

A volume protects data when containers are recreated.

A backup protects data if the volume is deleted, corrupted, or lost.

Created a backup directory:

```bash
mkdir -p backups
```

Created a SQL backup with `pg_dump`:

```bash
docker compose exec -T postgres \
  pg_dump -U pos_user pos_db \
  > backups/pos_db.sql
```

Explanation:

```text
pg_dump         = export database contents
-U pos_user     = connect as the database user
pos_db          = database being backed up
> pos_db.sql    = write output to a local SQL file
```

The `>` operator writes or overwrites the backup file.
The `>>` operator would append instead.

Verified backup file:

```bash
ls -lh backups/
head -20 backups/pos_db.sql
```

---

## Restore Testing

A backup is only useful if it can be restored.

Simulated data loss:

```sql
DROP TABLE products;
```

Restored from backup:

```bash
docker compose exec -T postgres \
  psql -U pos_user -d pos_db \
  < backups/pos_db.sql
```

Explanation:

```text
psql              = PostgreSQL command-line client
-U pos_user        = database user
-d pos_db          = database to restore into
< pos_db.sql       = feed backup file into psql
```

Verified restore:

```bash
curl localhost:8080/api/products
```

The product data returned again, proving the backup and restore process works.

---

## Security Notes

Docker access is powerful.

Anyone who can run:

```bash
docker compose exec postgres psql -U pos_user -d pos_db
```

can access the database container.

Users in the Docker group should be treated as highly privileged users.

The database is not exposed with:

```yaml
ports:
  - "5432:5432"
```

This keeps PostgreSQL private inside the Docker network.

---

## Key Lessons

- PostgreSQL can run as a containerized database service.
- Docker Compose service names become internal DNS hostnames.
- Databases should usually stay on private networks.
- Applications connect to databases using connection strings.
- Containers are ephemeral, but volumes persist.
- Docker volumes store database files on the host.
- Persistent storage is not the same thing as backups.
- `pg_dump` creates a logical database backup.
- Restore testing is required to prove a backup works.
- Docker group access should be treated as highly privileged.

---

## Day 5 Checklist

- [x] PostgreSQL Container
- [x] Persistent Storage
- [x] Database Networking
- [x] Application Connectivity
- [x] Database Backups
- [x] Restore Testing

---

## Outcome

Completed a working three-tier application stack:

```text
NGINX
   ↓
Next.js
   ↓
PostgreSQL
```

The application now serves real database-backed data through API routes, stores data persistently in a Docker volume, and has a verified backup and restore workflow.

This creates the foundation for Day 6 monitoring and observability with Grafana and Prometheus.
