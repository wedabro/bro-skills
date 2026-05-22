---
description: Validate Implementation vs Spec
---

# ✅ Final Validation

## Pre-conditions
- Mọi tasks complete, tests pass, review approved

## Steps

// turbo-all

1. **Tasks Completion Check**:
   - Đọc `tasks.md` → mọi task phải `[X]`
   - Nếu còn `[ ]` hoặc `[/]` → ❌ BLOCKED

2. **TypeScript Build Gate** (CRITICAL):
   ```bash
   docker compose -f docker-compose.beta.yml build 2>&1 | tail -n 100
   ```
   Nếu build fail → ❌ BLOCKED, liệt kê errors

3. **Runtime Verification**:
   ```bash
   docker compose -f docker-compose.beta.yml up -d
   sleep 15
   docker compose -f docker-compose.beta.yml ps
   ```
   - Tất cả services phải `Up` (KHÔNG `Restarting`)
   - Nếu `Restarting` → chạy `docker compose logs <service>` → ❌ BLOCKED

4. **Health Check**:
   ```bash
   curl -s http://localhost:<web_port> | head -c 200  # Public Web
   curl -s http://localhost:<admin_port> | head -c 200  # Admin Panel
   curl -s http://localhost:<api_port>/health  # API
   ```
   Tất cả phải trả về 200

5. **Constitution Compliance**:
   - Verify Monorepo Rules (type contracts)
   - Verify Docker Rules (no volume shadowing in prod)
   - Verify Build-time Safety (try-catch trong SSG)

6. **Final Verdict**:
   ```
   🏁 VALIDATION REPORT
   ═══════════════════════
   Tasks:        N/N ✅
   TS Build:     PASS ✅
   Runtime:      PASS ✅ (all services Up)
   Health:       PASS ✅ (all 200)
   Constitution: PASS ✅
   ───────────────────────
   VERDICT: ✅ READY FOR DEPLOY
   ```

## Success Criteria
- ✅ Verdict: READY FOR DEPLOY
- ❌ Nếu BẤT KỲ step nào FAIL → BLOCKED (không được deploy)
