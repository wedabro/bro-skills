---
description: Deploy code according to tasks (Anti-Regression)
---

# 🛠️ Implementation

## Steps

For EACH task `- [ ]` in tasks.md:

1. **@speckit.implement** — Implementation of IRONCLAD Protocols:
   - P1: Blast Radius Analysis.
   - P2: Strategy Selection.
   - P3: TDD (Repro fail first).
   - P4: Context Anchoring.
   - P5: Build Gate (tsc/build).
   - P6: **Deviation Rules** (Auto-fix bugs/missing).
2. Mark `- [X]` when task pass **AND build gate pass**.
3. **Auto-Map**: When ALL tasks are completed, automatically run **@speckit.map** to update the architecture document.
