---
name: speckit.validate
description: Implementation Validator - Validate implementation vs overall spec.
---

## 🎯 Mission
Check whether the ENTIRE implementation meets spec.md or not — final gate before deploying.

## 📥 Input
- All artifacts: spec.md, plan.md, tasks.md
- Source code (implementation)
- `.agents/memory/constitution.md`
- `.agents/project.json`, dependency manifests, and documented verification commands

## 📋 Protocol
1. **Tasks Completion**: All tasks in tasks.md have `[X]` ?
2. **Success Criteria**: All SCs in spec.md passed?
3. **Capability Discovery**:
   - Detect project type, language, package manager, containerization,
     configured services, build/test commands, and health checks.
   - Produce an applicability table. A non-applicable check is `N/A`, not PASS.
4. **Build Verification** (MUST run applicable commands):
   - Run the repository-defined build/type/lint commands.
   - Use the matching container service when the constitution requires Docker.
   - For non-Docker projects, use the documented project runtime.
   - Any applicable build failure → ❌ BLOCKED.
5. **Runtime Verification** (when the project has a runtime):
   - Start the documented runtime or discovered Compose configuration.
   - Wait using health/retry behavior with a bounded timeout; do not use a fixed
     sleep as proof of readiness.
   - Inspect failing service/application logs immediately.
6. **Health Check** (when configured):
   - Read health endpoints and ports from project configuration or environment.
   - Verify the expected status/body. Do not assume web/admin/API services.
7. **Tests and Success Criteria**:
   - Run the configured test suite and verify each spec success criterion with
     evidence. Missing required evidence → ❌ BLOCKED.
8. **Constitution Check**: No rules violated?
9. **Final Verdict**:
   ```
   🏁 VALIDATION REPORT
   ═══════════════════════
   Tasks:        15/15 ✅
   Build:        PASS ✅
   Runtime:      N/A (library project)
   Health:       N/A (no network service)
   Tests:        PASS ✅
   Constitution: PASS ✅
   ───────────────────────
   VERDICT: ✅ READY FOR DEPLOY
   ```

## 📤 Output
- File: `.agents/memory/validation-report.md`
- Verdict: ✅ PASS or ❌ FAIL (with blockers list)

## 🚫 Guard Rails
- DO NOT approve if there are unfinished tasks.
- DO NOT approve if an applicable build, test, runtime, or health check fails.
- MUST run actual commands — don't just read the code.
- DO NOT fail a project merely because a non-applicable Docker, TypeScript, or
  network-service check does not exist.
