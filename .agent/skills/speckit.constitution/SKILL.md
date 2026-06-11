---
name: speckit.constitution
description: Governance Manager - Set up & manage Constitution (Source of Law).
role: Governance Architect
---

## 🎯 Mission
Create and maintain constitution.md — the "supreme law" that every agent must comply with.

## 📥 Input
- Developer provides: tech stack, principles, constraints
- `.agent/knowledge_base/infrastructure.md` (if available)

## 📋 Protocol
1. Collected from developers:
   - Tech stack (frameworks, DB, language)
   - Docker ports (trong range 8900-8999)
   - Coding principles (VD: No hardcode, API-first)
   - Security requirements
2. Create/update `.agent/memory/constitution.md` with REQUIRED sections:
   - **§1 Infrastructure**: Docker-first policy, port allocation, environments
   - **§2 Security**: No root containers, no hardcoded secrets, multi-stage builds
   - **§3 Code Standards**: Language, naming conventions, ENV policy
   - **§4 Non-Negotiables**: List of rules that should NEVER be violated
   - **§5 Monorepo Rules** (if monorepo):
     - Shared Package Contract: type exports is the source of truth
     - Build Independence: each app must be compiled independently
     - Package exports must match actual file structure
   - **§6 Docker Deployment Rules**:
     - Volume shadowing ( `- .:/app` ) is PROHIBITED in production/beta
     - Dockerfile COPY paths must exist
     - CMD entrypoint must match build output
     - Next.js apps must have a `public/` folder
   - **§7 Build-time Safety** (if Next.js):
     - SSG pages (sitemap, generateStaticParams): API calls must be try-catch
     - fetchApi must return null/empty if API_URL is undefined
   - **§8 Pre-Deploy Checklist**:
     - `docker compose build` succeeded
     - All services `Up` (not `Restarting` )
     - Health check: 200 OK
3. Validate: Each section must have at least 1 specific rule, not general.

## 📤 Output
- File: `.agent/memory/constitution.md`

## 🚫 Guard Rails
- Constitution does NOT contain implementation details (HOW) — only rules (WHAT).
- Each rule must be testable (can be verified with code/check).
