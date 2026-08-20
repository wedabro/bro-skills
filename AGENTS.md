# bro-skills — Agent Instructions

Project: bro-skills

## 1. SUPREME ORDER
- Strictly follow the `.agents/memory/constitution.md` file.
- **UI/UX Absolute Priority**: All frontend design, styling, and page rendering MUST strictly follow the UI/UX standards in `.agents/knowledge_base/ui_ux_standards.md` as the absolute source of truth. UI/UX is the highest priority directive; functional code with poor design is considered a failure.
- Docker-First: All coding and app running activities must take place in the container. DO NOT run node/python on the host.
- Ports: Flexibly configure ports via environment variables (.env) to avoid conflicts.

## 2. bro-skills PROTOCOL
- **MANDATORY AUTOMATIC TRIGGER (`/00-speckit.all`)**: Khi người dùng yêu cầu phát triển hoặc thực hiện bất kỳ tính năng/yêu cầu mới nào, Tác nhân AI (Antigravity hoặc bất kỳ Model nào) BẮT BUỘC TỰ ĐỘNG kích hoạt workflow `/.agents/workflows/00-speckit.all.md` (`/00-speckit.all`) NGAY LẬP TỨC ở lượt trả lời đầu tiên mà KHÔNG ĐƯỢC ĐỢI NGƯỜI DÙNG NHẮC NHỞ. Phải tuân thủ nghiêm ngặt toàn bộ quy trình SDLC (Brainstorm → Specify → Clarify → Plan → Tasks → Analyze) trước khi viết bất kỳ dòng code thực thi nào.
- Every task must go through the process: Brainstorm & Align → Specify → Plan → Tasks → Implement.
- **Brainstorm-First**: Before writing any code/spec/plan, the Agent MUST brainstorm with the User to clarify requirements, propose solutions (with pros/cons), and recommend the best path.
- Use Workflows in `.agents/workflows/` and Skills in `.agents/skills/`.

## 3. LANGUAGE & CODE
- Respond in Vietnamese.
- 15-Minute Rule: Each task must be atomic, ≤ 15 minutes, affecting ≤ 3 files.
- PowerShell 5.1+, separate commands with `;` (DO NOT use `&&`).
- DO NOT hardcoding URLs, Tokens, Keys. Use ENV vars (`.env`).

## 4. SAFETY
- DO NOT run `docker compose down -v` on Production.
- Generate automatic scripts (`.agents/scripts/`) for recurring errors.
- Check logs immediately on error: `docker compose logs -f <service>`.
- **Version Bump Policy**: Agent MUST NEVER automatically bump version or create/push new version tags (`vX.Y.Z`). ONLY bump version and release when explicitly requested by the User.
- **Verified Commits**: Commit completed, verified atomic tasks using Conventional Commits. Push code/tags only when explicitly requested by the User.

## 5. AGENTIC MODE SYNC (Antigravity Only)
- **Task Tracking**: Use `task_boundary` to synchronize status with `@speckit.tasks` (tasks.md).
- **Planning Artifacts**: Always create `implementation_plan.md` when making large changes (atomic > 3 files).
- **Verification**: After completing the task, use `walkthrough.md` to compare the results with `spec.md`.

## 6. CONTINUOUS LEARNING & SELF-CORRECTION
- **Lessons Log**: Strictly consult and maintain `.agents/memory/lessons_learned.md`.
- **Anti-Regression**: After resolving any bug, edge case, or workflow issue, document the root cause and prevention rule in `lessons_learned.md` so the mistake is NEVER repeated.


## Build & Test
- Build: `docker compose build` (If using Docker)
- Run: `docker compose up -d` (If using Docker)
- Logs: `docker compose logs -f <service>`
- Stop: `docker compose down`

