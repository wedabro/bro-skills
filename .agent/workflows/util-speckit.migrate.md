---
description: Migrate Legacy Code — Reverse-engineer codebase hiện có
---

# 🔄 Legacy Migration

## Pre-conditions
- Existing codebase với source code
- constitution.md đã setup (target standards)

## Steps
1. **@speckit.migrate** — Scan codebase:
   - Detect languages, frameworks, dependencies
   - Reverse-engineer data models, routes
   - Tạo draft spec.md
   - Assess tech debt → migration-risk.md
2. Review findings với developer
3. Tiếp tục với `/02-speckit.specify` để thêm features mới

## Success Criteria
- ✅ Draft spec.md tạo từ existing code
- ✅ migration-risk.md với tech debt inventory
