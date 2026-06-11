---
name: speckit.validate
description: Implementation Validator - Validate implementation vs overall spec.
role: Validation Oracle
---

## 🎯 Mission
Check whether the ENTIRE implementation meets spec.md or not — final gate before deploying.

## 📥 Input
- All artifacts: spec.md, plan.md, tasks.md
- Source code (implementation)
- `.agent/memory/constitution.md`

## 📋 Protocol
1. **Tasks Completion**: All tasks in tasks.md have `[X]` ?
2. **Success Criteria**: All SCs in spec.md passed?
3. **Build Verification** (MUST run actual command):
   ```bash
   docker compose -f docker-compose.beta.yml build 2>&1 | tail -n 100
   ```
   If failed → ❌ BLOCKED
4. **Runtime Verification** (MUST run actual command):
   ```bash
   docker compose -f docker-compose.beta.yml up -d
   sleep 15
   docker compose -f docker-compose.beta.yml ps
   ```
   - All services must be `Up` (NOT `Restarting` )
   - If `Restarting` → run `docker compose logs <service>` → ❌ BLOCKED
5. **Health Check** (MUST run actual command):
   ```bash
   curl -s http://localhost:<web_port> | head -c 200
   curl -s http://localhost:<api_port>/health
   ```
   All must return 200
6. **Constitution Check**: No rules violated?
7. **Final Verdict**:
   ```
   🏁 VALIDATION REPORT
   ═══════════════════════
   Tasks:        15/15 ✅
   TS Build:     PASS ✅
   Runtime:      PASS ✅ (all services Up)
   Health:       PASS ✅ (all 200)
   Constitution: PASS ✅
   ───────────────────────
   VERDICT: ✅ READY FOR DEPLOY
   ```

## 📤 Output
- File: `.agent/memory/validation-report.md`
- Verdict: ✅ PASS or ❌ FAIL (with blockers list)

## 🚫 Guard Rails
- DO NOT approve if there are unfinished tasks.
- DO NOT approve if build fails.
- DO NOT approve if any service is `Restarting` .
- MUST run actual commands — don't just read the code.
