---
description: Establish/update Constitution (Source of Law)
---

# 📜 Constitution Setup

## Pre-conditions
- `.agent/` directory already exists (run `bro-skills init` first)

## Steps

1. **@speckit.constitution** — Collect information from developers:
   - Tech stack (language, framework, DB)
   - Docker port configuration
   - Coding principles (VD: No hardcode, Docker-first)
   - Security requirements
2. Create/update `.agent/memory/constitution.md`
3. Validate: Each section has ≥1 specific rule

## Success Criteria
- ✅ `constitution.md` exists with ≥4 sections
- ✅ Each rule is testable (not generic)
