"""
Workflow Templates - Detailed content for 31 workflows.
Each workflow has: Pre-conditions, Steps with gate checks, Success criteria.
"""


def wf_00_all():
    return r"""
---
description: Full Pipeline (Specify → Clarify → Plan → Tasks → Analyze)
---

# 🚀 Full Pipeline

## Steps

1. **@speckit.map** — (IF old project) Scans the structure and understands the current codebase.
   - Output: `.agent/codebase/` docs.

2. **@speckit.specify** — Generates spec.md from feature description.
   - Output: `.agent/specs/[feature]/spec.md`.

3. **@speckit.clarify** — Resolve ambiguity and close User Scenarios.

4. **@speckit.roadmap** — Updated `.agent/ROADMAP.md` with new Phase/Milestone.

5. **@speckit.plan** — Create architecture (Goal-Backward).
   - Output: plan.md, must_haves.

6. **@speckit.tasks** — Breakdown to atomic tasks (Task Anatomy).
   - Output: tasks.md.

7. **@speckit.analyze** — 360 degree consistency check.

## Success Criteria
- ✅ spec.md, plan.md, tasks.md exist and are consistent
- ✅ Does not violate the Constitution
"""


def wf_01_constitution():
    return r"""
---
description: Establish/update Constitution (Source of Law)
---

# 📜 Constitution Setup

## Pre-conditions
- `.agent/` directory already exists (run `bro-skills init` first)

## Steps

1. **@speckit.constitution** — Collect information from developers:
   - Tech stack (language, framework, DB)
   - Docker port range (default 8900-8999)
   - Coding principles (VD: No hardcode, Docker-first)
   - Security requirements
2. Create/update `.agent/memory/constitution.md`
3. Validate: Each section has ≥1 specific rule

## Success Criteria
- ✅ `constitution.md` exists with ≥4 sections
- ✅ Each rule is testable (not generic)
"""


def wf_02_specify():
    return r"""
---
description: Create Feature Specification (spec.md)
---

# 📝 Feature Specification

## Pre-conditions
- `.agent/memory/constitution.md` exists

## Steps

1. Developers describe features in natural language
2. **@speckit.specify** — Parse description → create standardized spec.md
3. Review output: spec.md must have Overview, User Scenarios, Requirements, Success Criteria

## Success Criteria
- ✅ spec.md has ≥1 User Scenario
- ✅ Each scenario has Actor + Action + Value
- ✅ Success Criteria is testable
"""


def wf_03_clarify():
    return r"""
---
description: Resolve ambiguity in Specification
---

# 🔍 Ambiguity Resolution

## Pre-conditions
- `.agent/specs/[feature]/spec.md` exists

## Steps

1. **@speckit.clarify** — Scan spec.md for ambiguity
2. Ask the developer up to 3 CRITICAL questions (table A/B/C options)
3. Auto-fix MINOR issues
4. Update spec.md with `[CLARIFIED]` markers

## Success Criteria
- ✅ No more vague language in spec.md
- ✅ All boundary conditions defined
"""


def wf_04_plan():
    return r"""
---
description: Create Technical Plan (plan.md)
---

# 🏗️ Technical Planning

## Steps

1. **@speckit.plan** — Switch spec (WHAT) → plan (HOW):
   - Phase 0: Research unknowns.
   - Phase 1: Data model.
   - Phase 2: API contracts.
   - Phase 3: Architecture.
   - Phase 4: **Must-Haves (Goal-Backward)**.
2. **GATE**: Compare plan vs constitution.
"""


def wf_05_tasks():
    return r"""
---
description: Create Task Breakdown (tasks.md)
---

# 📋 Task Breakdown

## Pre-conditions
- `.agent/specs/[feature]/plan.md` exists
- `.agent/specs/[feature]/spec.md` exists

## Steps

1. **@speckit.tasks** — Breakdown plan → atomic tasks
2. Verify:
   - Each task ≤15 minutes
   - Each task has a file path
   - Dependency ordering is correct
   - Phase structure is correct (Setup → Foundation → Features → Polish)

## Success Criteria
- ✅ tasks.md has ≥1 phases
- ✅ Each task format: `- [ ] T001 [P] [USx] Description affecting path/file`
- ✅ No task affects >3 files
"""


def wf_06_analyze():
    return r"""
---
description: Analyze consistency between artifacts
---

# 🔬 Consistency Analysis

## Pre-conditions
- spec.md, plan.md, tasks.md exist

## Steps

1. **@speckit.analyze** — Cross-check 3 artifacts:
   - Each User Scenario → has tasks?
   - Each data model → has tasks?
   - Conflicts between plan and constitution?
2. Output: Gap Analysis table + Coverage Score

## Success Criteria
- ✅ Coverage Score ≥ 90%
- ✅ No CRITICAL gaps
"""


def wf_07_implement():
    return r"""
---
description: Deploy code according to tasks (Anti-Regression)
---

# 🛠️ Implementation

## Steps

For EACH task `- [ ]` in tasks.md:

1. **@speckit.implement** — Implementation of IRONCLAD Protocols:
   - P1: Blast Radius Analysis.
   - P2: Strategy Selection.
   - P3: TDD (Repro fail first).
   - P4: Context Anchoring.
   - P5: Build Gate (tsc/build).
   - P6: **Deviation Rules** (Auto-fix bugs/missing).
2. Mark `- [X]` when task pass **AND build gate pass**.
3. **Auto-Map**: When ALL tasks are completed, automatically run **@speckit.map** to update the architecture document.
"""


def wf_08_checker():
    return r"""
---
description: Run Static Analysis
---

# 🔍 Static Analysis

## Pre-conditions
- Implemented code (≥1 task completed)

## Steps

// turbo-all

1. **TypeScript Compile Check** (CRITICAL):
   ```bash
   docker compose build 2>&1 | grep -iE "error|fail|TS[0-9]"
   ```
   Or:
   ```bash
   docker compose exec topdeli-web npx tsc --noEmit
   docker compose exec topdeli-admin npx tsc --noEmit
   docker compose exec topdeli-api npx tsc --noEmit
   ```

2. **Dockerfile Integrity** — Check COPY paths:
   - Verify any COPY directories exist (especially `public/` )
   - Verify CMD entrypoint matches build output structure
   - Verify does NOT have volume mount `.:/app` in production/beta compose

3. **ENV Compliance** — Scan hard-coded values:
   ```bash
   grep -rn "http://localhost\|http://127.0.0.1" apps/*/src/ --include="*.ts" --include="*.tsx" | grep -v "node_modules"
   grep -rn '|| "' apps/*/src/ --include="*.ts" --include="*.tsx" | grep -v "node_modules"
   ```

4. **Build-time Safety** — Verify SSG pages:
   ```bash
   grep -rn "await api\.\|await fetchApi" apps/*/src/app/sitemap.ts apps/*/src/app/*/page.tsx
   ```
   Each result MUST be in a try-catch block.

5. **Monorepo Type Contract** — @speckit.checker:
   - Cross-reference shared type exports vs component usage
   - Verify shared package exports match actual file structure

6. **Security Scan**:
   - Find `eval()` , `dangerouslySetInnerHTML` , exposed secrets
   - Docker compliance: ports trong range 8900-8999

7. **Output Report** → `.agent/memory/checker-report.md`

## Success Criteria
- ✅ TypeScript compile: 0 errors
- ✅ Docker build: complete success
- ✅ 0 issues CRITICAL (🔴)
- ✅ Report file existence
- ❌ If there are any 🔴 CRITICAL → BLOCK deploy
"""


def wf_09_tester():
    return r"""
---
description: Run Tests & Coverage
---

# 🧪 Testing & Coverage

## Pre-conditions
- Implemented code

## Steps

1. **@speckit.tester** — Create test plan → write tests → run → report
2. Target: Coverage ≥ 80%

## Success Criteria
- ✅ All tests pass
- ✅ Coverage ≥ 80%
- ✅ test-report.md exists
"""


def wf_10_reviewer():
    return r"""
---
description: Code Review
---

# 👀 Code Review

## Pre-conditions
- Code implemented + tests passed

## Steps

1. **@speckit.reviewer** — Review code:
   - Spec compliance, error handling, security, performance
2. Verdict: APPROVE or REQUEST CHANGES

## Success Criteria
- ✅ Verdict: APPROVE
- ✅ All CRITICAL findings have been fixed
"""


def wf_11_validate():
    return r"""
---
description: Validate Implementation vs Spec
---

# ✅ Final Validation

## Pre-conditions
- All tasks completed, tests passed, review approved

## Steps

// turbo-all

1. **Tasks Completion Check**:
   - Read `tasks.md` → every task must be `[X]`
   - If there is `[ ]` or `[/]` → ❌ BLOCKED

2. **TypeScript Build Gate** (CRITICAL):
   ```bash
   docker compose -f docker-compose.beta.yml build 2>&1 | tail -n 100
   ```
   If build fails → ❌ BLOCKED, list errors

3. **Runtime Verification**:
   ```bash
   docker compose -f docker-compose.beta.yml up -d
   sleep 15
   docker compose -f docker-compose.beta.yml ps
   ```
   - All services must be `Up` (NOT `Restarting` )
   - If `Restarting` → run `docker compose logs <service>` → ❌ BLOCKED

4. **Health Check**:
   ```bash
   curl -s http://localhost:<web_port> | head -c 200  # Public Web
   curl -s http://localhost:<admin_port> | head -c 200  # Admin Panel
   curl -s http://localhost:<api_port>/health  # API
   ```
   All must return 200

5. **Constitution Compliance**:
   - Verify Monorepo Rules (type contracts)
   - Verify Docker Rules (no volume shadowing in prod)
   - Verify Build-time Safety (try-catch trong SSG)

6. **Final Verdict**:
   ```
   🏁 VALIDATION REPORT
   ═══════════════════════
   Tasks:        N/N ✅
   TS Build:     PASS ✅
   Runtime:      PASS ✅ (all services Up)
   Health:       PASS ✅ (all 200)
   Constitution: PASS ✅
   ───────────────────────
   VERDICT: ✅ READY FOR DEPLOY
   ```

## Success Criteria
- ✅ Verdict: READY FOR DEPLOY
- ❌ If ANY step FAIL → BLOCKED (not deployed)
"""


def wf_12_seo():
    return r"""
---
description: Technical SEO Audit & Optimization
---

# 🔍 SEO Audit

## Pre-conditions
- Public pages implemented
- `.agent/knowledge_base/seo_standards.md` exists

## Steps

1. **@speckit.seo** — Audit:
   - Meta tags, headings, canonical, structured data
   - Core Web Vitals, crawlability
2. Output: Score 0-100 + issues list
3. If score < 80 → fix issues → re-audit

## Success Criteria
- ✅ SEO Score ≥ 80
- ✅ 0 CRITICAL issues
"""


def wf_13_geo():
    return r"""
---
description: GEO - Optimized for AI Search (ChatGPT, Gemini, Perplexity)
---

# 🤖 GEO Audit

## Pre-conditions
- SEO Audit passed (score ≥ 80)

## Steps

1. **@speckit.geo** — Audit:
   - AI crawlability (llms.txt, SSR, JSON-LD)
   - E-E-A-T compliance
   - Content format, topic authority
2. Output: GEO report

## Success Criteria
- ✅ llms.txt exists
- ✅ JSON-LD for all content pages
- ✅ E-E-A-T signals present
"""


def wf_identity():
    return r"""
---
description: Create/update Master Identity for AI Agent
---

# 🆔 Identity Setup

## Pre-conditions
- `.agent/project.json` exists (run `bro-skills init` first)
- `.agent/memory/constitution.md` exists (recommended)

## Steps

1. **@speckit.identity** — Collect information:
   - Read `project.json` → project type, name
   - Read `constitution.md` → tech stack, principles
   - Scan codebase → existing patterns, conventions
2. Create/update `.agent/identity/master-identity.md` :
   - Persona + Core Capabilities
   - Soul (Core Beliefs): "bro-skills First", "Docker is the Law"
   - Project Context (auto-detected)
3. If `web_public` / `fullstack` → add SEO & GEO Awareness section

## Success Criteria
- ✅ `master-identity.md` exists
- ✅ Persona closely tied to the project domain (not generic)
- ✅ Core Beliefs includes mandatory items
"""


def wf_devops():
    return r"""
---
description: Docker Infrastructure & Port Allocation (ENV-first)
---

# 🐳 DevOps Infrastructure Setup

## Pre-conditions
- `.agent/memory/constitution.md` exists
- Docker Desktop (local) or Docker Engine (server) installed

## Steps

// turbo-all

### Step 1: Determine Environment
- Detect environment: **local** / **staging** / **beta** / **production**
- Read `constitution.md` → port range (default 8900-8999)

### Step 2: Port Allocation (ENV-first) ⭐

**Port Rules — ALWAYS configure via ENV:**
- Port MUST be declared in `.env` (local) or server ENV (prod)
- `docker-compose.yml` reads port from ENV vars ( `${PUBLIC_PORT}` , `${ADMIN_PORT}` , `${API_PORT}` )
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
# If there are containers → Docker is already running → SKIP port scan
# If empty/error → Docker is not running → RUN port scan
```

**Port scan when needed:**
```text
Scan TCP bind availability on 127.0.0.1 for ports 8900-8999.
```
- Pattern: Public FE `N` → Admin FE `N+1` → Backend API `N+2`
- Always write in `.env` :
  ```env
  PUBLIC_PORT=8920
  ADMIN_PORT=8921
  API_PORT=8922
  ```

### Step 3: Docker Compose (Local)
- Create/update `docker-compose.yml` :
  - Ports read from ENV: `"${PUBLIC_PORT:-8920}:3000"`
  - Volume mounts cho hot-reload
  - Named volumes cho `node_modules`
  - Health checks for each service

### Step 4: Docker Compose (Production/Staging/Beta)
- Create/update `docker-compose.prod.yml` / `docker-compose.beta.yml` :
  - Multi-stage builds (builder → runner)
  - `USER node` or `USER appuser` (DO NOT run as root)
  - Remove devDependencies in the final image
  - Alpine/Slim base images
  - Ports read from ENV (NO hard-code)

### Step 5: Security Checklist
- `.dockerignore`: block `.env`, `.git`, `node_modules`
- DO NOT hard-code secrets in Dockerfile
- Only EXPOSE ports are needed

### Step 6: Documentation
- Update `.agent/knowledge_base/infrastructure.md`
- Update `.env.example` with all port vars

## Success Criteria
- ✅ Ports configured via ENV (no hard-code)
- ✅ `docker-compose.yml` works locally
- ✅ `docker-compose.prod.yml` complies with security checklist
- ✅ `.dockerignore` exists and is complete
- ✅ `.env.example` document all port vars
- ✅ `infrastructure.md` updated

## 🚫 Guard Rails
- DO NOT use ports outside the 8900-8999 range
- DO NOT hard-code port number — ALWAYS ENV vars
- DO NOT run `docker compose down -v` on production
- DO NOT hard-code credentials into the Dockerfile
- DO NOT scan ports when Docker local is already running
"""


def wf_prepare():
    return r"""
---
description: Prep Pipeline (Specify → Clarify → Plan → Tasks → Analyze) — no Implement
---

# 📋 Prep Pipeline

## Pre-conditions
- constitution.md exists

## Steps
1. **@speckit.specify** — Generate spec.md
2. **@speckit.clarify** — Resolve ambiguity
3. **@speckit.plan** — Create plan.md + data-model.md
4. **GATE**: Constitution compliance check
5. **@speckit.tasks** — Create tasks.md
6. **@speckit.analyze** — Verify consistency

## Success Criteria
- ✅ spec.md + plan.md + tasks.md exists
- ✅ Coverage ≥ 90%, no constitution violations
- ⏸️ Stop here — DO NOT implement
"""


def wf_util_checklist():
    return r"""
---
description: Create/validate Requirements Checklist
---

# ✅ Requirements Checklist

## Steps
1. **@speckit.checklist** — Parse spec.md → create checklist
2. Link requirements → task IDs
3. Output: checklist.md

## Success Criteria
- ✅ Each requirement linked to ≥1 task
"""


def wf_util_content():
    return r"""
---
description: Content Strategy & Readability Audit
---

# 📝 Content Audit

## Pre-conditions
- Content pages created

## Steps
1. **@speckit.content** — Audit heading, readability, multimodal, fact-density
2. Output: content-guidelines.md

## Success Criteria
- ✅ Each page has 1 H1, correct hierarchy
- ✅ Readability guidelines documented
"""


def wf_util_diff():
    return r"""
---
description: Compare Artifacts (Spec vs Implementation)
---

# 🔀 Artifact Comparison

## Steps
1. **@speckit.diff** — Compare 2 versions/artifacts
2. Output: Added/Removed/Changed table + impact analysis

## Success Criteria
- ✅ Diff report generated
"""


def wf_util_migrate():
    return r"""
---
description: Migrate Legacy Code — Reverse-engineer existing codebase
---

# 🔄 Legacy Migration

## Pre-conditions
- Existing codebase with source code
- constitution.md setup (target standards)

## Steps
1. **@speckit.migrate** — Scan codebase:
   - Detect languages, frameworks, dependencies
   - Reverse-engineer data models, routes
   - Create draft spec.md
   - Assess tech debt → migration-risk.md
2. Review findings with developers
3. Continue with `/02-speckit.specify` to add new features

## Success Criteria
- ✅ Draft spec.md created from existing code
- ✅ migration-risk.md with tech debt inventory
"""


def wf_util_quizme():
    return r"""
---
description: Red Team - Ask critical questions to find edge cases
---

# 🎯 Red Team Quiz

## Pre-conditions
- spec.md + plan.md exists

## Steps
1. **@speckit.quizme** — Challenge spec+plan:
   - Boundary, concurrency, failure, security, scale questions
   - Max 5 questions, interactive Q&A
2. If issues are detected → update spec.md

## Success Criteria
- ✅ All edge cases have been addressed
"""


def wf_util_status():
    return r"""
---
description: Display Progress Dashboard
---

# 📊 Progress Dashboard

## Steps
1. **@speckit.status** — Parse tasks.md → display:
   - Per-phase progress bars
   - Total completion %
   - Pending tasks list

## Success Criteria
- ✅ Dashboard displayed
"""


def wf_util_taskstoissues():
    return r"""
---
description: Sync tasks.md → Issue Tracker
---

# 🔗 Issue Sync

## Pre-conditions
- tasks.md exists

## Steps
1. **@speckit.taskstoissues** — Parse tasks → generate issue export
2. Output: issues-export.md (ready to copy to GitHub/GitLab)

## Success Criteria
- ✅ issues-export.md generated
- ✅ Each task mapped into 1 issue
"""


def wf_util_uiux():
    return r"""
---
description: Set up/update UI/UX Design System & Standards
---

# 🎨 UI/UX Standards Setup

## Pre-conditions
- `constitution.md` already exists (for tech stack)

## Steps

1. **@speckit.uiux** — Domain & tech stack analysis
2. Recommended Brand Palette & Typography
3. Definition of Spacing & Grid system
4. Set up Core Components (Buttons, Cards, Inputs)
5. Output/Update: `.agent/knowledge_base/ui_ux_standards.md`

## Success Criteria
- ✅ `ui_ux_standards.md` exists with all sections Brand, Typography, Components.
- ✅ Mobile-first compliant design.
"""


def wf_debug():
    return r"""
---
description: Systematic Debugging
---

# 🐞 Systematic Debugging Pipeline

## Steps
1. **@speckit.debug** — Analyze errors and find Root Cause.
2. Reproduce errors via script/test.
3. Propose and implement Fix Plan.
"""


def wf_backlog():
    return r"""
---
description: Managing Ideas (Backlog) and scanning technical debt (TODO/FIXME)
---

# 📋 Backlog Management

## Steps
1. **@speckit.backlog** — Scans the codebase and updates the to-do list.
2. Categorize and prioritize work items.
"""


def wf_roadmap():
    return r"""
---
description: Manage high-level roadmaps (Milestones) and transitions between Phases
---

# 🗺️ Project Roadmap

## Steps
1. **@speckit.roadmap** — Update and track project Phases/Milestones.
"""


def wf_map():
    return r"""
---
description: Draw the architecture map and dependency diagram of the Codebase
---

# 🗺️ Codebase Mapping

## Steps
1. **@speckit.map** — Scan the entire project and generate architectural documents.
"""


def wf_uat():
    return r"""
---
description: UAT Analyzer - Analyze manual acceptance results and process gaps from the User.
---

# ✅ User Acceptance Testing (UAT)

## Steps
1. **@speckit.uat** — Collect feedback and create a feature improvement plan.
"""


def wf_wordpress():
    return r"""
---
description: WordPress Theme & Plugin Development Workflow
---

# WordPress Development

## Steps
1. **@speckit.wordpress** — Deploy themes/plugins according to professional WordPress standards.
"""


def wf_orchestrate():
    return r"""
---
description: Multi-Agent Orchestration - Select and coordinate agents by project_type + attributes
---

# 🧭 Multi-Agent Orchestration

## Pre-conditions
- `.agent/project.json` exists (has `project_type` + `attributes` )
- `.agent/agents/registry.json` exists
- `.agent/memory/constitution.md` exists

## Steps

1. **@orchestrator** — Resolve agent set:
   - Read `project.json.project_type` + `attributes`
   - `active = core + base[type] + modifiers[architecture|platforms|flags]`
   - Log list of activated agents (duplicate types)

2. Run the pipeline with the selected agent:
   - Specify → Clarify → Plan → Tasks → Implement → Verify
   - Each task attaches the tag `@agent:<name>` to route

3. **Routing**: Orchestrator giao task cho domain agent theo tag.
   - For example project_type= `game` → task gameplay route to `@speckit.gamedev`
   - For example `platforms:[ios]` → task mobile route to `@speckit.ios`

4. **Conflict resolution**: Constitution > Orchestrator > Domain Agent.

## Success Criteria
- ✅ Correct set of agents activated according to project_type + attributes
- ✅ Each task has a clear owner agent
- ✅ Does not violate the Constitution
"""


def wf_gamedev():
    return r"""
---
description: Game Development Pipeline - Engine setup, game loop, performance, asset pipeline
---

# 🎮 Game Development

## Pre-conditions
- `project.json.project_type` = `game`
- Identified target engine (Unity/Unreal/Godot/Phaser/PixiJS/custom)

## Steps

1. **@speckit.gamedev** — Engine & Project Setup
   - Determine engine, directory structure, Docker env (web game) or CI build (native)

2. **@speckit.gamedev** — Core Architecture
   - Game loop (fixed/variable timestep), ECS/Component, State Machine, Event Bus

3. **@speckit.gamedev** — Performance Budget
   - Frame budget (16.6ms@60fps), object pooling, profiling

4. **@speckit.uiux** — HUD & Menu
   - UI states (Menu/Pause/GameOver), responsive HUD

5. **@speckit.gamedev** — Asset Pipeline + Netcode (if multiplayer)
   - Atlas/LOD, naming convention, server-authoritative netcode

6. **@speckit.tester** — Game logic tests + playtest checklist

## Success Criteria
- ✅ Game loop is stable, reaching frame budget
- ✅ No hard-code balance/asset/URL (use config/ENV)
- ✅ Object pooling cho hot objects
- ✅ Multiplayer (if any): server validate
"""


# =============================================================================
# WORKFLOW TEMPLATE MAP — Complete mapping for all workflows
# =============================================================================
WORKFLOW_TEMPLATE_MAP = {
    "00-speckit.all": wf_00_all,
    "01-speckit.constitution": wf_01_constitution,
    "02-speckit.specify": wf_02_specify,
    "03-speckit.clarify": wf_03_clarify,
    "04-speckit.plan": wf_04_plan,
    "05-speckit.tasks": wf_05_tasks,
    "06-speckit.analyze": wf_06_analyze,
    "07-speckit.implement": wf_07_implement,
    "08-speckit.checker": wf_08_checker,
    "09-speckit.tester": wf_09_tester,
    "10-speckit.reviewer": wf_10_reviewer,
    "11-speckit.validate": wf_11_validate,
    "12-speckit.seo": wf_12_seo,
    "13-speckit.geo": wf_13_geo,
    "speckit.identity": wf_identity,
    "speckit.devops": wf_devops,
    "speckit.prepare": wf_prepare,
    "util-speckit.checklist": wf_util_checklist,
    "util-speckit.content": wf_util_content,
    "util-speckit.diff": wf_util_diff,
    "util-speckit.migrate": wf_util_migrate,
    "util-speckit.quizme": wf_util_quizme,
    "util-speckit.status": wf_util_status,
    "util-speckit.taskstoissues": wf_util_taskstoissues,
    "util-speckit.uiux": wf_util_uiux,
    "speckit.debug": wf_debug,
    "speckit.backlog": wf_backlog,
    "speckit.roadmap": wf_roadmap,
    "speckit.map": wf_map,
    "speckit.uat": wf_uat,
    "speckit.wordpress": wf_wordpress,
    "speckit.orchestrate": wf_orchestrate,
    "speckit.gamedev": wf_gamedev,
}

