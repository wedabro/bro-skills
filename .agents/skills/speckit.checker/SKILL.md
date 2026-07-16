---
name: speckit.checker
description: Static Analysis Aggregator - Run static analysis on the codebase.
---

## 🎯 Mission
Codebase scanning detects violations of coding standards, security issues, performance anti-patterns.
**MUST run actual commands** — not just scan by eye.

## 📥 Input
- Source code (all `src/` , `app/` , `pages/` )
- `.agent/memory/constitution.md` (coding standards)
- `Dockerfile`, `docker-compose*.yml`

## 📋 Protocol

### Phase 1: TypeScript Compile Check (CRITICAL)
This is the most important step, MUST run before every deploy:
```bash
# In Docker container or local:
docker compose exec <service> npx tsc --noEmit
# Or try building:
docker compose build 2>&1 | grep -i "error\|fail"
```
- Catch: type mismatch, missing props, wrong property names, import errors
- All TS errors are 🔴 CRITICAL

### Phase 2: Dockerfile & Docker Compose Lint
```bash
# Check for any COPY sources that exist
# Check out docker compose syntax:
docker compose -f docker-compose*.yml config --quiet
# Check volume shadowing (Using volumes for production is PROHIBITED):
grep -A 5 "volumes:" docker-compose.prod.yml # Must NOT have `. :/app`
```
- Volume mount `- .:/app` trong production → 🔴 CRITICAL
- COPY path does not exist → 🔴 CRITICAL
- Outer port not in env → 🟡 WARNING

### Phase 3: ENV Compliance
```bash
# Find hard-coded URLs/tokens:
grep -rn "http://localhost\|http://127.0.0.1\|https://" apps/*/src/ --include="*.ts" --include="*.tsx" | grep -v "node_modules\|.next\|schema.org"
# Find default text fallback:
grep -rn '|| "' apps/*/src/ --include="*.ts" --include="*.tsx" | grep -v "node_modules"
```

### Phase 4: Import Hygiene
- Find unused imports, circular dependencies
- Verify shared package exports match actual usage

### Phase 5: Build-time Safety (Next.js specific)
```bash
# Find SSG/SSR pages that call the API without try-catch:
grep -rn "await api\.\|await fetchApi" apps/*/src/app/sitemap.ts apps/*/src/app/*/page.tsx
# Each result must be in a try-catch block
```
- API call in `generateStaticParams` / `sitemap()` has no try-catch → 🔴 CRITICAL

### Phase 6: Security Scan
- Find `eval()` , `dangerouslySetInnerHTML` (need sanitize), SQL concatenation
- Find secrets/keys in source code

### Phase 7: Monorepo Integrity
- Verify shared package exports match imports
- Cross-reference types: every `entity.X` must exist in the interface

## 📤 Output
- File: `.agent/memory/checker-report.md`
- Format:
  ```
  ## 🔴 CRITICAL (N issues)
  - `apps/web/src/app/page.tsx:65` — Property 'category' does not exist on type 'Article'
  ## 🟡 WARNING (N issues)
  - `docker-compose.beta.yml:40` — Volume mount `.:/app` will override built code
  ## 🟢 INFO (N issues)
  - ...
  ```

## 🚫 Guard Rails
- Report ONLY — DO NOT edit the code yourself.
- Each finding must have a specific file path + line number.
- **MUST run `tsc --noEmit` or `docker compose build` ** — visual scanning is NOT ENOUGH.
- If there is 🔴 CRITICAL → FAIL conclusion, deployment is NOT allowed.
