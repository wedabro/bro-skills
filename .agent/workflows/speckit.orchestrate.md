
---
description: Multi-Agent Orchestration - Select and coordinate agents by project_type + attributes
---

# 🧭 Multi-Agent Orchestration

## Pre-conditions
- `.agent/project.json` exists (has `project_type` + `attributes` )
- `.agent/agents/registry.json` exists
- `.agent/memory/constitution.md` exists

## Steps

1. **@orchestrator** — Resolve agent set:
   - Read `project.json.project_type` + `attributes`
   - `active = core + base[type] + modifiers[architecture|platforms|flags]`
   - Log list of activated agents (duplicate types)

2. Run the pipeline with the selected agent:
   - Specify → Clarify → Plan → Tasks → Implement → Verify
   - Each task attaches the tag `@agent:<name>` to route

3. **Routing**: Orchestrator giao task cho domain agent theo tag.
   - For example project_type= `game` → task gameplay route to `@speckit.gamedev`
   - For example `platforms:[ios]` → task mobile route to `@speckit.ios`

4. **Conflict resolution**: Constitution > Orchestrator > Domain Agent.

## Success Criteria
- ✅ Correct set of agents activated according to project_type + attributes
- ✅ Each task has a clear owner agent
- ✅ Does not violate the Constitution
