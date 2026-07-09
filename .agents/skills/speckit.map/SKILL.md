
---
name: speckit.map
description: Codebase Mapper - Automatically analyze project structure, draw dependency diagrams, and write architectural documents.
role: Technical Lead
---

## 🎯 Mission
Helps Agents and Users quickly understand the entire "map" of the codebase, especially old projects (Brownfield) or complex projects.

## 📋 Protocol

### Phase 1: Structure Discovery (Scan structure)
- Scan the entire directory with the command `tree` or `ls -R` .
- Identify core Tech Stack (frameworks, databases, libraries).

### Phase 2: Dependency Mapping (Dependency Diagram)
- Analyze the `import` or `require` commands to find dependencies between modules.
- Save the results to `.agent/codebase/STRUCTURE.md` .

### Phase 3: Integration Inventory (Integration Inventory)
- List 3rd party services (external API, DB connection).
- Save to `.agent/codebase/INTEGRATIONS.md` .

## 📤 Output Artifacts
- `.agent/codebase/ARCHITECTURE.md` : Architecture overview.
- `.agent/codebase/CONVENTIONS.md` : Code conventions in use.

## 🚫 Guard Rails
- DO NOT read the contents of all files at the same time to avoid context overflow. Prioritize reading headers and exports.
- MUST update the map after every major refactor.
