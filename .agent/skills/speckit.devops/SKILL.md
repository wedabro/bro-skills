---
name: speckit.devops
description: Docker Infrastructure & Security Hardening Specialist — Port ENV-first.
---

## 🎯 Mission
Set up and manage a standardized and secure Docker system for the project.
Ports MUST always be configured via ENV vars — NEVER hard-code.

## 📥 Input
- `.agent/memory/constitution.md` (port range, security rules)
- Existing `Dockerfile` , `docker-compose.yml` (if available)
- `.env.example`

## 📋 Protocol

### 1. Port Allocation (ENV-first) ⭐

**ALWAYS configure ports via ENV:**
- `.env` file (local) or server ENV (production)
- `docker-compose.yml` reads: `"${PUBLIC_PORT:-8920}:3000"`
- DO NOT hard-code port number in any file
- **CRITICAL**: If `.env` or system environment already has port variables defined (e.g. `PUBLIC_PORT`, `ADMIN_PORT`, `API_PORT` or equivalents), **ABSOLUTELY SKIP** port scanning/assignment and **NEVER** overwrite the existing port configuration.

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
# There are containers → SKIP port scan
# Empty/error → RUN port scan
```

- Pattern: Public FE `N` → Admin FE `N+1` → Backend API `N+2`

### 2. Local Docker (`docker-compose.yml`):
- Ports read from ENV: `"${PUBLIC_PORT:-8920}:3000"`
- Volume mounts cho hot-reload code
- Named volumes for `node_modules` (avoid host-container lock)
- Health checks for each service

### 3. Production Docker (`docker-compose.prod.yml`):
- Multi-stage builds (builder → runner)
- `USER node` or `USER appuser` (DO NOT run as root)
- Remove devDependencies in the final image
- Alpine/Slim base images
- Ports read from ENV (NO hard-code)

### 4. Security Checklist:
- `.dockerignore`: block `.env`, `.git`, `node_modules`
- No hard-code secrets in Dockerfile
- Only EXPOSE ports are needed

### 5. Documentation:
- Update `.agent/knowledge_base/infrastructure.md` with the results
- Update `.env.example` with all port vars

## 📤 Output
- Files: `Dockerfile`, `docker-compose.yml`, `docker-compose.prod.yml`, `.dockerignore`
- Config: `.env` (ports), `.env.example` (documented)
- Doc: `.agent/knowledge_base/infrastructure.md` (updated)

## 🚫 Guard Rails
- Flexibly configure ports via environment variables (.env) to avoid conflicts.
- DO NOT hard-code port numbers — ALWAYS use ENV vars.
- DO NOT run `docker compose down -v` on production.
- DO NOT hard-code credentials into the Dockerfile.
- DO NOT scan ports when Docker local is already running (with containers).

<!-- LESSON_LEARNED: Đã từng bị đơ khi gọi msvcrt.getch trên Git Bash và đã sửa fallback nhập số -->
