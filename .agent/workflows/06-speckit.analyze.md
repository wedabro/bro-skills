---
description: Phân tích tính nhất quán giữa artifacts
---

# 🔬 Consistency Analysis

## Pre-conditions
- spec.md, plan.md, tasks.md tồn tại

## Steps

1. **@speckit.analyze** — Cross-check 3 artifacts:
   - Mỗi User Scenario → có tasks?
   - Mỗi data model → có tasks?
   - Conflicts giữa plan và constitution?
2. Output: Gap Analysis table + Coverage Score

## Success Criteria
- ✅ Coverage Score ≥ 90%
- ✅ Không gaps CRITICAL
