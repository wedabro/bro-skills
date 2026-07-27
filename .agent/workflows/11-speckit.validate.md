---
description: Validate Implementation vs Spec
---

# ✅ Final Validation

## Pre-conditions

- All tasks completed, tests passed, review approved

## Steps

1. **@speckit.validate** checks task completion and maps success criteria to
   concrete evidence.
2. Discover the project stack, configured commands, containerization, runtime,
   services, and health checks.
3. Run every applicable build, type, lint, and test command in the runtime
   required by the constitution.
4. Start and inspect the runtime only when the project defines one. Read
   service names, compose files, ports, and health endpoints from project
   configuration rather than assuming a topology.
5. Mark non-applicable checks `N/A` with a reason and block on any failed
   applicable check.
6. Verify constitutional compliance and write
   `.agent/memory/validation-report.md`.

## Success Criteria

- ✅ Verdict: READY FOR DEPLOY
- ❌ If any applicable step fails → BLOCKED (not deployed)
