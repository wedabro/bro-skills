---
name: speckit.migrate
description: Legacy Code Migrator - Reverse-engineer codebase hiá»‡n cÃ³ sang chuáº©n SDD.
role: Migration Specialist
---

## ðŸŽ¯ Mission
Scan legacy codebase â†’ táº¡o spec + plan sÆ¡ bá»™ â†’ Ä‘Ã¡nh giÃ¡ tech debt â†’ Ä‘á» xuáº¥t migration path.

## ðŸ“¥ Input
- Existing codebase (source code, configs, DB schema)
- `.agent/memory/constitution.md` (target standards)

## ðŸ“‹ Protocol
1. **Scan Phase**: DÃ¹ng ProjectScanner patterns Ä‘á»ƒ detect:
   - Languages, frameworks, dependencies
   - Data models (Prisma/SQL/Mongoose schemas)
   - API routes, pages, components
   - Docker setup (náº¿u cÃ³)
2. **Reverse-Engineer Spec**: Tá»« code â†’ táº¡o draft `spec.md`:
   - Má»—i page/route â†’ 1 User Scenario
   - Má»—i data model â†’ 1 entity description
3. **Tech Debt Inventory** (`migration-risk.md`):
   - ðŸ”´ Critical: Security holes, deprecated deps, no tests
   - ðŸŸ¡ Important: Missing Docker, no CI/CD, inconsistent patterns
   - ðŸŸ¢ Minor: Code style, naming conventions
4. **Migration Sequence**: Äá» xuáº¥t thá»© tá»± migrate (Ã­t risk trÆ°á»›c).

## ðŸ“¤ Output
- `.agent/specs/migration/spec.md` (draft)
- `.agent/specs/migration/migration-risk.md`

## ðŸš« Guard Rails
- KHÃ”NG refactor code trong bÆ°á»›c nÃ y â€” chá»‰ phÃ¢n tÃ­ch vÃ  táº¡o tÃ i liá»‡u.
- KHÃ”NG xÃ³a code cÅ©.

## When to Use
- Khi reverse-engineer codebase legacy sang chuáº©n SDD: táº¡o spec/plan sÆ¡ bá»™ + Ä‘Ã¡nh giÃ¡ tech debt.
- **KHÃ”NG dÃ¹ng cho**: map kiáº¿n trÃºc thuáº§n (â†’ `@speckit.map`), refactor/implement (â†’ `@speckit.implement`).

## Common Rationalizations
| LÃ½ do bao biá»‡n | Sá»± tháº­t |
|---|---|
| "Refactor luÃ´n cho gá»n" | Migrate chá»‰ phÃ¢n tÃ­ch + táº¡o tÃ i liá»‡u, khÃ´ng refactor á»Ÿ bÆ°á»›c nÃ y. |
| "XÃ³a code cÅ© cho sáº¡ch" | KhÃ´ng xÃ³a code cÅ©. Äá» xuáº¥t migration path thÃ´i. |
| "Migrate háº¿t má»™t láº§n" | Big-bang migration rá»§i ro cao. Sáº¯p thá»© tá»± Ã­t risk trÆ°á»›c. |

## Red Flags
- Refactor/sá»­a code trong bÆ°á»›c migrate.
- XÃ³a code legacy.
- Äá» xuáº¥t migrate big-bang thay vÃ¬ tuáº§n tá»±.

## Verification
- [ ] ÄÃ£ scan languages/frameworks/deps/data models/routes/docker.
- [ ] Draft spec.md táº¡o tá»« code (pageâ†’scenario, modelâ†’entity).
- [ ] `migration-risk.md` phÃ¢n loáº¡i tech debt Critical/Important/Minor.
- [ ] Migration sequence Ä‘á» xuáº¥t Ã­t risk trÆ°á»›c; khÃ´ng refactor/xÃ³a code cÅ©.
