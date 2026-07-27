---
name: speckit.checker
description: Static Analysis Aggregator - Run static analysis on the codebase.
---

## 🎯 Mission
Detect coding-standard violations, security issues, and performance
anti-patterns using commands appropriate to the actual project stack.
**MUST run applicable checks** — do not claim a check passed from visual review.

## 📥 Input
- Source code and dependency manifests
- `.agent/memory/constitution.md` (coding standards)
- `.agent/project.json` and documented build/test commands
- Docker files when the project is containerized

## 📋 Protocol

### Phase 1: Capability Discovery

1. Read project configuration and dependency manifests.
2. Detect language, package manager, containerization, services, and available
   build/lint/type-check scripts.
3. Build an applicability table. Mark unavailable checks `N/A` with a reason;
   never treat `N/A` as a pass or failure.

### Phase 2: Compile, Type, and Lint Checks

- Run the repository-defined compile, type-check, and lint commands.
- If the constitution requires container execution, run them in the matching
  service. Otherwise use the project's documented runtime.
- Compiler/type errors are 🔴 CRITICAL. Lint severity follows project policy.
- Do not assume TypeScript, npm, a monorepo, or fixed service names.

### Phase 3: Container Checks (When Applicable)

- Validate every discovered Compose file with `docker compose ... config`.
- Verify Dockerfile COPY sources, non-root production runtime, health checks,
  environment-driven published ports, and no production source shadowing.
- If the project is not containerized, record this phase as `N/A`.

### Phase 4: Configuration and Security

- Scan source and tracked files for likely secrets, unsafe URL/endpoint
  literals, injection sinks, unsafe HTML, dynamic evaluation, and SQL
  concatenation.
- Exclude generated/vendor directories and report redacted locations only.
- Treat intentional public URLs, documentation links, and schema identifiers
  according to project policy rather than flagging every `https://` literal.

### Phase 5: Stack-Specific Integrity

- Apply framework checks only when that framework is detected.
- For monorepos, verify package exports and cross-package contracts.
- For server-rendered applications, inspect build-time data fetching and error
  behavior according to the framework and project requirements.

## 📤 Output
- File: `.agent/memory/checker-report.md`
- Format:
  ```
  ## 🔴 CRITICAL (N issues)
  - `apps/web/src/app/page.tsx:65` — Property 'category' does not exist on type 'Article'
  ## 🟡 WARNING (N issues)
  - `compose.prod.yml:40` — Source mount overrides the built production artifact
  ## 🟢 INFO (N issues)
  - ...
  ```

## 🚫 Guard Rails
- Report ONLY — DO NOT edit the code yourself.
- Each finding must have a specific file path + line number.
- MUST run every applicable configured check; visual scanning alone is not enough.
- If there is 🔴 CRITICAL → FAIL conclusion, deployment is NOT allowed.
