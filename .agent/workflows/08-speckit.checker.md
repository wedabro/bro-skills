---
description: Run Static Analysis
---

# 🔍 Static Analysis

## Pre-conditions
- Implemented code (≥1 task completed)

## Steps

// turbo-all

1. **TypeScript Compile Check** (CRITICAL):
   ```bash
   docker compose build 2>&1 | grep -iE "error|fail|TS[0-9]"
   ```
   Or:
   ```bash
   docker compose exec topdeli-web npx tsc --noEmit
   docker compose exec topdeli-admin npx tsc --noEmit
   docker compose exec topdeli-api npx tsc --noEmit
   ```

2. **Dockerfile Integrity** — Check COPY paths:
   - Verify any COPY directories exist (especially `public/` )
   - Verify CMD entrypoint matches build output structure
   - Verify does NOT have volume mount `.:/app` in production/beta compose

3. **ENV Compliance** — Scan hard-coded values:
   ```bash
   grep -rn "http://localhost\|http://127.0.0.1" apps/*/src/ --include="*.ts" --include="*.tsx" | grep -v "node_modules"
   grep -rn '|| "' apps/*/src/ --include="*.ts" --include="*.tsx" | grep -v "node_modules"
   ```

4. **Build-time Safety** — Verify SSG pages:
   ```bash
   grep -rn "await api\.\|await fetchApi" apps/*/src/app/sitemap.ts apps/*/src/app/*/page.tsx
   ```
   Each result MUST be in a try-catch block.

5. **Monorepo Type Contract** — @speckit.checker:
   - Cross-reference shared type exports vs component usage
   - Verify shared package exports match actual file structure

6. **Security Scan**:
   - Find `eval()` , `dangerouslySetInnerHTML` , exposed secrets
   - Docker compliance: ports configured in environment variables

7. **Output Report** → `.agent/memory/checker-report.md`

## Success Criteria
- ✅ TypeScript compile: 0 errors
- ✅ Docker build: complete success
- ✅ 0 issues CRITICAL (🔴)
- ✅ Report file existence
- ❌ If there are any 🔴 CRITICAL → BLOCK deploy
