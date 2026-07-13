# bro-skills — Project Rules

## 1. PROJECT SPECIFIC RULES
- **Constitution**: Strictly follow `.agent/memory/constitution.md`.
- **Protocol**: Every task must follow: Specify → Plan → Tasks → Implement.
- **Resources**: Use Workflows in `.agent/workflows/` and Skills in `.agent/skills/`.
- **15-Minute Rule**: Each task must be atomic, ≤ 15 minutes, affecting ≤ 3 files.

## 2. AGENTIC MODE SYNC (Antigravity Only)
- **Task Tracking**: Use `task_boundary` to synchronize status with `@speckit.tasks` (tasks.md).
- **Planning Artifacts**: Create `implementation_plan.md` for large changes (atomic > 3 files).
- **Verification**: Use `walkthrough.md` to compare results with `spec.md` after completion.

## 3. BUILD & RUN QUICK SHEET
- Build: `docker compose build`
- Run: `docker compose up -d`
- Logs: `docker compose logs -f <service>`
- Stop: `docker compose down`
