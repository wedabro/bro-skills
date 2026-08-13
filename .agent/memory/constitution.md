# 📜 Project Constitution

## §0 bro-skills Protocol (REQUIRED)
- **REQUIRED**: All development (Code), testing (Test), and deployment (Deploy Production) activities MUST use `bro-skills`.
- **MANDATORY AUTOMATIC TRIGGER (`/00-speckit.all`)**: Khi người dùng yêu cầu phát triển bất kỳ tính năng hoặc yêu cầu mới nào, Tác nhân AI (Antigravity hoặc bất kỳ Model AI nào) BẮT BUỘC TỰ ĐỘNG kích hoạt workflow `/.agent/workflows/00-speckit.all.md` (`/00-speckit.all`) NGAY LẬP TỨC ở lượt trả lời đầu tiên mà KHÔNG ĐƯỢC ĐỢI NGƯỜI DÙNG NHẮC NHỞ để hoàn thành các bước SDLC (Brainstorm → Specify → Clarify → Plan → Tasks → Analyze) trước khi viết bất kỳ dòng code thực thi nào.
- **Pipeline**: Strictly adhere to the SDLC pipeline: Brainstorm & Align → Specify → Plan → Tasks → Implement.
- **Brainstorming-First**: Before writing any code/spec/plan, the Agent MUST brainstorm with the User to clarify requirements, propose solutions (with pros/cons), and recommend the best path.
- **Tools**: Only use workflows under `.agent/workflows` to execute tasks.

## §1 Infrastructure (DOCKER-FIRST)
- **Docker-First Policy**: Use Docker by default for both Local and Production. DO NOT run `npm`/`node`/`python` directly on host.
- **Local**: Use `docker-compose.yml` for development.
- **Production**: Use `docker-compose.prod.yml` with Security Hardening.
- **Ports**: Flexibly configure ports via environment variables (.env) to avoid conflicts.

## §2 Security & Production Safety
- **FORBIDDEN**: Running `docker compose down -v` on Production.
- **FORBIDDEN**: Manual deployment (MUST use workflows `/deploy-production` or `/deploy-staging`).
- **FORBIDDEN**: Automatic version bumping or pushing version tags (`vX.Y.Z`) without explicit user instruction. Version bump & release tags MUST ONLY be performed when explicitly requested by the User.
- **Confirmation**: Require user confirmation before Deep Clean, Deploy Prod, or Delete Data.
- **Runtime**: Production containers MUST NOT run as root.

## §3 Code Standards & ENV
- **FORBIDDEN hardcoding**: Secrets, tokens, credentials, environment-specific
  URLs, and environment-specific endpoints. Product copy belongs in source or
  i18n resources; runtime configuration belongs in ENV.
- **Sensitive variables**: MUST use ENV (`.env` local, server ENV prod).
  - Prefix: `NEXT_PUBLIC_*`, `API_*`, `DB_*`.
- **Validate**: 
  - Critical variables: `throw new Error()` if missing.
  - Optional variables: `console.error()` if missing.
- **Documentation**: Must have a complete `.env.example` file.

## §4 Workflow & Scripting
- **Automation**: Create scripts when encountering errors or repetitive tasks.
- **Git**: Save scripts in `.agent/scripts` and commit them to version control.
- **Verified Commits**: Commit completed, verified atomic tasks using
  Conventional Commits. Push only when the user explicitly requests publishing
  or the active workflow includes an approved remote-publish boundary.
- **Update**: Update corresponding workflows after creating new scripts.

## §5 UI/UX & Anti-Slop (PREMIUM DESIGN)
- **REQUIRED**: Use the `design-taste-frontend` skill or `/util-speckit.uiux` for UI design.
- **FORBIDDEN**: Using standard template-like UI patterns, default browser colors, or overused AI gradients/shadows.
- **Design System**: MUST comply with Anti-Slop principles (Asymmetric layout, bento grids, Typography-first, Micro-interactions).
