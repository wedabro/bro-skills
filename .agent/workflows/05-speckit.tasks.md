---
description: Tạo Task Breakdown (tasks.md)
---

# 📋 Task Breakdown

## Pre-conditions
- `.agent/specs/[feature]/plan.md` tồn tại
- `.agent/specs/[feature]/spec.md` tồn tại

## Steps

1. **@speckit.tasks** — Breakdown plan → atomic tasks
2. Verify:
   - Mỗi task ≤15 phút
   - Mỗi task có file path
   - Dependency ordering đúng
   - Phase structure đúng (Setup → Foundation → Features → Polish)

## Success Criteria
- ✅ tasks.md có ≥1 phase
- ✅ Mỗi task format: `- [ ] T001 [P] [USx] Description affecting path/file`
- ✅ Không task nào ảnh hưởng >3 files
