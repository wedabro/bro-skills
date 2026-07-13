---
name: speckit.roadmap
description: Roadmap Strategist - Manage high-level roadmaps (Milestones) and transitions between Phases.
---

## 🎯 Mission
Ensure the project is on track according to the long-term vision, managing dependencies between phases (Phases) and milestones (Milestones).

## 📋 Protocol

### Phase 1: Milestone Definition
- Create/Update `.agent/ROADMAP.md` .
- Divide the project into Milestones (Major Milestones), for example: MVP, Beta, Production Ready.
- Each Milestone contains a list of Phases.

### Phase 2: Progress Tracking
- Update the completion status of each Phase based on the results from `speckit.status` .
- Ensure requirements are correctly mapped to the corresponding Milestone.

### Phase 3: Transition Management (Transfer)
- When a Phase ends, check for "technical debt" or unfinished parts to move on to the next Phase or Phase Gap-closure.

## 🚫 Guard Rails
- MUST maintain consistency between the Roadmap and actual implementation.
- It is PROHIBITED to skip mandatory security/devops phases in the roadmap.
