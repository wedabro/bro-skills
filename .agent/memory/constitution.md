# 📜 Project Constitution

## §0 bro-skills Protocol (REQUIRED)
- **REQUIRED**: All development (Code), testing (Test), and deployment (Deploy Production) activities MUST use `bro-skills` .
- **Pipeline**: Strictly follow the process: Specify → Plan → Tasks → Implement.
- **Tools**: Only use workflows in `.agent/workflows` to perform tasks.

## §1 Infrastructure (DOCKER-FIRST)
- **Default uses Docker** for both Local and Production. DO NOT run `npm` / `node` / `python` directly on the host.
- **Local**: Use `docker-compose.yml` for dev.
- **Production**: Use `docker-compose.prod.yml` with Security Hardening.
- **Ports**: Only use range **8900-8999**.
  - Public FE: `N` | Admin FE: `N+1` | Backend API: `N+2`

## §2 Security & Production Safety
- **PROHIBITED**: `docker compose down -v` on Production.
- **PROHIBITED**: Manual deployment (MUST use workflows `/deploy-production` or `/deploy-staging` ).
- **Confirm**: Requires confirmation before Deep Clean, Deploy Prod, or Delete Data.
- **Runtime**: Production containers do NOT run as root.

## §3 Code Standards & ENV
- **hard-code PROHIBITED**: URLs, Tokens, Keys, Credentials, Endpoints, Default Text.
- **Sensitive vars**: MUST use ENV ( `.env` local, server ENV prod).
  - Prefix: `NEXT_PUBLIC_*` , `API_*` , `DB_*` .
- **Validate**:
  - Critical vars: `throw new Error()` if missing.
  - Optional vars: `console.error()` if missing.
- **Documentation**: Must have full `.env.example`.

## §4 Workflow & Scripting
- **Automation**: Create scripts when encountering errors or recurring tasks.
- **Git**: Save script to `.agent/scripts` , commit to version control system.
- **Git Auto-Commit**: MUST perform git commit & push immediately after completing any function or task according to Conventional Commits standards.
- **Update**: Update the corresponding workflow after creating a new script.

## §5 UI/UX & Anti-Slop (PREMIUM DESIGN)
- **REQUIRED**: When designing the interface, MUST use skill `design-taste-frontend` or `/util-speckit.uiux` .
- **PROHIBITED**: Using stereotypical UI patterns, pre-existing templates, browser default colors, or abusing gradient/shadow AI.
- **Design System**: MUST comply with Anti-Slop rules (Asymmetric layout, bento grids, Typography-first, Micro-interactions).
