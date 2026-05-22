---
description: Docker Infrastructure & Port Allocation (ENV-first)
---

# 🐳 DevOps Infrastructure Setup

## Pre-conditions
- `.agent/memory/constitution.md` tồn tại
- Docker Desktop (local) hoặc Docker Engine (server) đã cài đặt

## Steps

// turbo-all

### Step 1: Xác định Environment
- Detect environment: **local** / **staging** / **beta** / **production**
- Đọc `constitution.md` → port range (mặc định 8900-8999)

### Step 2: Port Allocation (ENV-first) ⭐

**Quy tắc Port — LUÔN cấu hình qua ENV:**
- Port PHẢI được khai báo trong `.env` (local) hoặc server ENV (prod)
- `docker-compose.yml` đọc port từ ENV vars (`${PUBLIC_PORT}`, `${ADMIN_PORT}`, `${API_PORT}`)
- KHÔNG hard-code port number trong bất kỳ file nào

**Quy tắc quét port theo môi trường:**

| Môi trường | Docker đã chạy? | Hành động |
|---|---|---|
| **Local** | ❌ Chưa (lần đầu) | Quét `netstat -ano \| findstr 89` → chọn 3 ports trống liên tiếp |
| **Local** | ✅ Đã chạy | **BỎ QUA** quét — dùng ports hiện tại từ `.env` / docker |
| **Staging/Beta/Prod** | Bất kỳ | **LUÔN** quét lần đầu để cấu hình → ghi vào `.env` |

**Check Docker đã chạy (Local):**
```bash
docker compose ps --format json 2>$null
# Nếu có containers → Docker đã chạy → SKIP port scan
# Nếu trống/error → Docker chưa chạy → RUN port scan
```

**Port scan khi cần:**
```bash
netstat -ano | findstr 89
```
- Pattern: Public FE `N` → Admin FE `N+1` → Backend API `N+2`
- Ghi luôn vào `.env`:
  ```env
  PUBLIC_PORT=8920
  ADMIN_PORT=8921
  API_PORT=8922
  ```

### Step 3: Docker Compose (Local)
- Tạo/cập nhật `docker-compose.yml`:
  - Ports đọc từ ENV: `"${PUBLIC_PORT:-8920}:3000"`
  - Volume mounts cho hot-reload
  - Named volumes cho `node_modules`
  - Health checks cho mỗi service

### Step 4: Docker Compose (Production/Staging/Beta)
- Tạo/cập nhật `docker-compose.prod.yml` / `docker-compose.beta.yml`:
  - Multi-stage builds (builder → runner)
  - `USER node` hoặc `USER appuser` (KHÔNG chạy root)
  - Loại bỏ devDependencies trong final image
  - Alpine/Slim base images
  - Ports đọc từ ENV (KHÔNG hard-code)

### Step 5: Security Checklist
- `.dockerignore`: block `.env`, `.git`, `node_modules`
- KHÔNG hard-code secrets trong Dockerfile
- Chỉ EXPOSE ports cần thiết

### Step 6: Documentation
- Cập nhật `.agent/knowledge_base/infrastructure.md`
- Cập nhật `.env.example` với tất cả port vars

## Success Criteria
- ✅ Ports cấu hình qua ENV (không hard-code)
- ✅ `docker-compose.yml` hoạt động local
- ✅ `docker-compose.prod.yml` tuân thủ security checklist
- ✅ `.dockerignore` tồn tại và đầy đủ
- ✅ `.env.example` document tất cả port vars
- ✅ `infrastructure.md` cập nhật

## 🚫 Guard Rails
- KHÔNG dùng port ngoài dải 8900-8999
- KHÔNG hard-code port number — LUÔN ENV vars
- KHÔNG chạy `docker compose down -v` trên production
- KHÔNG hard-code credentials vào Dockerfile
- KHÔNG quét port khi Docker local đã chạy
