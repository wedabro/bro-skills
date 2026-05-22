# Technology & Development Standards

Project: bro-agent
Build System: Docker (docker compose)
Port Range: 8900-8999
Shell: PowerShell 5.1+ (Windows)

## Development Protocol
- Follow Spec-Driven Development (SDD): Specify â†’ Plan â†’ Tasks â†’ Implement.
- Specs directory: `.agent/specs/`
- Constitution: `.agent/memory/constitution.md`
- 15-Minute Rule: Each task must be atomic, â‰¤ 15 minutes, affecting â‰¤ 3 files.

## Environment
- Docker-First: All apps run inside containers. Never run npm/python on host directly.
- ENV vars required for all sensitive config (`.env` files).
- No hardcoded URLs, Tokens, Keys, or Credentials.

## Language
- Respond in Vietnamese (Tiáº¿ng Viá»‡t).

## Safety
- NEVER run `docker compose down -v` on Production.
- Always check logs on error: `docker compose logs -f <service>`.

