---
description: Tạo Technical Plan (plan.md)
---

# 🏗️ Technical Planning

## Pre-conditions
- `.agent/specs/[feature]/spec.md` tồn tại (đã clarified)
- `.agent/memory/constitution.md` tồn tại

## Steps

1. **@speckit.plan** — Chuyển spec (WHAT) → plan (HOW):
   - Phase 0: Research unknowns → research.md
   - Phase 1: Data model → data-model.md
   - Phase 2: API contracts → contracts/*.md
   - Phase 3: Architecture → plan.md
   - Phase 4: **Must-Haves (Goal-Backward)** → Xác định truths, artifacts, key links.
2. **GATE**: So sánh plan vs constitution
   - Vi phạm? → BÁO LỐI, yêu cầu fix

## Success Criteria
- ✅ plan.md có folder structure + component hierarchy
- ✅ data-model.md có entity definitions
- ✅ Không vi phạm constitution
