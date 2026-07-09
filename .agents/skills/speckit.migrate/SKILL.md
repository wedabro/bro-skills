
---
name: speckit.migrate
description: Legacy Code Migrator - Reverse-engineer existing codebase to SDD standard.
role: Migration Specialist
---

## 🎯 Mission
Scan legacy codebase → create spec + preliminary plan → evaluate tech debt → propose migration path.

## 📥 Input
- Existing codebase (source code, configs, DB schema)
- `.agent/memory/constitution.md` (target standards)

## 📋 Protocol
1. **Scan Phase**: Use ProjectScanner patterns to detect:
   - Languages, frameworks, dependencies
   - Data models (Prisma/SQL/Mongoose schemas)
   - API routes, pages, components
   - Docker setup (if any)
2. **Reverse-Engineer Spec**: From code → create draft `spec.md` :
   - Each page/route → 1 User Scenario
   - Each data model → 1 entity description
3. **Tech Debt Inventory** (`migration-risk.md`):
   - 🔴 Critical: Security holes, deprecated deps, no tests
   - 🟡 Important: Missing Docker, no CI/CD, inconsistent patterns
   - 🟢 Minor: Code style, naming conventions
4. **Migration Sequence**: Suggested migration order (less risk first).

## 📤 Output
- `.agent/specs/migration/spec.md` (draft)
- `.agent/specs/migration/migration-risk.md`

## 🚫 Guard Rails
- DO NOT refactor code in this step — just analyze and document.
- DO NOT delete old code.
