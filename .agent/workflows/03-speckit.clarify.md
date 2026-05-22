---
description: Giải quyết mơ hồ trong Specification
---

# 🔍 Ambiguity Resolution

## Pre-conditions
- `.agent/specs/[feature]/spec.md` tồn tại

## Steps

1. **@speckit.clarify** — Scan spec.md tìm ambiguity
2. Hỏi developer tối đa 3 câu CRITICAL (bảng A/B/C options)
3. Auto-fix MINOR issues
4. Update spec.md với `[CLARIFIED]` markers

## Success Criteria
- ✅ Không còn vague language trong spec.md
- ✅ Mọi boundary conditions defined
