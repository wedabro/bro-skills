---
description: Chạy Static Analysis
---

# 🔍 Static Analysis

## Pre-conditions
- Code đã implement (≥1 task complete)

## Steps

// turbo-all

1. **TypeScript Compile Check** (CRITICAL):
   ```bash
   docker compose build 2>&1 | grep -iE "error|fail|TS[0-9]"
   ```
   Hoặc:
   ```bash
   docker compose exec topdeli-web npx tsc --noEmit
   docker compose exec topdeli-admin npx tsc --noEmit
   docker compose exec topdeli-api npx tsc --noEmit
   ```

2. **Dockerfile Integrity** — Kiểm tra COPY paths:
   - Verify mọi thư mục được COPY tồn tại (đặc biệt `public/`)
   - Verify CMD entrypoint khớp với build output structure
   - Verify KHÔNG có volume mount `.:/app` trong production/beta compose

3. **ENV Compliance** — Scan hard-coded values:
   ```bash
   grep -rn "http://localhost\|http://127.0.0.1" apps/*/src/ --include="*.ts" --include="*.tsx" | grep -v "node_modules"
   grep -rn '|| "' apps/*/src/ --include="*.ts" --include="*.tsx" | grep -v "node_modules"
   ```

4. **Build-time Safety** — Verify SSG pages:
   ```bash
   grep -rn "await api\.\|await fetchApi" apps/*/src/app/sitemap.ts apps/*/src/app/*/page.tsx
   ```
   Mỗi kết quả PHẢI nằm trong try-catch block.

5. **Monorepo Type Contract** — @speckit.checker:
   - Cross-reference shared type exports vs component usage
   - Verify shared package exports match actual file structure

6. **Security Scan**:
   - Tìm `eval()`, `dangerouslySetInnerHTML`, exposed secrets
   - Docker compliance: ports trong range 8900-8999

7. **Output Report** → `.agent/memory/checker-report.md`

## Success Criteria
- ✅ TypeScript compile: 0 errors
- ✅ Docker build: thành công hoàn toàn
- ✅ 0 issues CRITICAL (🔴)
- ✅ Report file tồn tại
- ❌ Nếu có bất kỳ 🔴 CRITICAL → BLOCK deploy
