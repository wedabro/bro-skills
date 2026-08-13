# bro-skills — Agent Instructions

Project: bro-skills

## 1. SUPREME ORDER
- Strictly follow the `.agent/memory/constitution.md` file.
- **UI/UX Absolute Priority**: All frontend design, styling, and page rendering MUST strictly follow the UI/UX standards in `.agent/knowledge_base/ui_ux_standards.md` as the absolute source of truth. UI/UX is the highest priority directive; functional code with poor design is considered a failure.
- Docker-First: All coding and app running activities must take place in the container. DO NOT run node/python on the host.
- Ports: Flexibly configure ports via environment variables (.env) to avoid conflicts.

## 2. bro-skills PROTOCOL
- **Mandatory Feature Workflow**: Whenever requested to develop or implement any new feature/requirement, the Agent (Antigravity or any AI model) MUST trigger `/.agent/workflows/00-speckit.all.md` (`/00-speckit.all`) to run the full SDLC pipeline (Brainstorm → Specify → Clarify → Plan → Tasks → Analyze) before implementation.
- Every task must go through the process: Brainstorm & Align → Specify → Plan → Tasks → Implement.
- **Brainstorm-First**: Before writing any code/spec/plan, the Agent MUST brainstorm with the User to clarify requirements, propose solutions (with pros/cons), and recommend the best path.
- Use Workflows in `.agent/workflows/` and Skills in `.agent/skills/`.

## 3. LANGUAGE & CODE
- Respond in Vietnamese.
- 15-Minute Rule: Each task must be atomic, ≤ 15 minutes, affecting ≤ 3 files.
- PowerShell 5.1+, separate commands with `;` (DO NOT use `&&`).
- DO NOT hardcoding URLs, Tokens, Keys. Use ENV vars (`.env`).

## 4. SAFETY
- DO NOT run `docker compose down -v` on Production.
- Generate automatic scripts (`.agent/scripts/`) for recurring errors.
- Check logs immediately on error: `docker compose logs -f <service>`.
- **Verified Commits**: Commit completed, verified atomic tasks using Conventional
  Commits. Push only when the user explicitly requests publishing or the active
  workflow includes an approved remote-publish boundary.

## 5. AGENTIC MODE SYNC (Antigravity Only)
- **Task Tracking**: Use `task_boundary` to synchronize status with `@speckit.tasks` (tasks.md).
- **Planning Artifacts**: Always create `implementation_plan.md` when making large changes (atomic > 3 files).
- **Verification**: After completing the task, use `walkthrough.md` to compare the results with `spec.md`.


## Build & Test
- Build: `docker compose build` (If using Docker)
- Run: `docker compose up -d` (If using Docker)
- Logs: `docker compose logs -f <service>`
- Stop: `docker compose down`
