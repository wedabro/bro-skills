---
name: speckit.devops
description: Chuyên gia hạ tầng Docker & Security Hardening — Port ENV-first, dải 8900-8999.
role: DevOps Architect
---

## 🎯 Mission
Thiết lập và quản lý hệ thống Docker chuẩn hóa, bảo mật cho dự án.
Port PHẢI luôn cấu hình qua ENV vars — KHÔNG BAO GIỜ hard-code.

## 📥 Input
- `.agent/memory/constitution.md` (port range, security rules)
- Existing `Dockerfile`, `docker-compose.yml` (nếu có)
- `.env.example`

## 📋 Protocol

### 1. Port Allocation (ENV-first) ⭐

**LUÔN cấu hình port qua ENV:**
- `.env` file (local) hoặc server ENV (production)
- `docker-compose.yml` đọc: `"${PUBLIC_PORT:-8920}:3000"`
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
# Có containers → SKIP port scan
# Trống/error → RUN port scan
```

- Pattern: Public FE `N` → Admin FE `N+1` → Backend API `N+2`

### 2. Local Docker (`docker-compose.yml`):
- Ports đọc từ ENV: `"${PUBLIC_PORT:-8920}:3000"`
- Volume mounts cho hot-reload code
- Named volumes cho `node_modules` (tránh host-container lock)
- Health checks cho mỗi service

### 3. Production Docker (`docker-compose.prod.yml`):
- Multi-stage builds (builder → runner)
- `USER node` hoặc `USER appuser` (KHÔNG chạy root)
- Loại bỏ devDependencies trong image final
- Alpine/Slim base images
- Ports đọc từ ENV (KHÔNG hard-code)

### 4. Security Checklist:
- `.dockerignore`: block `.env`, `.git`, `node_modules`
- Không hard-code secrets trong Dockerfile
- Chỉ EXPOSE ports cần thiết

### 5. Documentation:
- Cập nhật `.agent/knowledge_base/infrastructure.md` với kết quả
- Cập nhật `.env.example` với tất cả port vars

## 📤 Output
- Files: `Dockerfile`, `docker-compose.yml`, `docker-compose.prod.yml`, `.dockerignore`
- Config: `.env` (ports), `.env.example` (documented)
- Doc: `.agent/knowledge_base/infrastructure.md` (updated)

## 🚫 Guard Rails
- KHÔNG dùng port ngoài dải 8900-8999.
- KHÔNG hard-code port number — LUÔN dùng ENV vars.
- KHÔNG chạy `docker compose down -v` trên production.
- KHÔNG hard-code credentials vào Dockerfile.
- KHÔNG quét port khi Docker local đã chạy (có containers).
