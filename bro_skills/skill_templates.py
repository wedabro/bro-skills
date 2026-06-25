"""
Skill Templates - Detailed SKILL.md content for 29 skills.
Principle: Concise but precise enough for AI to know what to do, what to read, what to output, and what NOT to do.
"""


def skill_identity():
    return r"""
---
name: speckit.identity
description: Manage AI personality and behavioral orientation for the project.
role: Persona Architect
---

## 🎯 Mission
Create and maintain file `master-identity.md` — defines who AI is in this project context.

## 📥 Input
- `.agent/project.json` (project type, name)
- `.agent/memory/constitution.md` (tech stack, principles)
- Codebase scan results (if any)

## 📋 Protocol
1. Read `project.json` → determine project type and domain.
2. Read `constitution.md` → extract tech stack, principles, non-negotiables.
3. Analyze the codebase (if any) → determine the patterns and conventions in use.
4. Create/update `.agent/identity/master-identity.md` with sections:
   - **Persona**: Role + expertise domain. **MANDATORY communication in Vietnamese**.
   - **Core Capabilities**: 3-5 main abilities.
   - **Collaboration Style**: How to interact with developers.
   - **Soul (Core Beliefs)**: Must include "bro-skills First" and "Docker is the Law".
   - **Project Context**: Tech stack, DB, Docker info (auto-detected).
5. If project type is `web_public` / `fullstack` → add SEO & GEO Awareness section.

## 📤 Output
- File: `.agent/identity/master-identity.md`

## 🚫 Guard Rails
- DO NOT create a persona that is too general — it must be closely tied to the project domain.
- DO NOT add capabilities that the project does not use (eg: do not say ML if there is no ML).
- DO NOT use languages ​​other than Vietnamese when communicating with Users.
"""


def skill_devops():
    return r"""
---
name: speckit.devops
description: Docker Infrastructure & Security Hardening Specialist — Port ENV-first, range 8900-8999.
role: DevOps Architect
---

## 🎯 Mission
Set up and manage a standardized and secure Docker system for the project.
Ports MUST always be configured via ENV vars — NEVER hard-code.

## 📥 Input
- `.agent/memory/constitution.md` (port range, security rules)
- Existing `Dockerfile` , `docker-compose.yml` (if available)
- `.env.example`

## 📋 Protocol

### 1. Port Allocation (ENV-first) ⭐

**ALWAYS configure ports via ENV:**
- `.env` file (local) or server ENV (production)
- `docker-compose.yml` reads: `"${PUBLIC_PORT:-8920}:3000"`
- DO NOT hard-code port number in any file

**Port scanning rules according to environment:**

| Environment | Docker running? | Act |
|---|---|---|
| **Local** | ❌ No (first time) | Scan range `8900-8999` with socket/helper → select 3 consecutive empty ports |
| **Local** | ✅ Already running | **SKIP** scan — use current ports from `.env` / docker |
| **Staging/Beta/Prod** | Any | **ALWAYS** initial scan for configuration → write to `.env` |

**Check Docker is running (Local):**
```bash
docker compose ps --format json 2>$null
# There are containers → SKIP port scan
# Empty/error → RUN port scan
```

- Pattern: Public FE `N` → Admin FE `N+1` → Backend API `N+2`

### 2. Local Docker (`docker-compose.yml`):
- Ports read from ENV: `"${PUBLIC_PORT:-8920}:3000"`
- Volume mounts cho hot-reload code
- Named volumes for `node_modules` (avoid host-container lock)
- Health checks for each service

### 3. Production Docker (`docker-compose.prod.yml`):
- Multi-stage builds (builder → runner)
- `USER node` or `USER appuser` (DO NOT run as root)
- Remove devDependencies in the final image
- Alpine/Slim base images
- Ports read from ENV (NO hard-code)

### 4. Security Checklist:
- `.dockerignore`: block `.env`, `.git`, `node_modules`
- No hard-code secrets in Dockerfile
- Only EXPOSE ports are needed

### 5. Documentation:
- Update `.agent/knowledge_base/infrastructure.md` with the results
- Update `.env.example` with all port vars

## 📤 Output
- Files: `Dockerfile`, `docker-compose.yml`, `docker-compose.prod.yml`, `.dockerignore`
- Config: `.env` (ports), `.env.example` (documented)
- Doc: `.agent/knowledge_base/infrastructure.md` (updated)

## 🚫 Guard Rails
- DO NOT use ports outside the 8900-8999 range.
- DO NOT hard-code port numbers — ALWAYS use ENV vars.
- DO NOT run `docker compose down -v` on production.
- DO NOT hard-code credentials into the Dockerfile.
- DO NOT scan ports when Docker local is already running (with containers).
"""


def skill_analyze():
    return r"""
---
name: speckit.analyze
description: Consistency Checker - Analyze consistency between spec, plan, tasks.
role: Consistency Analyst
---

## 🎯 Mission
Make sure spec.md, plan.md, tasks.md do not conflict and cover all requirements.

## 📥 Input
- `.agent/specs/[feature]/spec.md`
- `.agent/specs/[feature]/plan.md`
- `.agent/specs/[feature]/tasks.md`

## 📋 Protocol
1. **Coverage Check**: Each User Scenario in the spec → must have task(s) in tasks.md.
2. **Conflict Check**: Plan says to use tech A but tasks reference tech B → ERROR REPORT.
3. **Constitution Check**: Compare plan.md with constitution.md → detect violations.
4. **Completeness Check**: Each data model in the plan → must have a model creation + migration task.
5. **Gap Analysis table output**:
   ```
   | Spec Requirement | Plan Section | Task ID | Status |
   |------------------|-------------|---------|--------|
   | User login       | Auth flow   | T005    | ✅ OK  |
   | Payment          | -           | -       | ❌ GAP |
   ```
6. Calculate Coverage Score: `(matched / total) × 100%` .

## 📤 Output
- Console: Gap Analysis table + Coverage Score
- File: `.agent/memory/analyze-report.md`

## 🚫 Guard Rails
- Reporting ONLY — DO NOT arbitrarily edit artifacts.
- Each gap must clearly indicate which artifact is missing.
"""


def skill_checker():
    return r"""
---
name: speckit.checker
description: Static Analysis Aggregator - Run static analysis on the codebase.
role: Static Analyst
---

## 🎯 Mission
Codebase scanning detects violations of coding standards, security issues, performance anti-patterns.
**MUST run actual commands** — not just scan by eye.

## 📥 Input
- Source code (all `src/` , `app/` , `pages/` )
- `.agent/memory/constitution.md` (coding standards)
- `Dockerfile`, `docker-compose*.yml`

## 📋 Protocol

### Phase 1: TypeScript Compile Check (CRITICAL)
This is the most important step, MUST run before every deploy:
```bash
# In Docker container or local:
docker compose exec <service> npx tsc --noEmit
# Or try building:
docker compose build 2>&1 | grep -i "error\|fail"
```
- Catch: type mismatch, missing props, wrong property names, import errors
- All TS errors are 🔴 CRITICAL

### Phase 2: Dockerfile & Docker Compose Lint
```bash
# Check for any COPY sources that exist
# Check out docker compose syntax:
docker compose -f docker-compose*.yml config --quiet
# Check volume shadowing (Using volumes for production is PROHIBITED):
grep -A 5 "volumes:" docker-compose.prod.yml # Must NOT have `. :/app`
```
- Volume mount `- .:/app` trong production → 🔴 CRITICAL
- COPY path does not exist → 🔴 CRITICAL
- Outer port 8900-8999 → 🟡 WARNING

### Phase 3: ENV Compliance
```bash
# Find hard-coded URLs/tokens:
grep -rn "http://localhost\|http://127.0.0.1\|https://" apps/*/src/ --include="*.ts" --include="*.tsx" | grep -v "node_modules\|.next\|schema.org"
# Find default text fallback:
grep -rn '|| "' apps/*/src/ --include="*.ts" --include="*.tsx" | grep -v "node_modules"
```

### Phase 4: Import Hygiene
- Find unused imports, circular dependencies
- Verify shared package exports match actual usage

### Phase 5: Build-time Safety (Next.js specific)
```bash
# Find SSG/SSR pages that call the API without try-catch:
grep -rn "await api\.\|await fetchApi" apps/*/src/app/sitemap.ts apps/*/src/app/*/page.tsx
# Each result must be in a try-catch block
```
- API call in `generateStaticParams` / `sitemap()` has no try-catch → 🔴 CRITICAL

### Phase 6: Security Scan
- Find `eval()` , `dangerouslySetInnerHTML` (need sanitize), SQL concatenation
- Find secrets/keys in source code

### Phase 7: Monorepo Integrity
- Verify shared package exports match imports
- Cross-reference types: every `entity.X` must exist in the interface

## 📤 Output
- File: `.agent/memory/checker-report.md`
- Format:
  ```
  ## 🔴 CRITICAL (N issues)
  - `apps/web/src/app/page.tsx:65` — Property 'category' does not exist on type 'Article'
  ## 🟡 WARNING (N issues)
  - `docker-compose.beta.yml:40` — Volume mount `.:/app` will override built code
  ## 🟢 INFO (N issues)
  - ...
  ```

## 🚫 Guard Rails
- Report ONLY — DO NOT edit the code yourself.
- Each finding must have a specific file path + line number.
- **MUST run `tsc --noEmit` or `docker compose build` ** — visual scanning is NOT ENOUGH.
- If there is 🔴 CRITICAL → FAIL conclusion, deployment is NOT allowed.
"""


def skill_checklist():
    return r"""
---
name: speckit.checklist
description: Requirements Validator - Create and validate checklist from spec.
role: Requirements Auditor
---

## 🎯 Mission
Extract all functional requirements from spec.md into a trackable checklist.

## 📥 Input
- `.agent/specs/[feature]/spec.md`
- `.agent/specs/[feature]/tasks.md` (if available)

## 📋 Protocol
1. Read spec.md → extract all requirements (from User Scenarios + Success Criteria).
2. Create checklist format:
   ```markdown
   ## Functional Requirements
   - [ ] FR01: User can register an account → T003, T004
   - [ ] FR02: User can log in → T005
   - [x] FR03: User can view product → T010 ✅
   ```
3. If there is tasks.md → link each requirement to task IDs.
4. Enter status: ✅ Met / ❌ Not Met / ⚠️ Partial.

## 📤 Output
- File: `.agent/specs/[feature]/checklist.md`

## 🚫 Guard Rails
- Each requirement MUST be quoted from spec.md (not made up).
"""


def skill_clarify():
    return r"""
---
name: speckit.clarify
description: Ambiguity Resolver - Detect and resolve ambiguity in spec.
role: Clarity Engineer
---

## 🎯 Mission
Scan spec.md → detect ambiguity → ask developer up to 3 questions → update spec.

## 📥 Input
- `.agent/specs/[feature]/spec.md`

## 📋 Protocol
1. Scan spec.md to find:
   - **Vague language**: "fast", "many", "easy to use", "similar", "etc."
   - **Missing boundaries**: Unknown min/max, pagination limits, file size limits
   - **Undefined error handling**: What happens when X fails?
   - **Ambiguous actors**: Who is "User"? Admin? Guest? Registered?
2. Categorize each issue:
   - 🔴 **CRITICAL**: Architectural influence, MUST ask developer
   - 🟡 **IMPORTANT**: Should ask but can suggest default
   - 🟢 **MINOR**: Can be fixed by yourself (eg: add "maximum 50 items" if missing)
3. Ask the developer MAXIMUM 3 CRITICAL questions, each question has an options table:
   ```
| Option | Describe | Impact |
   |--------|-------|--------|
   | A      | ...   | ...    |
   | B      | ...   | ...    |
   | C      | ...   | ...    |
   ```
4. Auto-fix items 🟢 MINOR.
5. Update spec.md with clarifications → mark `[CLARIFIED]` .

## 📤 Output
- File: Updated `.agent/specs/[feature]/spec.md`

## 🚫 Guard Rails
- MAXIMUM 3 questions — don't ask too many.
- DO NOT change the original intent of the spec.
"""


def skill_constitution():
    return r"""
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
"""


def skill_diff():
    return r"""
---
name: speckit.diff
description: Artifact Comparator - Compares differences between artifacts.
role: Diff Analyst
---

## 🎯 Mission
Compare 2 versions of artifact → highlight changes → evaluate impact.

## 📥 Input
- 2 files or 2 versions to compare (spec, plan, tasks, code)

## 📋 Protocol
1. Read both versions.
2. Compare section-by-section:
   - ➕ **Added**: New Sections/requirements
   - ➖ **Removed**: Sections/requirements are removed
   - ✏️ **Changed**: Sections have changed content
3. Impact Analysis: What downstream artifact does each change affect?
   - For example: Add fields in spec → need to update plan → need to add tasks
4. Output summary table.

## 📤 Output
- Console: Diff summary table
- File: `.agent/memory/diff-report.md` (if needed to save)

## 🚫 Guard Rails
- Compare and report ONLY — DO NOT arbitrarily edit artifacts.
"""


def skill_implement():
    return r"""
---
name: speckit.implement
description: Code Builder (Anti-Regression) - Deploy code in tasks with IRONCLAD protocols.
role: Master Builder
---

## 🎯 Mission
Implement code according to tasks.md, complying with IRONCLAD Protocols and **Deviation Rules** to operate automatically when encountering errors.

## 📋 Protocol

### IRONCLAD Protocols:
1. **Blast Radius**: Analyzes risk based on the number of affected files.
2. **Strategy**: Choose direct editing or Strangler Pattern.
3. **TDD**: Create repro script fail -> code -> pass.
4. **Context Anchoring**: Re-read constitution every 3 tasks.
5. **Build Gate**: ALWAYS run tsc/build after each task.

### Deviation Rules (Self-handling when deviating) ⭐
- **Bug detected**: Automatically fix if within scope, or create new task if serious.
- **Missing Critical**: If important config/file is missing, automatically add it immediately.
- **Blocker**: If stuck, perform "Root Cause Analysis" yourself before asking the user.
- **Arch Change**: If you need to change the architecture, you MUST ask the user.

### Self-Check Protocol
- All tasks are only completed when they pass Build Gate (no Type errors, no Docker errors).

## 🚫 Guard Rails
- DO NOT commit build error code.
- NO hard-code sensitive info.
"""


def skill_migrate():
    return r"""
---
name: speckit.migrate
description: Legacy Code Migrator - Reverse-engineer existing codebase to SDD standard.
role: Migration Specialist
---

## 🎯 Mission
Scan legacy codebase → create spec + preliminary plan → evaluate tech debt → propose migration path.

## 📥 Input
- Existing codebase (source code, configs, DB schema)
- `.agent/memory/constitution.md` (target standards)

## 📋 Protocol
1. **Scan Phase**: Use ProjectScanner patterns to detect:
   - Languages, frameworks, dependencies
   - Data models (Prisma/SQL/Mongoose schemas)
   - API routes, pages, components
   - Docker setup (if any)
2. **Reverse-Engineer Spec**: From code → create draft `spec.md` :
   - Each page/route → 1 User Scenario
   - Each data model → 1 entity description
3. **Tech Debt Inventory** (`migration-risk.md`):
   - 🔴 Critical: Security holes, deprecated deps, no tests
   - 🟡 Important: Missing Docker, no CI/CD, inconsistent patterns
   - 🟢 Minor: Code style, naming conventions
4. **Migration Sequence**: Suggested migration order (less risk first).

## 📤 Output
- `.agent/specs/migration/spec.md` (draft)
- `.agent/specs/migration/migration-risk.md`

## 🚫 Guard Rails
- DO NOT refactor code in this step — just analyze and document.
- DO NOT delete old code.
"""


def skill_plan():
    return r"""
---
name: speckit.plan
description: Technical Planner - Create plan.md from spec (data model, API contracts, research).
role: System Architect
---

## 🎯 Mission
Convert spec.md (WHAT) to plan.md (HOW). Use **Goal-Backward** thinking to ensure your plan leads directly to Success Criteria.

## 📋 Protocol

### Phase 0: Research
- Scan spec → list unknowns ("NEEDS CLARIFICATION").
- Research the solution → write to `research.md` .

### Phase 1: Data Model
- From entities in spec → create `data-model.md` .
- Determine relationships (1:N, N:N).

### Phase 2: API Contracts
- From User Scenarios → create `contracts/[entity].md` .

### Phase 3: Architecture
- Create `plan.md` with: Folder structure, Component hierarchy, State management, Docker topology.

### Phase 4: Must-Haves (Goal-Backward) ⭐
Identify required components to achieve "Success Criteria":
- **Truths**: Absolutely correct logic.
- **Artifacts**: Key files/outputs.
- **Key Links**: Links between modules.

### Gate Check
- Compare plan vs constitution → REPORT if rules are violated.

## 🚫 Guard Rails
- DO NOT write code during the planning step.
- MUST check constitutional compliance.
"""


def skill_quizme():
    return r"""
---
name: speckit.quizme
description: Logic Challenger (Red Team) - Ask critical questions, find edge cases.
role: Red Team Analyst
---

## 🎯 Mission
Challenge spec + plan with edge-case questions, find logic flaws before implementation.

## 📥 Input
- `.agent/specs/[feature]/spec.md`
- `.agent/specs/[feature]/plan.md`

## 📋 Protocol
1. Read spec + plan → find implicit assumptions.
2. Generate a MAXIMUM of 5 edge-case questions, each in 1 category:
   - **Boundary**: "What if the user enters 0 products?"
   - **Concurrency**: "If two people buy the final product together?"
   - **Failure**: "If payment gateway timeout?"
   - **Security**: "If the user edits the price in the request?"
   - **Scale**: "If there are 100K products, how will the performance be?"
3. For each question → suggest a solution if the developer confirms it is the problem.
4. Interactive: Wait for the developer to respond → decide whether to update the spec or not.

## 📤 Output
- Console: Interactive Q&A session
- File: `.agent/memory/quizme-findings.md` (if issues are detected)

## 🚫 Guard Rails
- MAXIMUM 5 questions — don't overwhelm the developer.
- Questions must be REALISTIC, do not ask edge cases that are too far-fetched.
"""


def skill_reviewer():
    return r"""
---
name: speckit.reviewer
description: Code Reviewer - Review code according to spec and best practices.
role: Code Reviewer
---

## 🎯 Mission
Review implementation code → ensure correct spec, security, performance.

## 📥 Input
- Source code (implemented files)
- `.agent/specs/[feature]/spec.md` + `plan.md`
- `.agent/memory/constitution.md`

## 📋 Protocol
1. **Spec Compliance**: Does the code correctly implement all requirements in the spec?
2. **Error Handling**: Does every API route have try-catch? Is return in the correct error format?
3. **Security**: Find injection risks, missing auth checks, exposed secrets.
4. **Performance**: Found N+1 queries, awaiting waterfalls, missing pagination.
5. **Constitution**: Does the code violate any rules in constitution.md?
6. **Output**: Verdict + table findings:
   ```
   | File:Line | Severity | Issue | Suggestion |
   |-----------|----------|-------|------------|
   | api/users.ts:45 | 🔴 | Missing auth | Add middleware |
   ```
7. Verdict: ✅ **APPROVE** or ❌ **REQUEST CHANGES** (with list to fix).

## 📤 Output
- File: `.agent/memory/review-report.md`

## 🚫 Guard Rails
- DO NOT fix the code yourself — only review and make suggestions.
- Each finding MUST have a specific file:line.
"""


def skill_specify():
    return r"""
---
name: speckit.specify
description: Feature Definer - Generates spec.md from natural language description.
role: Domain Scribe
---

## 🎯 Mission
Pass natural language description → standardized spec.md (WHAT, not HOW).

## 📥 Input
- Feature description from developer (free text)
- `.agent/memory/constitution.md` (constraints)

## 📋 Protocol
1. Read description → extract:
   - **Actors**: Who interacts? (User, Admin, System, Guest)
   - **Actions**: Do what? (CRUD, search, filter, export)
   - **Data**: What data? (entities, fields, relationships)
   - **Constraints**: What limits? (auth, permissions, limits)
2. Create `.agent/specs/[feature]/spec.md` with REQUIRED format:
   ```markdown
   ---
   title: [Feature Name]
   status: DRAFT
   version: 1.0.0
   created: [date]
   ---
   ## 1. Overview
   [1-2 sentence description]

   ## 2. User Scenarios
   - **US1**: As a [actor], I want to [action], so that [value].
   - **US2**: ...

   ## 3. Functional Requirements
   - FR01: [specific, measurable requirement]

   ## 4. Non-Functional Requirements
   - NFR01: Response time < 2s

   ## 5. Success Criteria
   - [ ] SC01: [testable criterion]
   ```
3. Each User Scenario MUST have: Actor + Action + Value.
4. Each Functional Requirement MUST be measurable (have specific data).

## 📤 Output
- File: `.agent/specs/[feature]/spec.md`

## 🚫 Guard Rails
- DO NOT write implementation details (HOW) — just describe WHAT.
- DO NOT use technical jargon in User Scenarios (business language).
- DO NOT ignore error cases — each action must have a "what if it fails?"
"""


def skill_status():
    return r"""
---
name: speckit.status
description: Progress Dashboard - Displays project progress status.
role: Progress Tracker
---

## 🎯 Mission
Parse tasks.md → calculate progress → display visual dashboard.

## 📥 Input
- `.agent/specs/[feature]/tasks.md`

## 📋 Protocol
1. Parse tasks.md → count checkboxes:
   - `- [X]` = completed
   - `- [ ]` = pending
2. Group by Phase → calculate % for each phase.
3. Output dashboard:
   ```
   📊 Progress Dashboard: [Feature Name]
   ═══════════════════════════════════════
   Phase 1: Setup        ████████████████ 100% (4/4)
   Phase 2: Foundation   ████████░░░░░░░░  50% (3/6)
   Phase 3: User Auth    ░░░░░░░░░░░░░░░░   0% (0/5)
   ───────────────────────────────────────
   Total:                ███████░░░░░░░░░  47% (7/15)
   ```
4. List of pending tasks (next to do).

## 📤 Output
- Console: Dashboard visualization

## 🚫 Guard Rails
- DO NOT change tasks.md — read and report only.
"""


def skill_tasks():
    return r"""
---
name: speckit.tasks
description: Task Breaker - Create atomic tasks.md, with dependency order from plan.
role: Execution Strategist
---

## 🎯 Mission
Convert plan.md into a list of atomic tasks, ordered by dependency, each task ≤15 minutes.

## 📥 Input
- `.agent/specs/[feature]/plan.md`
- `.agent/specs/[feature]/spec.md`

## 📋 Protocol
1. Read plan.md → break down each component into atomic tasks.
2. REQUIRED format for each task:
   ```
   - [ ] T001 [P] Setup project structure per plan.md
   - [ ] T002 [P] Create database schema in prisma/schema.prisma
   - [ ] T003 [P] [US1] Implement user registration API in src/api/auth.ts
   ```
   - `[P]`: Priority (blocking task)
   - `[US1]` : Link to User Scenario
   - Path: Main file affected
3. Phase Structure REQUIRED:
   - **Phase 1: Setup** — Project init, configs, boilerplate
   - **Phase 2: Foundation** — DB, auth, shared utilities (blocking)
   - **Phase 3+**: Each User Story = 1 phase (according to priority from spec)
   - **Final Phase: Polish** — Error handling, optimization, cleanup
4. Dependency Rules:
   - Task depends on another task → must be placed AFTER.
   - Foundation tasks are always in Phase 2.
5. **15-Minute Rule**: Each task takes ≤ 15 minutes, affects ≤ 3 files.

## 📤 Output
- File: `.agent/specs/[feature]/tasks.md`

## 🚫 Guard Rails
- DO NOT create tasks that are too large (>3 files or >15 minutes).
- DO NOT create duplicate tasks.
- Each task MUST have a specific file path.
"""


def skill_taskstoissues():
    return r"""
---
name: speckit.taskstoissues
description: Issue Tracker Syncer - Synchronize tasks.md to issue tracker.
role: Issue Syncer
---

## 🎯 Mission
Parse tasks.md → create issues ready to import into GitHub/GitLab/Jira.

## 📥 Input
- `.agent/specs/[feature]/tasks.md`

## 📋 Protocol
1. Parse each task → extract: ID, title, description, phase, user story link.
2. Map sang issue format:
   ```markdown
   **Title**: T003 - Implement user registration API
   **Labels**: phase-2, us-1, backend
   **Description**:
   - File: `src/api/auth.ts`
   - Depends on: T002
   - Acceptance: User can register with email/password
   ```
3. Group issues by Phase → create Milestones.
4. Output file `.agent/memory/issues-export.md`.

## 📤 Output
- File: `.agent/memory/issues-export.md`

## 🚫 Guard Rails
- DO NOT create an issue on the remote — just generate an export file.
"""


def skill_tester():
    return r"""
---
name: speckit.tester
description: Test Runner & Coverage - Create test plans, write tests, report coverage.
role: Test Engineer
---

## 🎯 Mission
Make sure the implementation has full test coverage and passes 100%.

## 📥 Input
- Source code (implemented files)
- `.agent/specs/[feature]/tasks.md` (completed tasks)
- `.agent/specs/[feature]/spec.md` (success criteria)

## 📋 Protocol
1. **Test Plan**: From tasks.md (completed) → list functions/routes to test.
2. **Write Tests**: For each function/route:
   - Happy path (valid input → correct output)
   - Error path (error input → error handling correct)
   - Edge case (boundary values, empty, null)
3. **Run Tests**: `docker compose exec [service] npm test` or equivalent.
4. **Coverage Report**:
   ```
   📊 Test Coverage Report
   ═══════════════════════
   Files Tested:    12/15 (80%)
   Tests Passed:    45/48 (93.7%)
   Tests Failed:    3
   ───────────────────────
   Untested: src/api/payment.ts, src/utils/cache.ts, src/hooks/useAuth.ts
   ```
5. List failed tests with error details.

## 📤 Output
- Test files (theo convention: `*.test.ts`, `*.spec.ts`)
- File: `.agent/memory/test-report.md`

## 🚫 Guard Rails
- DO NOT skip error path tests — must also test failing cases.
- DON'T mock too much — prefer integration tests for API routes.
"""


def skill_validate():
    return r"""
---
name: speckit.validate
description: Implementation Validator - Validate implementation vs overall spec.
role: Validation Oracle
---

## 🎯 Mission
Check whether the ENTIRE implementation meets spec.md or not — final gate before deploying.

## 📥 Input
- All artifacts: spec.md, plan.md, tasks.md
- Source code (implementation)
- `.agent/memory/constitution.md`

## 📋 Protocol
1. **Tasks Completion**: All tasks in tasks.md have `[X]` ?
2. **Success Criteria**: All SCs in spec.md passed?
3. **Build Verification** (MUST run actual command):
   ```bash
   docker compose -f docker-compose.beta.yml build 2>&1 | tail -n 100
   ```
   If failed → ❌ BLOCKED
4. **Runtime Verification** (MUST run actual command):
   ```bash
   docker compose -f docker-compose.beta.yml up -d
   sleep 15
   docker compose -f docker-compose.beta.yml ps
   ```
   - All services must be `Up` (NOT `Restarting` )
   - If `Restarting` → run `docker compose logs <service>` → ❌ BLOCKED
5. **Health Check** (MUST run actual command):
   ```bash
   curl -s http://localhost:<web_port> | head -c 200
   curl -s http://localhost:<api_port>/health
   ```
   All must return 200
6. **Constitution Check**: No rules violated?
7. **Final Verdict**:
   ```
   🏁 VALIDATION REPORT
   ═══════════════════════
   Tasks:        15/15 ✅
   TS Build:     PASS ✅
   Runtime:      PASS ✅ (all services Up)
   Health:       PASS ✅ (all 200)
   Constitution: PASS ✅
   ───────────────────────
   VERDICT: ✅ READY FOR DEPLOY
   ```

## 📤 Output
- File: `.agent/memory/validation-report.md`
- Verdict: ✅ PASS or ❌ FAIL (with blockers list)

## 🚫 Guard Rails
- DO NOT approve if there are unfinished tasks.
- DO NOT approve if build fails.
- DO NOT approve if any service is `Restarting` .
- MUST run actual commands — don't just read the code.
"""


def skill_seo():
    return r"""
---
name: speckit.seo
description: Technical SEO Lead - Optimize Meta Tags, Sitemap, Core Web Vitals, Schema.org.
role: SEO Technical Lead
---

## 🎯 Mission
Ensure all public pages meet Technical SEO standards and are ready for AI Search (GEO).

## 📥 Input
- Source code (pages, layouts, components)
- `.agent/knowledge_base/seo_standards.md` (checklist)

## 📋 Protocol

### Step 1: Audit Technical SEO
- Is each page `<title>` unique, ≤60 characters?
- Each page has `<meta description>` , ≤160 characters?
- Standard heading hierarchy (1 `<h1>` per page, H1→H2→H3)?
- Canonical URLs set for every page?
- Structured Data (JSON-LD) correct schema?

### Step 2: Core Web Vitals
- LCP < 2.5s, INP < 200ms, CLS < 0.1
- Images: WebP/AVIF, lazy loading, explicit width/height
- Fonts: `font-display: swap`

### Step 3: Crawlability
- `robots.txt` does not block CSS/JS
- `sitemap.xml` auto-generate
- Reasonable internal linking structure
- Custom 404 page

### Step 4: Output
Report at `.agent/memory/seo-audit-report.md` :
- Issues: 🔴 Critical / 🟡 Warning / 🟢 Info
- Fix suggestions for each issue
- Total Score (0-100)

## 📤 Output
- File: `.agent/memory/seo-audit-report.md`

## 🔗 Handoffs
- `@speckit.geo` : After Technical SEO passes → switch to GEO audit
- `@speckit.implement` : Fix detected issues
"""


def skill_geo():
    return r"""
---
name: speckit.geo
description: GEO Strategist - Optimized for AI Search (ChatGPT, Gemini, Perplexity).
role: GEO Strategist
---

## 🎯 Mission
Make sure the website is **cited** by AI Search engines in the answer.

## 📥 Input
- Source code (content pages)
- `.agent/knowledge_base/seo_standards.md`

## 📋 Protocol

### Step 1: AI Crawlability
- File `llms.txt` at root domain?
- SSR/SSG for content pages (NO CSR)?
- Full JSON-LD for Article, Product, FAQ?

### Step 2: E-E-A-T Compliance
- **Experience**: Does the content represent real-life experience?
- **Expertise**: Author bio, credentials?
- **Authoritativeness**: Source of citation, data points?
- **Trustworthiness**: HTTPS, privacy policy, contact info?

### Step 3: Content Format for AI
- Short paragraphs (2-3 sentences)
- Bullet points, numbered lists
- Direct answers at the beginning of each section
- FAQ sections "People Also Ask" format
- Fact-dense: Each segment ≥1 data point

### Step 4: Topic Authority
- Topic clusters (pillar + supporting articles)
- Internal linking between articles on the same topic

## 📤 Output
- File: `.agent/memory/geo-audit-report.md`

## 🔗 Handoffs
- `@speckit.content` : Optimize content according to GEO standards
"""


def skill_content():
    return r"""
---
name: speckit.content
description: Content Architect - Heading Structure, Readability, Multimodal, Fact-density.
role: Content Strategist
---

## 🎯 Mission
Ensure website content meets standards for both readers AND AI search engines.

## 📥 Input
- Content pages (articles, products, landing pages)
- `.agent/knowledge_base/seo_standards.md`

## 📋 Protocol

### Step 1: Heading Structure
- Each page has only one `<h1>`
- Hierarchy: H1→H2→H3 (no level jump)
- Heading describes the specific section content

### Step 2: Readability
- Paragraph: Maximum 3-4 sentences
- Bullet points instead of long paragraphs
- Highlight key terms (bold/italic)

### Step 3: Multimodal Content
- Image: `alt` text detailed description
- Video: Transcript or description
- Tables: Responsive, with captions

### Step 4: Fact-density
- Each section ≥1 statistic/data point
- Cite sources when submitting claims
- Quotes from experts when appropriate

## 📤 Output
- File: `.agent/memory/content-guidelines.md`

## 🔗 Handoffs
- `@speckit.seo`: Validate SEO compliance sau khi optimize
"""


def skill_uiux():
    return r"""
---
name: speckit.uiux
description: UI/UX Architect - Definition of Design System Anti-Slop, UI Components, Spacing, Typography, Responsive Patterns.
role: UI/UX Architect
---

## 🎯 Mission
Set up and manage "Pro Max" UI/UX standards for the project, ensuring a premium, professional, unique interface and ABSOLUTELY no "AI slops" (avoid AI's boring default designs).

## 📥 Input
- `.agent/specs/[feature]/spec.md` (contains User Scenarios)
- `.agent/memory/constitution.md` (tech stack constraints)
- Brand guidelines (if any)

## 📋 Protocol

### Phase 0: Brief Inference (Read the Room)
- Analyze projects (SaaS, portfolio, public-sector) to shape vibe.
- Define 3 parameters: `DESIGN_VARIANCE` (1-10), `MOTION_INTENSITY` (1-10), `VISUAL_DENSITY` (1-10).

### Phase 1: Brand Identity & Colors (Anti-Default)
- **Colors**: It is PROHIBITED to use default colors (red, blue, green). It is PROHIBITED to abuse "AI Purple / Blue glow". Use a sophisticated palette like Cold Luxury, Forest, Black & Tan.
- **Typography**: PROHIBITED using `Inter` and Serif as default for anything. Use `Geist` , `Satoshi` , `Cabinet Grotesk` or a sans-serif font of your choice.

### Phase 2: Spacing, Layout & Rhythm
- Limit Hero's top padding (max `pt-24` ). Hero maximum 2 subject lines.
- Apply Anti-Center Bias: Avoid boringly centering the Hero.
- Misuse of "eyebrow" (titles in super small caps) is PROHIBITED. Maximum 1 eyebrow per 3 sections.
- Bento Grid must have rhythm, not leave empty cells, diversify the background of the cells (images, subtle gradients, text).

### Phase 3: Core Components Design
- **Buttons**: Text does not wrap lines on the desktop. Contrast WCAG AA.
- **Cards**: Limit dark shadows on light backgrounds. Do not nest cards within cards.
- **Forms**: Label on input, do not use placeholder instead of label.

### Phase 4: Rich Aesthetics Directive
- Avoid cheap AI gradients. Use realistic Glassmorphism (backdrop-filter + 1px inner border) if the vibe fits.
- Interactive States: Skeletal loading (no generic spinner), tactile feedback when clicking (scale-98).

## 📤 Output
- File: `.agent/knowledge_base/ui_ux_standards.md`
- File: `.agent/specs/[feature]/ui-specs.md` (for each feature)

## 🚫 Guard Rails
- DO NOT use browser default colors.
- DO NOT mix Serif and Sans-serif in the same headline.
- DO NOT use 2 CTAs with the same purpose (same intent) on the same page.
- MANDATORY Mobile-first design priority.
"""


def skill_backend():
    return r"""
---
name: speckit.backend
description: Backend/API Developer - Xay dung API service, business logic, auth, integration theo API standards.
role: Backend Engineer
---

## 🎯 Mission
Build backend/API production: standard REST/GraphQL endpoint, layered business logic, solid auth/authz, stable integration. Match `knowledge_base/api_standards.md` .

## 📥 Input
- `.agent/specs/[feature]/spec.md` + `plan.md` (data model, API contracts)
- `.agent/knowledge_base/api_standards.md`, `data_schema.md`
- `.agent/memory/constitution.md` (Docker-First, ENV, Port 8900-8999)

## 📋 Protocol

### 1. API Layer
- `api_standards.md` compliance: versioning ( `/v1` ), naming, status codes, error envelope consistency.
- Validation of input at the edge (DTO/schema). Reject soon, clear message.
- Standardized pagination/filtering/sorting for list endpoints.

### 2. Architecture (Layered)
- Detach `controller → service → repository` . DO NOT put business logic in the controller.
- Dependency injection, no hard initialization of dependencies.
- Idempotency for sensitive operations (payment, create).

### 3. Auth & Security
- AuthN (JWT/session) + AuthZ (RBAC/policy) in middleware.
- Parameterized query (anti-SQLi). DO NOT concatenate SQL strings.
- Rate limiting + input sanitization cho public endpoints.

### 4. Data & Transaction
- Transaction boundary is clear; rollback on error.
- N+1 query check; index theo `data_schema.md`.

### 5. Observability
- Structured logging (request id), health check endpoint, basic metrics.
- Error handling is centralized, NOT exception swallowing.

## 📤 Output
- API code + contract (OpenAPI/GraphQL schema).
- Update `knowledge_base/api_standards.md` if pattern is added.

## 🚫 Guard Rails
- DO NOT hard-code URL/secret/port → ENV ( `API_*` , `DB_*` ).
- DO NOT return raw error/stacktrace to the client.
- DO NOT bypass authz check on sensitive endpoints.
- DO NOT let public endpoints fail to authenticate without warning.
- Feedback in Vietnamese.
"""


def skill_frontend():
    return r"""
---
name: speckit.frontend
description: Frontend Developer - Xay dung UI components, state management, data fetching, accessibility, performance (Anti-Slop).
role: Frontend Engineer
---

## 🎯 Mission
Realize Design System (from `@speckit.uiux` ) into production code: reusable components, clean state management, optimized data fetching, accessible & smooth animation standard taste-skill.

## 📥 Input
- `.agent/knowledge_base/ui_ux_standards.md` (Design System)
- `.agent/specs/[feature]/spec.md` (UI requirements)
- API contract from `@speckit.backend`
- `.agent/memory/constitution.md` (ENV, Docker-First, Port 8900-8999)

## 📋 Protocol

### 1. Component Architecture
- Small, reusable, single responsibility components. Viewport uses `100dvh` instead of `100vh` to avoid layout jump on mobile.
- According to Design System: spacing/typography/color tokens. Absolutely do not hardcode inline style unless required.

### 2. State & Data
- It is PROHIBITED to use `useState` for continuous values ​​(mouse position, scroll progress). Use `useMotionValue` / `useTransform` of Framer Motion / GSAP.
- Data fetching: MUST have Skeletal loader states (match the final UI shape), do not use generic circular spinner.

### 3. Accessibility (a11y) & UI Rules
- Semantic HTML, ARIA. MANDATORY contrast ratio test (WCAG AA). Button CTA text must be easy to read on the button background.
- Button text must NOT wrap on the desktop. Label button is brief (maximum 3 words).
- Tactile Feedback: add `active:scale-[0.98]` or `-translate-y-[1px]` to create a physical click feeling.

### 4. Motion & Performance
- Animate `transform` and `opacity` (supports hardware acceleration). It is PROHIBITED to animate top/left/width/height continuously.
- REQUIRED respect for `prefers-reduced-motion` if adding complex animations.
- GSAP / Framer Motion must be cleared in time (to avoid memory leaks).

### 5. ENV & Config
- Use `NEXT_PUBLIC_*` for client config. NO hard-code endpoints.

## 📤 Output
- UI component code + basic tests (render/interaction).

## 🚫 Guard Rails
- DO NOT hard-code text/URL/color → use i18n/tokens/ENV.
- DO NOT use 2 CTA buttons for the same purpose on one screen.
- DO NOT violate a11y (missing label, button with white text on light background).
- Feedback in Vietnamese.
"""


def skill_database():
    return r"""
---
name: speckit.database
description: Database Architect - Thiet ke schema, index, migration, query optimization, data integrity.
role: Database Architect
---

## 🎯 Mission
Design and optimize the data layer: reasonable standardized schema, effective indexing, safe migration, fast query, data integrity.

## 📥 Input
- `.agent/knowledge_base/data_schema.md`
- `.agent/specs/[feature]/spec.md` + `plan.md` (data model)
- `.agent/memory/constitution.md`

## 📋 Protocol

### 1. Schema Design
- Normalize (3NF) default; Denormalize intentionally when performance is needed (specify the reason).
- Clear primary/foreign keys, constraints (NOT NULL, UNIQUE, CHECK) in the DB.
- Naming convention is consistent; update `data_schema.md` .

### 2. Indexing & Performance
- Index according to actual query pattern (WHERE/JOIN/ORDER BY).
- Avoid over-indexing (slow writing). Composite index correct column order.
- Detect & process N+1, full table scan.

### 3. Migration (Safe)
- Migration versioned, reversible (up/down).
- Zero-downtime pattern: expand → migrate → contract.
- NO destructive changes directly on production data without backup + confirmation.

### 4. Integrity & Transaction
- Transaction isolation level is appropriate; avoid deadlock.
- Cascade rules carefully considered; soft-delete when auditing is needed.

### 5. Security
- Least-privilege DB user; DO NOT use root/admin for the app.
- Encryption at-rest for sensitive data; mask PII.

## 📤 Output
- Schema DDL + migration files.
- Update `knowledge_base/data_schema.md` (ERD, index list).

## 🚫 Guard Rails
- DO NOT run destructive migration on prod without backup + confirmation.
- NO hard-code credential → ENV ( `DB_*` ).
- DO NOT drop index on FK/hot query columns.
- DO NOT save plaintext passwords (must be hashed).
- Feedback in Vietnamese.
"""


def skill_ios():
    return """---
name: speckit.ios
description: iOS Developer - Native iOS (Swift/SwiftUI/UIKit), lifecycle, App Store compliance, Keychain.
role: iOS Engineer
---

## 🎯 Mission
Build native production iOS apps: Swift + SwiftUI/UIKit, clean architecture, complying with Human Interface Guidelines & App Store Review.

## 📥 Input
- `.agent/specs/[feature]/spec.md`
- `.agent/knowledge_base/ui_ux_standards.md`
- API contract from `@speckit.backend`

## 📋 Protocol

### 1. Architecture
- Swift + SwiftUI (preferred) or UIKit. MVVM / TCA pattern.
- Dependency injection; modularize features.

### 2. Lifecycle & State
- Scene/App lifecycle, background tasks, state restoration.
- `@State` / `@Observable` or Combine for reactive state.

### 3. Platform Integration
- Permission flow (camera, location, notification) correct Info.plist + rationale.
- Push notification (APNs), deep linking (Universal Links).

### 4. Performance & UX
- 60/120fps, avoid main-thread blocking, lazy lists.
- Safe area, Dynamic Type, Dark Mode, accessibility (VoiceOver).

### 5. Security & Compliance
- Tokens in Keychain (NOT UserDefaults).
- App Transport Security (HTTPS only).
- Comply with App Store Review Guidelines + privacy nutrition label.

## 📤 Output
- Swift code + project config (xcconfig/ENV for endpoints).

## 🚫 Guard Rails
- DO NOT hard-code endpoints/keys -> xcconfig/ENV.
- DO NOT save tokens in UserDefaults/plaintext -> Keychain.
- DO NOT block the main thread with I/O operations.
- DO NOT bypass privacy permission rationale.
"""


def skill_android():
    return """---
name: speckit.android
description: Android Developer - Native Android (Kotlin/Jetpack Compose), lifecycle, Play Store compliance, Keystore.
role: Android Engineer
---

## 🎯 Mission
Build native production Android apps: Kotlin + Jetpack Compose, clean architecture, complying with Material Design & Play Store Policy.

## 📥 Input
- `.agent/specs/[feature]/spec.md`
- `.agent/knowledge_base/ui_ux_standards.md`
- API contract from `@speckit.backend`

## 📋 Protocol

### 1. Architecture
- Kotlin + Jetpack Compose (preferred) or View. MVVM / MVI + Clean Architecture pattern.
- Hilt/Koin for DI; modularize features.

### 2. Lifecycle & State
- Activity/Fragment lifecycle, `ViewModel` + `StateFlow`, config change survival.
- WorkManager for background tasks; Navigation Component.

### 3. Platform Integration
- Runtime permission flow correct + rationale.
- Push notification (FCM), deep linking (App Links).

### 4. Performance & UX
- Avoid main-thread blocking (Coroutines/Dispatchers), lazy lists (LazyColumn).
- Material Design 3, Dark theme, accessibility (TalkBack), multi-screen size.

### 5. Security & Compliance
- Tokens in EncryptedSharedPreferences/Keystore.
- Network security config (HTTPS), ProGuard/R8 obfuscation.
- Comply with Play Store Data Safety + latest target SDK.

## 📤 Output
- Kotlin code + Gradle config (BuildConfig/ENV for endpoints).

## 🚫 Guard Rails
- DO NOT hard-code endpoints/keys -> BuildConfig/ENV.
- DO NOT save tokens in plaintext -> Keystore/EncryptedSharedPreferences.
- DO NOT block the main thread -> Coroutines.
- DO NOT bypass runtime permission rationale.
"""


def skill_mobile():
    return """---
name: speckit.mobile
description: Mobile Developer - Cross-platform (React Native/Flutter), offline-first, lifecycle, store compliance.
role: Mobile Engineer
---

## 🎯 Mission
Build cross-platform mobile production apps: React Native/Flutter, 1 codebase running on iOS + Android, offline-first, complying with store guidelines.

## 📥 Input
- `.agent/specs/[feature]/spec.md`
- `.agent/knowledge_base/ui_ux_standards.md`
- API contract from `@speckit.backend`
- Target framework (RN/Flutter; ASK if missing)

## 📋 Protocol

### 1. Framework & Architecture
- Determine RN or Flutter. MVVM/Clean pattern, clear navigation, deep linking.

### 2. Lifecycle & State
- App lifecycle (background/foreground), state restoration.
- State management (Redux/Riverpod/Bloc); correct runtime permission flow.

### 3. Offline-First & Data
- Local storage (SQLite/Realm/AsyncStorage), sync strategy, conflict resolution.
- Cache + retry for unstable network.

### 4. Performance & UX
- 60 FPS scroll, virtualized lists, avoid UI jank.
- Optimize app size, cold start; responsive + safe area.

### 5. Store Compliance & Security
- Comply with App Store / Play Store guidelines.
- Secure storage for tokens (Keychain/Keystore). NO plaintext.

## 📤 Output
- App code (RN/Flutter) + build config.

## 🚫 Guard Rails
- DO NOT hard-code endpoints/keys -> ENV / secure config.
- DO NOT save credentials in plaintext.
- DO NOT block the main/UI thread with I/O operations.
- DO NOT bypass permission rationale.
"""


def skill_data():
    return """---
name: speckit.data
description: Data/ML Engineer - Build data pipelines (ETL/ELT), data quality, ML workflows, orchestration.
role: Data Engineer
---

## 🎯 Mission
Build production data pipelines: reliable ingest → transform → load, guaranteed data quality, reproducible ML workflows.

## 📥 Input
- `.agent/specs/[feature]/spec.md`
- `.agent/knowledge_base/data_schema.md`
- `.agent/memory/constitution.md` (Docker-First, ENV)

## 📋 Protocol

### 1. Pipeline Architecture
- Select model: batch (ETL/ELT) vs streaming. Orchestration (Airflow/Dagster/Prefect).
- Idempotent + re-runnable steps; clear checkpoint/state.
- Partition + incremental load instead of full reload when possible.

### 2. Data Quality
- Schema validation at ingest edge; reject/quarantine bad records.
- Data contract: type, null, range, uniqueness checks.
- Lineage + freshness monitoring.

### 3. Storage & Modeling
- Separate raw / staging / curated layers.
- Modeling according to `data_schema.md`; reasonable partition keys + indexing.

### 4. ML Workflow (if any)
- Separate feature engineering, training, inference.
- Reproducibility: seed, version data + model, track experiments.
- Avoid data leakage (correct train/test split).

### 5. Reliability
- Retry + dead-letter queue for failed steps; alerting.
- Safe backfill strategy.

## 📤 Output
- Pipeline code + orchestration DAG/config.
- Update `knowledge_base/data_schema.md`.

## 🚫 Guard Rails
- DO NOT hard-code connection string/credentials -> ENV (`DB_*`).
- DO NOT full reload when incremental is feasible.
- DO NOT bypass data validation -> avoid silent corruption.
- DO NOT leave unmasked PII in logs/outputs.
"""


def skill_security():
    return r"""
---
name: speckit.security
description: Security Auditor - Audit AppSec theo OWASP, secret scanning, dependency/vuln, threat modeling.
role: Security Auditor
---

## 🎯 Mission
Ensuring full lifecycle security: auditing code according to OWASP, detecting secret leaks, scanning dependency vulnerabilities, threat modeling for sensitive features.

## 📥 Input
- Codebase + `.agent/specs/[feature]/spec.md`
- `.agent/memory/constitution.md` (§2 Security, §3 ENV)
- Dependency manifest (package.json, requirements.txt...)

## 📋 Protocol

### 1. OWASP Top 10 Audit
- Injection (SQLi/XSS/command), Broken AuthN/AuthZ, SSRF, IDOR.
- Insecure deserialization, security misconfiguration.
- Each finding: severity + location + suggested fix.

### 2. Secret & Config
- Scan hard-coded secrets/keys/tokens in code + git history.
- Verify ENV usage according to Constitution §3; `.env` does not commit.
- Check `.dockerignore` , `.gitignore` block sensitive files.

### 3. Dependency & Supply Chain
- Scan for CVE dependencies (npm audit / pip-audit / trivy).
- Detected package typosquatting / unmaintained.
- Pin version (DO NOT use open range for sensitive devices).

### 4. AuthN / AuthZ
- Verify all sensitive endpoints with authz check (anti-IDOR).
- Token storage/expiry/rotation correct; rate limiting.

### 5. Threat Modeling (sensitive features)
- Light STRIDE: lists assets, attack surface, mitigation.
- Production hardening: non-root container, minimum port.

## 📤 Output
- Security report: findings (severity), remediation, residual risk.
- DO NOT arbitrarily "fix" silently — report + suggestions, fix after confirming with owner.

## 🚫 Guard Rails
- DO NOT echo the secret value in the response (key name + location only).
- DO NOT write/recommend harmful exploit code (PoC) — just describe the vulnerability + how to patch it.
- DO NOT ignore serious finding even if it affects progress.
- DO NOT send code/secret to third party endpoint.
- Feedback in Vietnamese.
"""


def skill_gamedev():
    return """---
name: speckit.gamedev
description: Game Developer - Game development specialist (engine, gameplay loop, physics, asset pipeline, netcode, performance).
role: Game Developer
---

## 🎯 Mission
Build production-grade games: stable gameplay loop, performance within frame-budget, compact asset pipeline, scalable architecture. Engine-agnostic (Unity/Unreal/Godot/Phaser/PixiJS/custom).

## 📥 Input
- `.agent/project.json` (project_type = `game`)
- `.agent/memory/constitution.md` (Docker-First, ENV, Port 8900-8999)
- `.agent/specs/[feature]/spec.md` (gameplay requirements)
- Target engine (from spec or ask developer if missing)

## 📋 Protocol

### Phase 1: Engine & Project Setup
- Identify target engine. If missing -> ASK before coding.
- Web game (Phaser/PixiJS/Babylon): run in Docker (Node container), port range 8900-8999.
- Native engine (Unity/Unreal/Godot): build/CI in Docker if feasible; editor running on host is allowed (exception to Docker-First, state reason clearly).
- Structure: `assets/`, `scenes/`, `scripts/` (or `src/`), `prefabs/`, `config/`.

### Phase 2: Core Architecture
- **Game Loop**: separate `update(dt)` (logic) from `render()` (draw). Fixed timestep for physics, variable for render.
- **ECS / Component**: prefer Entity-Component-System or composition over deep inheritance.
- **State Machine**: manage game states (Menu, Playing, Pause, GameOver) using clear FSMs.
- **Event Bus**: communicate between systems via events, avoid tight coupling.

### Phase 3: Performance Budget
- Set **frame budget**: 60 FPS = 16.6ms/frame (mobile/web 30 FPS = 33ms if needed).
- Object pooling for bullets/enemies/particles — DO NOT `new` inside game loop.
- Profiling: measure draw calls, GC spikes, physics cost. Document results in spec.
- Asset budget: texture atlas, compressed audio, lazy-load scene.

### Phase 4: Asset Pipeline
- Isolate asset source (raw) from asset build (optimized).
- Consistent naming convention: `sfx_`, `tex_`, `mdl_`, `anim_`.
- Sprite atlas / texture packing for 2D; LOD for 3D.

### Phase 5: Netcode (if multiplayer)
- Select model: authoritative server vs P2P. Default to **server-authoritative** to prevent cheating.
- Client prediction + server reconciliation for realtime.
- Endpoint/port from ENV (`API_*`), DO NOT hard-code.

### Phase 6: Game Feel & Testing
- Input buffering, coyote time, juice (screen shake, tween) when spec requires.
- Test: unit tests for pure game logic (damage calc, inventory); playtest checklist for gameplay.
- Determinism: core logic must be reproducible (seed RNG).

## 📤 Output
- Game source code based on target engine.
- `config/` for balance values (DO NOT hard-code gameplay balance data into logic).
- Update `.agent/knowledge_base/` with architecture decisions (game loop, ECS, netcode).

## 🚫 Guard Rails
- DO NOT hard-code: gameplay balance, asset paths, server URLs, keys -> use config/ENV.
- DO NOT allocate memory (`new`/instantiate) in hot loop -> use pooling.
- DO NOT block game loop with synchronous I/O -> async load.
- DO NOT trust client in multiplayer -> server validate.
- DO NOT use assets with unknown licenses.
"""


def skill_debug():
    return r"""
---
name: speckit.debug
description: Systematic Debugger - Diagnose problems, find individual root causes, and recommend fix plans.
role: Debugging Specialist
---

## 🎯 Mission
Use scientific methodology to find the root cause of bugs without disturbing the main context of feature development.

## 📋 Protocol

### Phase 1: Symptom Gathering (Symptom collection)
Before starting to code, make it clear:
- **Expected behavior**: What is the expected result?
- **Actual behavior**: What is the actual result that is happening?
- **Error messages**: Specific error logs (paste directly).
- **Reproduction**: Specific steps to reproduce the error (required).

### Phase 2: Isolation & Hypothesis (Isolation & Hypothesis)
- Create file `.agent/debug/[issue-slug].md` to save the investigation log.
- Hypotheses: "Maybe the error lies in function X because of Y".
- Use the commands `grep` , `log` to verify the hypothesis.

### Phase 3: Root Cause Found (Determine the cause)
- Only end the investigation when the specific line of code/configuration causing the error is found.
- Explain **WHY** it fails instead of just saying **IT IS ERROR**.

### Phase 4: Fix Proposal (Proposal to fix errors)
- Do not correct errors directly in this skill.
- The output is either a proposed fix or the creation of a `gap_plan` for `speckit.implement` to execute.

## 🚫 Guard Rails
- NO guessing. Every conclusion must have evidence from logs or code.
- DO NOT further damage existing code during debugging (use Read-only tools mainly).
- MUST create a debug log file to save traces.
"""


def skill_backlog():
    return r"""
---
name: speckit.backlog
description: Backlog Manager - Manage Ideas, Pending Requests and scan TODO/FIXME from codebase.
role: Product Owner Assistant
---

## 🎯 Mission
Organize and prioritize unfulfilled requirements, ensuring no ideas or bugs are missed during long-term development.

## 📋 Protocol

### Phase 1: Idea Scoping (Idea recording)
- When a user makes a request that they don't want to do right away, save it to `.agent/backlog/IDEAS.md` .
- Each idea needs: Description, Priority (Low/Med/High), Status (Pending).

### Phase 2: Automated Todo Scan (Scan source code)
- Use the command `grep` to find the keywords: `TODO:` , `FIXME:` , `HACK:` , `BUG:` .
- Summarize the results found into `.agent/backlog/TECHNICAL_DEBT.md` .

### Phase 3: Backlog Grooming (Backlog filtering)
- Periodically review items in the backlog to convert to `spec.md` when the user is ready to deploy.

## 🚫 Guard Rails
- DO NOT arbitrarily delete the backlog without asking the user.
- DO NOT overflow the context by listing thousands of TODOs. Only list tasks related to the area you are working on.
"""


def skill_roadmap():
    return r"""
---
name: speckit.roadmap
description: Roadmap Strategist - Manage high-level roadmaps (Milestones) and transitions between Phases.
role: Project Manager
---

## 🎯 Mission
Ensure the project is on track according to the long-term vision, managing dependencies between phases (Phases) and milestones (Milestones).

## 📋 Protocol

### Phase 1: Milestone Definition
- Create/Update `.agent/ROADMAP.md` .
- Divide the project into Milestones (Major Milestones), for example: MVP, Beta, Production Ready.
- Each Milestone contains a list of Phases.

### Phase 2: Progress Tracking
- Update the completion status of each Phase based on the results from `speckit.status` .
- Ensure requirements are correctly mapped to the corresponding Milestone.

### Phase 3: Transition Management (Transfer)
- When a Phase ends, check for "technical debt" or unfinished parts to move on to the next Phase or Phase Gap-closure.

## 🚫 Guard Rails
- MUST maintain consistency between the Roadmap and actual implementation.
- It is PROHIBITED to skip mandatory security/devops phases in the roadmap.
"""


def skill_map():
    return r"""
---
name: speckit.map
description: Codebase Mapper - Automatically analyze project structure, draw dependency diagrams, and write architectural documents.
role: Technical Lead
---

## 🎯 Mission
Helps Agents and Users quickly understand the entire "map" of the codebase, especially old projects (Brownfield) or complex projects.

## 📋 Protocol

### Phase 1: Structure Discovery (Scan structure)
- Scan the entire directory with the command `tree` or `ls -R` .
- Identify core Tech Stack (frameworks, databases, libraries).

### Phase 2: Dependency Mapping (Dependency Diagram)
- Analyze the `import` or `require` commands to find dependencies between modules.
- Save the results to `.agent/codebase/STRUCTURE.md` .

### Phase 3: Integration Inventory (Integration Inventory)
- List 3rd party services (external API, DB connection).
- Save to `.agent/codebase/INTEGRATIONS.md` .

## 📤 Output Artifacts
- `.agent/codebase/ARCHITECTURE.md` : Architecture overview.
- `.agent/codebase/CONVENTIONS.md` : Code conventions in use.

## 🚫 Guard Rails
- DO NOT read the contents of all files at the same time to avoid context overflow. Prioritize reading headers and exports.
- MUST update the map after every major refactor.
"""


def skill_uat():
    return r"""
---
name: speckit.uat
description: UAT Analyzer - Analyze manual acceptance results and process gaps from the User.
role: Quality Assurance
---

## 🎯 Mission
Bridging the actual user experience and code logic, ensuring features run as customers expect.

## 📋 Protocol

### Phase 1: UAT Intake (Acceptance)
- Collect manual user feedback after each Phase.
- Recorded in `.agent/verification/[phase]-UAT.md` .

### Phase 2: Gap Analysis (Gap Analysis)
- Compare the actual results User reports with the original Spec.md.
- Error classification: UI Bug, Logic Bug, or New Requirement.

### Phase 3: Restoration Plan (Patch plan)
- Automatically generate a Tasks list to patch the "Gaps" just found.
- Forwarding for `speckit.implement` processes as `--gaps-only` .

## 🚫 Guard Rails
- There MUST be a clear distinction between "Bug" and "New Feature Requested".
- It is PROHIBITED to mark Phase completed if the User has not yet Approve the core UAT criteria.
"""


def skill_wordpress():
    return r"""
---
name: speckit.wordpress
description: WordPress Master Architect - Expert in developing core-compliant Themes, Gutenberg Blocks (apiVersion 3), Plugins, Interactivity API, REST API endpoints, WP-CLI automation, and Performance profiling/database optimization.
role: WordPress Master Expert
---

## 🎯 Mission
Build industrial-grade, secure, performant, and highly interactive WordPress products (Themes/Plugins/Blocks), strictly adhering to official core developer guidelines and Spec-Driven Development.

## 📋 Protocol

### 1. Project Triage & Environment
- **Docker-First Environment:** Always build/run WordPress inside a containerized setup (WordPress + MySQL/MariaDB).
- **Core Triage:** Detect project type (theme vs. plugin vs. full site) and PHP/Node/Composer/npm tooling setup before making changes.
- **Theme Pathing:** Place theme code under `wp-content/themes/[theme-slug]/`.
- **Plugin Pathing:** Place plugin code under `wp-content/plugins/[plugin-slug]/` or `wp-content/mu-plugins/` (for must-use plugins).

### 2. Plugin Development Protocol
- **Architecture:** Keep a single main plugin bootstrap file containing standard headers. Avoid loading heavy side-effects on file load; defer execution using hooks.
- **Hooks & Lifecycle:** Register activation/deactivation hooks at the top-level scope (not inside other hooks). Implement safe uninstallation using `uninstall.php` or `register_uninstall_hook`.
- **Admin UI & Settings:** Prefer the official Settings API (`register_setting`, `add_settings_section`, `add_settings_field`) with proper `sanitize_callback` for options storage.

### 3. Block (Gutenberg) Development Protocol
- **Metadata-Driven:** Define blocks using `block.json` with `apiVersion: 3` (WordPress 6.9+ standard) to ensure correct block iframe behavior.
- **Edit/Save/Render Patterns:**
  - In the Editor: Wrap component markup with `useBlockProps()`.
  - Static blocks (markup saved in database): Use `useBlockProps.save()` in `save()`.
  - Dynamic blocks (server-rendered): Set `"render": "file:./render.php"` in `block.json` (or use PHP `render_callback`) and keep `save()` returning `null`. Use `get_block_wrapper_attributes()` in PHP.
- **Block Composition:** Use `useInnerBlocksProps()` for container-like blocks.
- **Deprecations & Migrations:** If modifying saved markup/attributes, add a `deprecated` array (newest to oldest) in the client script to avoid "Invalid block" errors.

### 4. Block Themes & theme.json Protocol
- **Global Settings & Styles:** Use `theme.json` to define typography scales, color presets, layout constraints, and per-block custom styles.
- **Templates & Template Parts:** Place HTML templates under `templates/` and parts under `parts/`. Do not nest parts in subdirectories.
- **Style Variations:** Define style presets in JSON files inside `styles/`. Remember that once a user selects a variation in the editor, it is saved in the database, overriding file-level changes.
- **Patterns:** Prefer theme-registered patterns located under `patterns/*.php` for modular reuse.

### 5. Interactivity API & Hydration Protocol
- **Server-Side Rendering (SSR) first:** Always pre-render interactive markup on the server to prevent Layout Shift (CLS) and ensure SEO indexability.
- **Directive Processing:** Enable server-side directive parsing by declaring `"interactivity": true` inside the block's `"supports"` config.
- **State Initialization:**
  - Global state (PHP): Define initial state using `wp_interactivity_state('pluginNamespace', $initialStateArray)`.
  - Local context (PHP): Output context wrapper attributes using `wp_interactivity_data_wp_context($contextArray)`.
- **Directives:** Use `data-wp-interactive`, `data-wp-context`, `data-wp-bind`, `data-wp-on`, and custom store stores. **Avoid the deprecated `data-wp-ignore` directive**.

### 6. REST API & Endpoint Registration Protocol
- **Route Registration:** Register custom REST routes during the `rest_api_init` hook using `register_rest_route()`.
- **Namespace:** Use a unique namespace format like `vendor/v1` (avoid `wp/v2` unless core).
- **Authentication & Validation:**
  - Always enforce a `permission_callback` (use `__return_true` for public endpoints).
  - Perform authorization checks via WordPress user capabilities (e.g. `current_user_can('manage_options')`).
  - Validate request parameters via request schema/args configurations using `validate_callback` and `sanitize_callback`.
- **Response:** Enclose responses inside `rest_ensure_response()` or `WP_REST_Response`. Use `WP_Error` with explicit HTTP status codes for errors.

### 7. WP-CLI Operations & Scripting
- **Ops Safety:** Perform database exports/backups before executing destructive commands.
- **Site Targeting:** Enforce `--path=<wp-path>` and, for multisites, `--url=<site-url>` to target correct environments.
- **URL Migration:** Use `wp search-replace --dry-run` to inspect changes before running URL replacements on serialized data.
- **Automation:** Build repeatable operations scripts using `wp-cli.yml` configuration defaults.

### 8. Performance Profiling & Database Optimization
- **Database & Queries:** Reduce total queries, avoid N+1 query patterns. Prefer `WP_Query` or `get_posts` over raw SQL. Use `$wpdb->prepare()` if raw SQL is necessary.
- **Autoload Bloat:** Audit and optimize autoloaded options. Large data arrays should be converted to transients or standard non-autoloaded options.
- **Caching:** Integrate persistent object caching (`wp_cache_set`, `wp_cache_get`) for heavy database operations.
- **Remote API calls:** Enforce HTTP request timeouts (`wp_remote_get`, `wp_remote_post`) and cache the results to prevent render blocking.

## 🚫 Guard Rails (Security & Anti-patterns)
- **Sanitize & Escape:** Validate/sanitize input early, escape output late (use `esc_html`, `esc_attr`, `esc_url`, `wp_kses`).
- **CSRF Prevention:** Implement and verify nonces on all admin actions, AJAX hooks, and REST requests.
- **Core Hook Safety:** Do not modify Core files or third-party plugin codes directly; always utilize actions, filters, or child themes.
- **Plugin Sourcing:** Strictly forbid using cracked, nulled, or unverified plugins.
"""



def skill_3d():
    return r"""
---
name: speckit.3d
description: 3D Specialist - 3D modeling, WebGL/Three.js/React Three Fiber, Unity/Unreal Engine 3D integration, shaders, optimization.
role: 3D Architect & Developer
---

## 🎯 Mission
Provide standards, best practices, and implementation guidelines for 3D graphics development, rendering, assets pipeline, and engine integration (Web 3D and native Game engines).

## 📥 Input
- `.agent/memory/constitution.md` (principles, tech stack)
- Spec & Plan files (e.g., `spec.md`, `plan.md`)
- Assets catalog and directories (e.g., glTF, FBX, OBJ, textures)

## 📋 Protocol

### Giai đoạn 1: Assets Pipeline & Setup
- **WebGL/Web 3D (Three.js / React Three Fiber):**
  - Sử dụng định dạng **glTF/glb** làm định dạng mô hình chuẩn.
  - Phải nén file mô hình 3D bằng **Draco compression** hoặc Meshopt trước khi sử dụng trong ứng dụng web (giới hạn dung lượng model < 5MB).
  - Tải tài nguyên bất đồng bộ (Async Loading) kèm theo Loading Screen/Progress Bar trực quan.
  - Tách biệt thư mục chứa tài nguyên 3D (ví dụ: `public/assets/3d/` hoặc `assets/models/`).

- **Game Engines (Unity / Unreal / Godot):**
  - Quản lý asset khoa học: Thư mục riêng cho `Prefabs/`, `Models/`, `Materials/`, `Textures/`, `Shaders/`.
  - Thiết lập Prefab Variants thay vì tạo bản sao Prefab độc lập.

### Giai đoạn 2: Phát triển & Logic
- **Web 3D:**
  - Viết code sạch, quản lý vòng đời (Lifecycle Management) của Scene, Camera, Renderer và Light.
  - Giải phóng bộ nhớ (Dispose) hoàn toàn cho Geometries, Materials, Textures khi unmount/destroy component để tránh memory leak.
  - Sử dụng `requestAnimationFrame` thông qua loop của Three.js hoặc custom tick loop.

- **Game Engines (Unity / Unreal / Godot):**
  - Sử dụng mô hình ECS (Entity Component System) hoặc Object-Component sạch sẽ.
  - Tránh sử dụng hàm `Find()` hoặc `GetComponent()` trong các vòng lặp Update.
  - Quản lý State bằng State Machine rõ ràng.

### Giai đoạn 3: Shaders & Hiệu ứng hình ảnh
- Viết shader custom (GLSL/HLSL) tối ưu, hạn chế tính toán phức tạp trong Fragment Shader.
- Tận dụng Vertex Shader cho các tính toán di chuyển/vật lý đơn giản.

### Giai đoạn 4: Tối ưu hiệu năng (Performance Optimization)
- **WebGL/Web 3D:**
  - Hạn chế số lượng Draw Calls bằng cách gộp mesh (InstancedMesh) hoặc sử dụng Texture Atlases.
  - Bật/tắt Shadow Map một cách chọn lọc, giới hạn resolution của shadow.
  - Sử dụng **LOD (Level of Detail)** cho các mô hình ở xa.
  - Giảm thiểu tính toán va chạm vật lý (Physics) trên CPU bằng cách sử dụng bounding boxes/spheres đơn giản.

- **Game Engines:**
  - Bật Occlusion Culling và Frustum Culling.
  - Sử dụng GPU Instancing cho các vật thể lặp lại (cỏ, cây, đá).

## 🚫 Guard Rails (Không được làm)
- KHÔNG load các mô hình chưa được tối ưu hóa trực tiếp lên Web (tránh làm đơ trình duyệt).
- KHÔNG tạo Material hoặc Texture mới trong mỗi frame render.
- KHÔNG hardcode đường dẫn asset 3D.
- KHÔNG chạy render loop liên tục khi Scene không có sự thay đổi (sử dụng render on demand nếu Scene tĩnh).
"""


# =============================================================================
# TEMPLATES FOR NEW SKILLS
# =============================================================================

def skill_k8s_manifest_generator():
    return r"""---
name: k8s-manifest-generator
description: Create production-ready Kubernetes manifests for Deployments, Services, ConfigMaps, and Secrets.
role: Kubernetes Architect
---

## 🎯 Mission
Create production-ready Kubernetes manifests following best practices and security standards.

## 📋 Protocol
1. Clarify goals, constraints, and required inputs.
2. Define Deployment, Service, ConfigMap, and Secret resources.
3. Apply resource limits, health checks, security contexts, and naming conventions.
4. Ensure manifests are designed for multi-environment deployments.
5. Provide actionable steps and verification.

## 🚫 Guard Rails
- DO NOT generate insecure configurations (e.g. running containers as root).
- DO NOT hard-code sensitive credentials in manifests (always use Secrets/ConfigMaps).
"""


def skill_async_python_patterns():
    return r"""---
name: async-python-patterns
description: Master Python asyncio, concurrent programming, and async/await patterns for high-performance applications.
role: Async Python Expert
---

## 🎯 Mission
Implement asynchronous Python applications using asyncio and concurrent patterns.

## 📋 Protocol
1. Clarify workload characteristics (I/O vs CPU), targets, and runtime constraints.
2. Pick concurrency patterns (tasks, gather, queues, pools) with cancellation rules.
3. Add timeouts, backpressure, and structured error handling.
4. Include testing and debugging guidance for async code paths.

## 🚫 Guard Rails
- DO NOT block the event loop with synchronous, long-running I/O or heavy CPU work (use run_in_executor).
- DO NOT use async when a simple synchronous script is sufficient.
"""


def skill_backend_architect():
    return r"""---
name: backend-architect
description: Expert backend architect specializing in API design, microservices, and distributed systems.
role: Backend Architect
---

## 🎯 Mission
Design scalable, resilient, and maintainable backend systems, APIs, and microservices boundaries.

## 📋 Protocol
1. Capture domain context, use cases, and non-functional requirements (scale, latency, consistency).
2. Design API contracts (REST, GraphQL, gRPC) with clear specs (OpenAPI/GraphQL schemas).
3. Choose architecture patterns, database boundaries, and inter-service communication (sync vs async).
4. Build in resilience (circuit breakers, retries, timeouts) and observability (logging, metrics, tracing).
5. Document architectural decisions (ADRs) with clear trade-offs.

## 🚫 Guard Rails
- DO NOT overcomplicate with microservices when a modular monolith is sufficient.
- DO NOT hard-code service URLs or secrets (always use env vars or service discovery).
- Defers database schema design to database-architect (works after data layer is designed).
"""


def skill_security_auditor():
    return r"""---
name: security-auditor
description: Expert security auditor specializing in DevSecOps, cybersecurity, and compliance frameworks.
role: Security Auditor
---

## 🎯 Mission
Perform security audits, threat modeling, and secure software development lifecycle (SDLC) checks.

## 📋 Protocol
1. Confirm scope, assets, and compliance requirements (GDPR, SOC2, PCI-DSS, etc.).
2. Review architecture, perform threat modeling (STRIDE), and check secure coding controls.
3. Implement DevSecOps automated scans (SAST, DAST, dependency scanning) in CI/CD pipelines.
4. Review authentication/authorization protocols (OAuth2, OIDC, JWT security, zero-trust).
5. Prioritize findings by severity and business impact, providing clear remediation steps.

## 🚫 Guard Rails
- DO NOT run intrusive security tests on production environments without explicit written approval.
- DO NOT expose sensitive data, passwords, or credentials in reports.
"""


def skill_full_stack_orchestration():
    return r"""---
name: full-stack-orchestration-full-stack-feature
description: Orchestrate full-stack feature development across backend, frontend, and infrastructure layers.
role: Orchestration Engineer
---

## 🎯 Mission
Coordinate multi-agent and full-stack feature development with an API-first approach.

## 📋 Protocol
1. **Architecture & Design**:
   - Database: Design schema & migrations.
   - Backend: Define API contracts (OpenAPI/GraphQL) & authentication.
   - Frontend: Design component hierarchy, state, and routing.
2. **Implementation**:
   - Build backend service endpoints with validation and observability.
   - Build frontend components (React/Next.js), integrating APIs and state management.
   - Deploy & optimize database indexing.
3. **Integration & Testing**:
   - Perform API contract testing (Pact/Dredd).
   - Implement E2E user-journey tests (Playwright/Cypress).
   - Run security audit & hardening.
4. **Operations**:
   - Setup Docker, Kubernetes, CI/CD pipelines, and feature flags.
   - Configure observability (OpenTelemetry, Prometheus, Grafana).

## 🚫 Guard Rails
- DO NOT skip API contract validation before building frontend/backend features.
- Ensure all services use correlation IDs for distributed tracing.
"""


def skill_conductor_implement():
    return r"""---
name: conductor-implement
description: Execute tasks from a track's implementation plan following TDD workflow.
role: Conductor Specialist
---

## 🎯 Mission
Execute track implementation tasks step-by-step according to `conductor/workflow.md`.

## 📋 Protocol
1. **Pre-flight Check**: Verify Conductor files exist (`product.md`, `workflow.md`, `tracks.md`).
2. **Track Selection**: Load track context, specs, plan, and update status to in-progress (`[~]`).
3. **Task Loop**:
   - Select next incomplete task.
   - **TDD Workflow**: Write failing test (Red), implement code (Green), refactor (Refactor).
   - Commit task changes: `git commit -m "{prefix}: {task} ({trackId})"`.
   - Update `plan.md` to `[x]` and commit the plan change.
4. **Phase Check**: Run phase verification and wait for user approval before next phase.
5. **Completion**: Run final verification, update track status to complete, sync docs.

## 🚫 Guard Rails
- NEVER skip verification checkpoints. Wait for user approval between phases.
- STOP immediately on any tool, test, or git failure. Do not auto-continue.
"""


# =============================================================================
# SKILL TEMPLATE MAP — Complete mapping for all 44 skills
# =============================================================================
SKILL_TEMPLATE_MAP = {
    "speckit.identity": skill_identity,
    "speckit.devops": skill_devops,
    "speckit.analyze": skill_analyze,
    "speckit.checker": skill_checker,
    "speckit.checklist": skill_checklist,
    "speckit.clarify": skill_clarify,
    "speckit.constitution": skill_constitution,
    "speckit.diff": skill_diff,
    "speckit.implement": skill_implement,
    "speckit.migrate": skill_migrate,
    "speckit.plan": skill_plan,
    "speckit.quizme": skill_quizme,
    "speckit.reviewer": skill_reviewer,
    "speckit.specify": skill_specify,
    "speckit.status": skill_status,
    "speckit.tasks": skill_tasks,
    "speckit.taskstoissues": skill_taskstoissues,
    "speckit.tester": skill_tester,
    "speckit.validate": skill_validate,
    "speckit.seo": skill_seo,
    "speckit.geo": skill_geo,
    "speckit.content": skill_content,
    "speckit.uiux": skill_uiux,
    # --- Multi-Agent builders (v2 attribute-based) ---
    "speckit.backend": skill_backend,
    "speckit.frontend": skill_frontend,
    "speckit.database": skill_database,
    "speckit.ios": skill_ios,
    "speckit.android": skill_android,
    "speckit.mobile": skill_mobile,
    "speckit.data": skill_data,
    "speckit.security": skill_security,
    "speckit.gamedev": skill_gamedev,
    # --- Process/utility skills (detailed, replacing fallback) ---
    "speckit.debug": skill_debug,
    "speckit.backlog": skill_backlog,
    "speckit.roadmap": skill_roadmap,
    "speckit.map": skill_map,
    "speckit.uat": skill_uat,
    "speckit.wordpress": skill_wordpress,
    "speckit.3d": skill_3d,
    # --- New skills from external vault ---
    "k8s-manifest-generator": skill_k8s_manifest_generator,
    "async-python-patterns": skill_async_python_patterns,
    "backend-architect": skill_backend_architect,
    "security-auditor": skill_security_auditor,
    "full-stack-orchestration-full-stack-feature": skill_full_stack_orchestration,
    "conductor-implement": skill_conductor_implement,
}


