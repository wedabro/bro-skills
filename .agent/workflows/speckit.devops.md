---
description: Docker Infrastructure & Port Allocation (ENV-first)
---

# 🐳 DevOps Infrastructure Setup

## Pre-conditions
- `.agent/memory/constitution.md` exists
- Docker Desktop (local) or Docker Engine (server) installed

## Steps

// turbo-all

### Step 1: Determine Environment
- Detect environment: **local** / **staging** / **beta** / **production**
- Read `constitution.md` → port configuration

### Step 2: Port Allocation (ENV-first) ⭐

**Port Rules — ALWAYS configure via ENV:**
- Port MUST be declared in `.env` (local) or server ENV (prod)
- `docker-compose.yml` reads port from ENV vars ( `${PUBLIC_PORT}` , `${ADMIN_PORT}` , `${API_PORT}` )
- DO NOT hard-code port number in any file
- **CRITICAL**: If `.env` or system environment already has port variables defined (e.g., `PUBLIC_PORT`, `ADMIN_PORT`, `API_PORT` or equivalents), **ABSOLUTELY SKIP** port scanning/assignment and **NEVER** overwrite the existing port configuration.

**Port scanning rules according to environment:**

| Environment | Existing Ports in .env? | Docker running? | Act |
|---|---|---|---|
| **Any** | ✅ Yes | Any | **SKIP** scan — use existing ports, **DO NOT** overwrite |
| **Local** | ❌ No | ❌ No (first time) | Scan available ports with socket/helper → select 3 consecutive empty ports |
| **Local** | ❌ No | ✅ Already running | **SKIP** scan — use current ports from docker/containers |
| **Staging/Beta/Prod** | ❌ No | Any | **ALWAYS** initial scan for configuration → write to `.env` |

**Check Docker is running (Local):**
```bash
docker compose ps --format json 2>$null
# If there are containers → Docker is already running → SKIP port scan
# If empty/error → Docker is not running → RUN port scan
```

**Port scan when needed:**
```text
Scan TCP bind availability on 127.0.0.1 for available ports.
```
- Pattern: Public FE `N` → Admin FE `N+1` → Backend API `N+2`
- Always write in `.env` :
  ```env
  PUBLIC_PORT=8920
  ADMIN_PORT=8921
  API_PORT=8922
  ```

### Step 3: Docker Compose (Local)
- Create/update `docker-compose.yml` :
  - Ports read from ENV: `"${PUBLIC_PORT:-8920}:3000"`
  - Volume mounts cho hot-reload
  - Named volumes cho `node_modules`
  - Health checks for each service

### Step 4: Docker Compose (Production/Staging/Beta)
- Create/update `docker-compose.prod.yml` / `docker-compose.beta.yml` :
  - Multi-stage builds (builder → runner)
  - `USER node` or `USER appuser` (DO NOT run as root)
  - Remove devDependencies in the final image
  - Alpine/Slim base images
  - Ports read from ENV (NO hard-code)

### Step 5: Security Checklist
- `.dockerignore`: block `.env`, `.git`, `node_modules`
- DO NOT hard-code secrets in Dockerfile
- Only EXPOSE ports are needed

### Step 6: Documentation
- Update `.agent/knowledge_base/infrastructure.md`
- Update `.env.example` with all port vars

## Success Criteria
- ✅ Ports configured via ENV (no hard-code)
- ✅ `docker-compose.yml` works locally
- ✅ `docker-compose.prod.yml` complies with security checklist
- ✅ `.dockerignore` exists and is complete
- ✅ `.env.example` document all port vars
- ✅ `infrastructure.md` updated

## 🚫 Guard Rails
- Flexibly configure ports via environment variables (.env) to avoid conflicts
- DO NOT hard-code port number — ALWAYS ENV vars
- DO NOT run `docker compose down -v` on production
- DO NOT hard-code credentials into the Dockerfile
- DO NOT scan ports when Docker local is already running
