# 📜 Project Constitution

## §0 bro-skills Protocol (REQUIRED)
- **REQUIRED**: All development (Code), testing (Test), and deployment (Deploy Production) activities MUST use `bro-skills`.
- **Pipeline**: Strictly adhere to the SDLC pipeline: Specify → Plan → Tasks → Implement.
- **Tools**: Only use workflows under `.agent/workflows` to execute tasks.

## §1 Infrastructure (DOCKER-FIRST)
- **Docker-First Policy**: Use Docker by default for both Local and Production. DO NOT run `npm`/`node`/`python` directly on host.
- **Local**: Use `docker-compose.yml` for development.
- **Production**: Use `docker-compose.prod.yml` with Security Hardening.
- **Ports**: Flexibly configure ports via environment variables (.env) to avoid conflicts.

## §2 Security & Production Safety
- **FORBIDDEN**: Running `docker compose down -v` on Production.
- **FORBIDDEN**: Manual deployment (MUST use workflows `/deploy-production` or `/deploy-staging`).
- **Confirmation**: Require user confirmation before Deep Clean, Deploy Prod, or Delete Data.
- **Runtime**: Production containers MUST NOT run as root.

## §3 Code Standards & ENV
- **FORBIDDEN hardcoding**: URLs, Tokens, Keys, Credentials, Endpoints, Default Text.
- **Sensitive variables**: MUST use ENV (`.env` local, server ENV prod).
  - Prefix: `NEXT_PUBLIC_*`, `API_*`, `DB_*`.
- **Validate**: 
  - Critical variables: `throw new Error()` if missing.
  - Optional variables: `console.error()` if missing.
- **Documentation**: Must have a complete `.env.example` file.

## §4 Workflow & Scripting
- **Automation**: Create scripts when encountering errors or repetitive tasks.
- **Git**: Save scripts in `.agent/scripts` and commit them to version control.
- **Git Auto-Commit**: MUST perform git commit & push immediately after completing any function or task according to Conventional Commits standards.
- **Update**: Update corresponding workflows after creating new scripts.

## §5 UI/UX & Anti-Slop (PREMIUM DESIGN)
- **REQUIRED**: Use the `design-taste-frontend` skill or `/util-speckit.uiux` for UI design.
- **FORBIDDEN**: Using standard template-like UI patterns, default browser colors, or overused AI gradients/shadows.
- **Design System**: MUST comply with Anti-Slop principles (Asymmetric layout, bento grids, Typography-first, Micro-interactions).
