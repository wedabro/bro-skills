---
description: Run Static Analysis
---

# 🔍 Static Analysis

## Pre-conditions
- Implemented code (≥1 task completed)

## Steps

1. **@speckit.checker** discovers the project language, package manager,
   configured scripts, containerization, services, and framework.
2. Build an applicability table for compile/type, lint, container,
   configuration/security, and stack-specific integrity checks.
3. Run every applicable repository-defined command in the runtime required by
   the constitution. Mark unavailable checks `N/A` with a reason.
4. Report every finding with a specific file and line while redacting secrets.
5. Write `.agent/memory/checker-report.md`.

## Success Criteria
- ✅ Every applicable compile/type/lint check passes
- ✅ Container checks pass, or are explicitly `N/A` for a non-container project
- ✅ 0 issues CRITICAL (🔴)
- ✅ Report file existence
- ❌ If there are any 🔴 CRITICAL → BLOCK deploy
