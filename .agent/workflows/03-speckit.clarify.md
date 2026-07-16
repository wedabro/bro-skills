---
description: Resolve ambiguity in Specification
---

# 🔍 Ambiguity Resolution

## Pre-conditions
- `.agent/specs/[feature]/spec.md` exists

## Steps

1. **@speckit.clarify** — Scan spec.md for ambiguity
2. Ask the developer up to 3 CRITICAL questions (table A/B/C options)
3. Auto-fix MINOR issues
4. Update spec.md with `[CLARIFIED]` markers

## Success Criteria
- ✅ No more vague language in spec.md
- ✅ All boundary conditions defined
