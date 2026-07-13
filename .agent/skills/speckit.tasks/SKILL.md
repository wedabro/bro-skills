---
name: speckit.tasks
description: Task Breaker - Create atomic tasks.md, with dependency order from plan.
---

## 🎯 Mission
Convert plan.md into a list of atomic tasks, ordered by dependency, each task ≤15 minutes.

## 📥 Input
- `.agent/specs/[feature]/plan.md`
- `.agent/specs/[feature]/spec.md`

## 📋 Protocol
1. Read plan.md → break down each component into atomic tasks.
2. REQUIRED format for each task:
   ```
   - [ ] T001 [P] Setup project structure per plan.md
   - [ ] T002 [P] Create database schema in prisma/schema.prisma
   - [ ] T003 [P] [US1] Implement user registration API in src/api/auth.ts
   ```
   - `[P]`: Priority (blocking task)
   - `[US1]` : Link to User Scenario
   - Path: Main file affected
3. Phase Structure REQUIRED:
   - **Phase 1: Setup** — Project init, configs, boilerplate
   - **Phase 2: Foundation** — DB, auth, shared utilities (blocking)
   - **Phase 3+**: Each User Story = 1 phase (according to priority from spec)
   - **Final Phase: Polish** — Error handling, optimization, cleanup
4. Dependency Rules:
   - Task depends on another task → must be placed AFTER.
   - Foundation tasks are always in Phase 2.
5. **15-Minute Rule**: Each task takes ≤ 15 minutes, affects ≤ 3 files.

## 📤 Output
- File: `.agent/specs/[feature]/tasks.md`

## 🚫 Guard Rails
- DO NOT create tasks that are too large (>3 files or >15 minutes).
- DO NOT create duplicate tasks.
- Each task MUST have a specific file path.
