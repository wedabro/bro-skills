---
description: Create Task Breakdown (tasks.md)
---

# 📋 Task Breakdown

## Pre-conditions
- `.agent/specs/[feature]/plan.md` exists
- `.agent/specs/[feature]/spec.md` exists

## Steps

1. **@speckit.tasks** — Breakdown plan → atomic tasks
2. Verify:
   - Each task ≤15 minutes
   - Each task has a file path
   - Dependency ordering is correct
   - Phase structure is correct (Setup → Foundation → Features → Polish)

## Success Criteria
- ✅ tasks.md has ≥1 phases
- ✅ Each task format: `- [ ] T001 [P] [USx] Description affecting path/file`
- ✅ No task affects >3 files
