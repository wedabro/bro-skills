---
trigger: always_on
glob: "**/*"
description: bro-skills Workspace Rules for bro-skills - ASF 3.3 Standard
---

# 🛡️ bro-skills Workspace Rules

Project: bro-skills

## 1. SUPREME ORDER
- Strictly follow the `.agent/memory/constitution.md` file.
- **UI/UX Absolute Priority**: All frontend design, styling, and page rendering MUST strictly follow the UI/UX standards in `.agent/knowledge_base/ui_ux_standards.md` as the absolute source of truth. UI/UX is the highest priority directive; functional code with poor design is considered a failure.
- Docker-First: All coding and app running activities must take place in the container. DO NOT run node/python on the host.
- Ports: Flexibly configure ports via environment variables (.env) to avoid conflicts.

## 2. bro-skills PROTOCOL
- Every task must go through the process: Specify → Plan → Tasks → Implement.
- Use Workflows in `.agent/workflows/` and Skills in `.agent/skills/`.

## 3. LANGUAGE & CODE
- Respond in English.
- 15-Minute Rule: Each task must be atomic, ≤ 15 minutes, affecting ≤ 3 files.
- PowerShell 5.1+, separate commands with `;` (DO NOT use `&&`).
- DO NOT hardcoding URLs, Tokens, Keys. Use ENV vars (`.env`).

## 4. SAFETY
- DO NOT run `docker compose down -v` on Production.
- Generate automatic scripts (`.agent/scripts/`) for recurring errors.
- Check logs immediately on error: `docker compose logs -f <service>`.
- **Auto-Commit**: MUST perform git commit & push immediately after completing any function or task according to Conventional Commits standards.

## 5. AGENTIC MODE SYNC (Antigravity Only)
- **Task Tracking**: Use `task_boundary` to synchronize status with `@speckit.tasks` (tasks.md).
- **Planning Artifacts**: Always create `implementation_plan.md` when making large changes (atomic > 3 files).
- **Verification**: After completing the task, use `walkthrough.md` to compare the results with `spec.md`.

