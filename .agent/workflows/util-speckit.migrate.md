
---
description: Migrate Legacy Code — Reverse-engineer existing codebase
---

# 🔄 Legacy Migration

## Pre-conditions
- Existing codebase with source code
- constitution.md setup (target standards)

## Steps
1. **@speckit.migrate** — Scan codebase:
   - Detect languages, frameworks, dependencies
   - Reverse-engineer data models, routes
   - Create draft spec.md
   - Assess tech debt → migration-risk.md
2. Review findings with developers
3. Continue with `/02-speckit.specify` to add new features

## Success Criteria
- ✅ Draft spec.md created from existing code
- ✅ migration-risk.md with tech debt inventory
