
---
description: Full Pipeline (Specify → Clarify → Plan → Tasks → Analyze)
---

# 🚀 Full Pipeline

## Steps

1. **@speckit.map** — (IF old project) Scans the structure and understands the current codebase.
   - Output: `.agent/codebase/` docs.

2. **@speckit.specify** — Generates spec.md from feature description.
   - Output: `.agent/specs/[feature]/spec.md`.

3. **@speckit.clarify** — Resolve ambiguity and close User Scenarios.

4. **@speckit.roadmap** — Updated `.agent/ROADMAP.md` with new Phase/Milestone.

5. **@speckit.plan** — Create architecture (Goal-Backward).
   - Output: plan.md, must_haves.

6. **@speckit.tasks** — Breakdown to atomic tasks (Task Anatomy).
   - Output: tasks.md.

7. **@speckit.analyze** — 360 degree consistency check.

## Success Criteria
- ✅ spec.md, plan.md, tasks.md exist and are consistent
- ✅ Does not violate the Constitution
