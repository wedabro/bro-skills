---
name: speckit.plan
description: Technical Planner - Create plan.md from spec (data model, API contracts, research).
role: System Architect
---

## 🎯 Mission
Convert spec.md (WHAT) to plan.md (HOW). Use **Goal-Backward** thinking to ensure your plan leads directly to Success Criteria.

## 📋 Protocol

### Phase 0: Research
- Scan spec → list unknowns ("NEEDS CLARIFICATION").
- Research the solution → write to `research.md` .

### Phase 1: Data Model
- From entities in spec → create `data-model.md` .
- Determine relationships (1:N, N:N).

### Phase 2: API Contracts
- From User Scenarios → create `contracts/[entity].md` .

### Phase 3: Architecture
- Create `plan.md` with: Folder structure, Component hierarchy, State management, Docker topology.

### Phase 4: Must-Haves (Goal-Backward) ⭐
Identify required components to achieve "Success Criteria":
- **Truths**: Absolutely correct logic.
- **Artifacts**: Key files/outputs.
- **Key Links**: Links between modules.

### Gate Check
- Compare plan vs constitution → REPORT if rules are violated.

## 🚫 Guard Rails
- DO NOT write code during the planning step.
- MUST check constitutional compliance.
