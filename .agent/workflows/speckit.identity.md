
---
description: Create/update Master Identity for AI Agent
---

# 🆔 Identity Setup

## Pre-conditions
- `.agent/project.json` exists (run `bro-skills init` first)
- `.agent/memory/constitution.md` exists (recommended)

## Steps

1. **@speckit.identity** — Collect information:
   - Read `project.json` → project type, name
   - Read `constitution.md` → tech stack, principles
   - Scan codebase → existing patterns, conventions
2. Create/update `.agent/identity/master-identity.md` :
   - Persona + Core Capabilities
   - Soul (Core Beliefs): "bro-skills First", "Docker is the Law"
   - Project Context (auto-detected)
3. If `web_public` / `fullstack` → add SEO & GEO Awareness section

## Success Criteria
- ✅ `master-identity.md` exists
- ✅ Persona closely tied to the project domain (not generic)
- ✅ Core Beliefs includes mandatory items
