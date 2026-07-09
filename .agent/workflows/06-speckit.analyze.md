
---
description: Analyze consistency between artifacts
---

# 🔬 Consistency Analysis

## Pre-conditions
- spec.md, plan.md, tasks.md exist

## Steps

1. **@speckit.analyze** — Cross-check 3 artifacts:
   - Each User Scenario → has tasks?
   - Each data model → has tasks?
   - Conflicts between plan and constitution?
2. Output: Gap Analysis table + Coverage Score

## Success Criteria
- ✅ Coverage Score ≥ 90%
- ✅ No CRITICAL gaps
