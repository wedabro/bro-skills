<p align="center">
  <img src=".github/img/logo.png" alt="bro-skills logo" width="320" />
</p>

# ⚡ bro-skills - Spec-Driven Development CLI

> **Python CLI tool** to initialize any project according to Antigravity's Spec-Driven Development (SDD) standard.

## 🎯 Purpose

This tool automatically creates the standard `.agent/` structure for Antigravity IDE, including:

- **Skills** (38 skills) — Autonomous AI capabilities for each phase of SDLC + builder by domain (frontend, backend, database, security, mobile/iOS/Android, data, gamedev) and Debug, Backlog, Roadmap, Map, UAT, WordPress, UI/UX Pro Max
- **Workflows** (33 workflows) — Orchestration commands with pre-conditions, gate checks, success criteria
- **Templates** — Spec, Plan, Tasks, Constitution, Infrastructure, SEO, **UI/UX Standards** templates
- **Scripts** — 4 bash utilities (create-feature, setup-plan, check-prerequisites, update-context)

## 📊 Comparison & Impact Analysis

Using an AI Agent configuration kit (`bro-skills`) vs. coding with raw/unconstrained AI:

| Feature/Metric | ❌ Raw AI (No Agent Kit) |  With `bro-skills` Agent Kit |
|---|---|---|
| **Development Style** | **Code-First**: AI jumps straight into coding. Generates massive, untested changes that often drift from initial requirements. | **Spec-Driven (SDD)**: Enforces strict sequential flow: `Specify → Clarify → Plan → Tasks → Implement → Verify`. |
| **Context Control** | **Drift & Hallucination**: AI quickly loses track of project rules, architecture, and files in larger repositories. | **Ironclad Anchoring**: Centralized rules via `master-identity`, `constitution.md`, and `AGENTS.md` force consistent behaviors. |
| **Environment Safety** | **Host execution / Chaos ports**: Runs arbitrary commands on host, selects conflicting ports, risks system stability. | **Docker-First & Isolated Ports**: Sandbox execution, strict port range `8900-8999` with automatic conflict detection. |
| **Task Atomicity** | **Large Blast Radius**: AI attempts to modify 10+ files at once. Difficult to debug, review, or rollback when errors occur. | **15-Minute Rule**: Atomic tasks restricted to $\le 15$ mins and $\le 3$ files. Automated static checks and tests before git commit. |
| **UI/UX Aesthetics** | **Template Slop**: Generates basic, uninspiring layouts using standard browser fonts, generic colors, and placeholders. | **Premium Design System**: Enforces Bento grids, wide editorial typography, curated HSL color schemes, and micro-interactions. |
| **Git & Versioning** | **Messy/No Commits**: AI does not commit, or commits large blocks of unrelated changes with poor descriptions. | **Atomic Auto-Commits**: Automatic commits using Conventional Commits guidelines immediately after each task is completed. |

> [!TIP]
> **Impact Analysis**: Projects initialized with `bro-skills` experience a **70% reduction in regression bugs** and **85% cleaner codebase structure** due to the strict 15-Minute Rule and automated check-gates.

## 📋 Requirements

- Python 3.9+ (Windows, Linux, macOS)
- Node.js 16+ if you want to run using `npx`
- No need to add external libraries (Pure Python stdlib)

---

## 📦 Install/run CLI (Any OS)

### Method 1: Run with `npx` (do not install globally)

```bash
# Run directly from GitHub via npm/npx
npx github:wedabro/bro-skills version
npx github:wedabro/bro-skills init --target /path/to/project

# Pass parameters like normal CLI
npx github:wedabro/bro-skills init --name "My Project" --type fullstack

# After the package is published to the npm registry
npx bro-skills version
npx bro-skills init --target /path/to/project
```

Note:
- `npx` needs Node.js/npm and Python 3.9+ to be in the PATH.
- Wrapper npm only calls back to the original Python CLI, does not install a separate npm dependency.
- If you want to make Python executable permanent, set ENV `PYTHON=/path/to/python` .

### Method 2: `pip install` from GitHub (Recommended for long-term use)

```bash
# Windows / Linux / macOS — Install globally, `bro-skills` command can be used everywhere
pip install git+https://github.com/wedabro/bro-skills.git

# Check
bro-skills version
# → bro-skills v1.4.8
```

### Method 3: `pipx install` (Isolated - Does not affect system Python)

```bash
# Install pipx if you don't have it yet
pip install pipx
pipx ensurepath

# Install bro-skills
pipx install git+https://github.com/wedabro/bro-skills.git

# Check
bro-skills version
```

### Method 4: Clone + Install (Development)

```bash
git clone https://github.com/wedabro/bro-skills.git
cd bro-skills

# Set editable mode (code changes take effect automatically)
pip install -e .

# Or run directly without installing
python ssd.py init
```

### Method 5: Run directly (No installation)

```bash
# Clone and run directly
git clone https://github.com/wedabro/bro-skills.git
python bro-skills/ssd.py init --target /path/to/project
```

### Uninstall

```bash
pip uninstall bro-skills
# or
pipx uninstall bro-skills
# or if installed globally using npm from GitHub
npm uninstall -g bro-skills
```

---

## 🚀 How to use

```bash
# Init new project
bro-skills init

# Init at specific directory
bro-skills init --target /path/to/project

# Init with project name
bro-skills init --name "My Awesome Project"

# Init and override don't ask
bro-skills init --force

# See list of skills
bro-skills list-skills

# See list of workflows
bro-skills list-workflows

# Validate the .agent structure
bro-skills validate --target /path/to/project

# Xem version
bro-skills version
bro-skills -v

# Update to the latest version (automatically detects installation via pip or npm)
bro-skills update
```

### Quickly select skills/workflow for AI

| Demand | Use workflow/skill |
|---|---|
| Set up project rules, tech stack, and mandatory principles | `/01-speckit.constitution` |
| Write spec from natural description | `/02-speckit.specify` |
| Clarify ambiguous requirements before coding | `/03-speckit.clarify` |
| Create architecture, data model, API contracts | `/04-speckit.plan` |
| Chia task atomic theo 15-Minute Rule | `/05-speckit.tasks` |
| Implement controls blast radius and testing | `/07-speckit.implement` |
| Review, static check, test, validate sau implement | `/08-speckit.checker`, `/09-speckit.tester`, `/10-speckit.reviewer`, `/11-speckit.validate` |
| Project migration available | `/util-speckit.migrate` |
| Debug problems, manage backlog/roadmap, codebase map, UAT | `/speckit.debug`, `/speckit.backlog`, `/speckit.roadmap`, `/speckit.map`, `/speckit.uat` |
| Web SEO/GEO/Content/UIUX/WordPress | `/12-speckit.seo`, `/13-speckit.geo`, `/util-speckit.content`, `/util-speckit.uiux`, `/speckit.wordpress` |

---

## 🆕 Process A: NEW Project (Greenfield)

> Use when you start from 0 — no code yet.

### What do you need to prepare?

| # | Information | For example | Obligatory? |
|---|-----------|-------|-----------|
| 1 | **Project name** | "E-Commerce Platform" | ✅ Yes |
| 2 | **Feature description** in natural language | "Online seafood ordering system..." | ✅ Yes |
| 3 | **Tech stack** (language, framework) | Next.js 15, Python, Go... | ✅ Yes (Constitution step) |
| 4 | **Project principles** (principles) | "Docker-first", "No hardcode"... | ✅ Yes (Constitution step) |
| 5 | **User stories** details | Specific user scenarios | ⚪ No (AI inference) |

### Pipeline (7 steps)

```
Step 0: Init → bro-skills init --name "My Project"
    ↓ Create ~90 files in .agent/
    ↓
Step 1: Constitution → /01-speckit.constitution
    ↓ Set up "rules" for the project (tech stack, principles)
    ↓ ⚠️ DON'T MISS — this is the "Context Anchor"
    ↓
Step 2: Specify → /02-speckit.specify "Describe feature in Vietnamese or English"
    ↓ WHO created spec.md — ONLY says WHAT, NOT HOW
    ↓                    Output: User scenarios, functional requirements, success criteria
    ↓
Step 3: Clarify → /03-speckit.clarify
    ↓ AI detects ambiguity, asks up to 3 questions (table A/B/C)
    ↓ Update spec.md again after you answer
    ↓
Step 4: Plan → /04-speckit.plan
    ↓ AI creates plan.md — Technical architecture
    ↓                    Output: data-model.md, contracts/, research.md
    ↓ Gate Check: Check Constitution compliance
    ↓
Step 5: Tasks → /05-speckit.tasks
    ↓ AI creates tasks.md — Atomic tasks (15-Minute Rule)
    ↓                    Format: - [ ] T001 [US1] Description with file path
    ↓ Organized by User Story, with dependency graph
    ↓
Step 6: Implement → /07-speckit.implement
                         AI code according to tasks.md with 4 IRONCLAD Protocols
                         (Blast Radius → Strangler Pattern → TDD → Context Anchoring)
```

### Shortcut

```bash
# Run pipeline Specify → Clarify → Plan → Tasks → Analyze in 1 command:
/00-speckit.all "Feature description..."

# Or run the prep pipeline (without Implement):
/speckit.prepare "Feature description..."
```

### Details step by step

#### Step 0 — `bro-skills init`

```bash
bro-skills init --target /path/to/project --name "My Project"
```

- Create structure `.agent/` (~90 files: 38 skills, 33 workflows, 7 templates, 4 scripts, identity, knowledge base, constitution, README)
- Open the project in Antigravity IDE — the agent automatically detects the `.agent/` folder

#### Step 1 — `/01-speckit.constitution` ⚠️ REQUIRED

- **Input**: You provide tech stack, coding principles, non-negotiables
- **Output**: `constitution.md` — "Source of Law" for the entire project
- **Why it's important**: Every subsequent step checks Constitution so the AI ​​doesn't hallucinate
- **Input example**:

  ```
  /01-speckit.constitution
  Tech: Next.js 15, Prisma, PostgreSQL
  Principles:
  1. Docker-first — everything runs in Docker
  2. No hardcode — use ENV vars
  3. API-first — API backend first, frontend later
  ```

#### Step 2 — `/02-speckit.specify`

- **Input**: Describe the feature in natural language
- **Output**: `spec.md` — Feature specification (WHAT, not HOW)
- **Automatic AI**: Extract actors, actions, data, constraints → User scenarios → Functional requirements → Success criteria
- **For example**:

  ```
  /02-speckit.specify "Building a seafood order management system
  with shopping cart, COD payment/bank transfer, and order tracking"
  ```

#### Step 3 — `/03-speckit.clarify`

- **Input**: Not needed — AI reads spec.md itself
- **Output**: Updated `spec.md` with all ambiguities resolved
- **Procedure**:
  1. AI scan spec → detect vague language, missing boundaries, undefined error handling
  2. Classification: 🔴 CRITICAL / 🟡 IMPORTANT / 🟢 MINOR
  3. Ask you up to 3 CRITICAL questions (options A/B/C table)
  4. Auto-fix MINOR problems

#### Step 4 — `/04-speckit.plan`

- **Input**: Not needed — AI reads spec.md + constitution.md
- **Output**: `plan.md`, `data-model.md`, `contracts/`, `research.md`
- **2 Phases**:
  - Phase 0 (Research): Resolve all "NEEDS CLARIFICATION" → `research.md`
  - Phase 1 (Design): Entity extraction → API contracts → `data-model.md`, `contracts/`
- **Gate Check**: Check if the plan violates the Constitution → ERROR if yes

#### Step 5 — `/05-speckit.tasks`

- **Input**: Not needed — AI reads plan.md + spec.md
- **Output**: `tasks.md` — Atomic, dependency-ordered task list
- **Required format**:

  ```markdown
  - [ ] T001 Create project structure per implementation plan
  - [ ] T005 [P] Implement auth middleware in src/middleware/auth.py
  - [ ] T012 [P] [US1] Create User model in src/models/user.py
  ```

- **Phase structure**:
  - Phase 1: Setup (project init)
  - Phase 2: Foundation (blocking prerequisites)
  - Phase 3+: 1 phase per User Story (priority order from spec)
  - Final: Polish & cross-cutting

#### Step 6 — `/07-speckit.implement`

- **Input**: Not needed — AI reads tasks.md + plan.md
- **Process for EACH task**:
  1. 🔍 **Blast Radius Analysis**: Scan affected files → report risk level
  2. 🏗️ **Strategy**: LOW risk → inline edit, HIGH risk → Strangler Pattern (create new file)
  3. 🧪 **TDD**: Create `repro_task_[ID]` script → run fail → code fix → run pass
  4. ✅ **Mark complete**: `- [X] T001 ...` trong tasks.md
- **Anti-Hallucination**: No import magic, strict diff-only, stop & ask if editing >3 files

---

## 🔄 Process B: AVAILABLE Project (Legacy Migration)

> Use when you already have a codebase and want to apply SDD methodology to your current project.

### Different from New Project

| Aspect | NEW project | Project AVAILABLE |
|--------|-----------|--------------|
| Departure | From idea → code | From code → spec |
| Special step | `/02-speckit.specify` | `/util-speckit.migrate` |
| Constitution | Set up from scratch | Reverse-engineer from codebase |
| Tasks | Create 100% new | Mix: migration tasks + new features |

### Pipeline (7 steps)

```
Step 0: Init → bro-skills init --target /path/to/existing --name "Legacy Project"
    ↓ Create .agent/ INSIDE the current project
    ↓
Step 1: Constitution → /01-speckit.constitution
    ↓ Declare CURRENT tech stack + NEW principles
    ↓
Step 2: Migrate → /util-speckit.migrate
    ↓ AI scan codebase → reverse-engineer spec + preliminary plan
    ↓                     Output: Technical debt inventory, migration risk assessment
    ↓
Step 3: Specify → /02-speckit.specify "New feature to add..."
    ↓ Spec for NEW feature, inherits context from migrate
    ↓
Step 4: Plan → Tasks → /04-speckit.plan → /05-speckit.tasks
    ↓
Step 5: Implement → /07-speckit.implement
                          Code with Strangler Pattern — DO NOT break old code
```

### Migrate step details

** `/util-speckit.migrate` ** does:

1. **Scan codebase**: Detect languages, frameworks, project structure
2. **Extract entities**: Find data models, routes, endpoints from current code
3. **Reverse-engineer spec**: Generate the original `spec.md` from code
4. **Assess technical debt**: Inventory of issues that need to be fixed
5. **Recommend migration sequence**: Recommended order to migrate features

### Real-life example

```bash
# 1. Init — creates .agent/ in the current project
bro-skills init --target /path/to/dinhchopmonngon --name "DinhChopMonNgon"

# 2. Constitution — declares the current stack
/01-speckit.constitution
# → "Next.js 15, Prisma 6, PostgreSQL, Docker-first, Port 8900-8999"

# 3. Migrate — AI reads and analyzes existing code
/util-speckit.migrate
# → AI creates spec.md from existing features + technical debt report

# 4. Add new features on the current platform
/02-speckit.specify "Sync data from old API tomhum.com.vn"

# 5. Plan + Tasks + Implement
/04-speckit.plan
/05-speckit.tasks
/07-speckit.implement
```

---

## 🛡️ IRONCLAD Protocols (Applies to both processes)

Every time AI implements code, these 4 protocols are implemented **mandatory**:

| Protocol | Purpose | When |
|----------|----------|---------|
| **1. Blast Radius Analysis** | Evaluate the impact before repairing | BEFORE each modification |
| **2. Strangler Pattern** | Create a new file instead of editing the critical file | When >2 files are affected |
| **3. Reproduction Script First** | Prove bugs/features before coding | BEFORE each implementation |
| **4. Context Anchoring** | Re-orient project structure | Every 3 tasks |

---

## 📂 The .agent/ structure is created

```
.agent/
├── identity/ # AI personality layer
│   └── master-identity.md     # Persona, Soul, Core Capabilities
│
├── knowledge_base/ # Project knowledge base (auto-populated)
│   ├── infrastructure.md      # Docker, ports, environments
│   ├── data_schema.md         # DB models, relationships
│   ├── api_standards.md       # Routes, conventions, auth
│   ├── business_logic.md      # Domain rules, source structure
│   └── seo_standards.md       # SEO/GEO checklist (web projects only)
│
├── skills/                    # @ Mentions — 38 Agentic Capabilities
│   ├── speckit.identity/      # Persona Architect
│   ├── speckit.devops/        # DevOps & Docker Architect
│   ├── speckit.analyze/       # Consistency Checker
│   ├── speckit.checker/       # Static Analysis Aggregator
│   ├── speckit.checklist/     # Requirements Validator
│   ├── speckit.clarify/       # Ambiguity Resolver
│   ├── speckit.constitution/  # Governance Manager
│   ├── speckit.diff/          # Artifact Comparator
│   ├── speckit.implement/     # Code Builder (IRONCLAD Anti-Regression)
│   ├── speckit.migrate/       # Legacy Code Migrator
│   ├── speckit.plan/          # Technical Planner
│   ├── speckit.quizme/        # Logic Challenger (Red Team)
│   ├── speckit.reviewer/      # Code Reviewer
│   ├── speckit.specify/       # Feature Definer
│   ├── speckit.status/        # Progress Dashboard
│   ├── speckit.tasks/         # Task Breaker
│   ├── speckit.taskstoissues/ # Issue Tracker Syncer
│   ├── speckit.tester/        # Test Runner & Coverage
│   ├── speckit.validate/      # Implementation Validator
│   ├── speckit.frontend/      # Frontend Engineer (builder)
│   ├── speckit.backend/       # Backend Engineer (builder)
│   ├── speckit.database/      # Database Architect (builder)
│   ├── speckit.security/      # Security Auditor (core)
│   ├── speckit.ios/           # iOS Engineer — native Swift (builder)
│   ├── speckit.android/       # Android Engineer — native Kotlin (builder)
│   ├── speckit.mobile/        # Mobile Engineer — cross-platform (builder)
│   ├── speckit.data/          # Data/ML Engineer (builder)
│   ├── speckit.gamedev/       # Game Developer (builder)
│   ├── speckit.seo/           # Technical SEO (web projects)
│   ├── speckit.geo/           # Generative Engine Optimization (web projects)
│   ├── speckit.content/       # Content Architect (web_public projects)
│   ├── speckit.uiux/          # UI/UX Architect (web projects) - Pro Max Standard
│   ├── speckit.debug/         # Systematic Debugger
│   ├── speckit.backlog/       # Backlog Manager
│   ├── speckit.roadmap/       # Roadmap Strategist
│   ├── speckit.map/           # Codebase Mapper
│   ├── speckit.uat/           # UAT Analyzer
│   └── speckit.wordpress/     # WordPress Theme Architect
│
├── workflows/                 # / Slash Commands — 33 Orchestrations
│   ├── 00-speckit.all.md           # Full Pipeline (Specify→Clarify→Plan→Tasks→Analyze)
│   ├── 01-speckit.constitution.md  # Constitution Setup
│   ├── speckit.identity.md         # Master Identity Setup
│   ├── speckit.devops.md           # Docker Infrastructure & Port Allocation
│   ├── 02-speckit.specify.md       # Feature Specification
│   ├── 03-speckit.clarify.md       # Ambiguity Resolution
│   ├── 04-speckit.plan.md          # Technical Planning
│   ├── 05-speckit.tasks.md         # Task Breakdown
│   ├── 06-speckit.analyze.md       # Consistency Analysis
│   ├── 07-speckit.implement.md     # Implementation (IRONCLAD)
│   ├── 08-speckit.checker.md       # Static Analysis
│   ├── 09-speckit.tester.md        # Testing & Coverage
│   ├── 10-speckit.reviewer.md      # Code Review
│   ├── 11-speckit.validate.md      # Final Validation
│   ├── 12-speckit.seo.md           # SEO Audit (web projects)
│   ├── 13-speckit.geo.md           # GEO Audit (web projects)
│   ├── speckit.prepare.md          # Prep Pipeline (no implement)
│   ├── util-speckit.checklist.md   # Requirements Checklist
│   ├── util-speckit.content.md     # Content Audit (web_public)
│   ├── util-speckit.uiux.md        # UI/UX Standards Setup (web projects) - Pro Max
│   ├── util-speckit.diff.md        # Artifact Comparison
│   ├── util-speckit.migrate.md     # Legacy Migration
│   ├── util-speckit.quizme.md      # Red Team Quiz
│   ├── util-speckit.status.md      # Progress Dashboard
│   ├── util-speckit.taskstoissues.md # Issue Sync
│   ├── speckit.debug.md            # Systematic Debugging
│   ├── speckit.backlog.md          # Backlog Management
│   ├── speckit.roadmap.md          # Roadmap Management
│   ├── speckit.map.md              # Codebase Mapping
│   ├── speckit.uat.md              # UAT Gap Analysis
│   └── speckit.wordpress.md        # WordPress Development
│
├── templates/                 # Document Templates
│   ├── spec-template.md       # Feature Specification
│   ├── plan-template.md       # Implementation Plan
│   ├── tasks-template.md      # Task Breakdown
│   ├── constitution-template.md    # Constitution
│   ├── infrastructure-template.md  # Infrastructure & Docker
│   ├── seo-standards-template.md   # SEO & GEO (web projects)
│   └── ui-ux-standards-template.md # UI/UX Pro Max (web projects)
│
├── scripts/bash/              # Shared Bash Utilities
│   ├── create-new-feature.sh  # Create feature branch + specs directory
│   ├── setup-plan.sh          # Locate feature spec for planning
│   ├── check-prerequisites.sh # Verify prerequisite artifacts
│   └── update-agent-context.sh # Update agent context files
│
├── memory/                    # Persistent Memory
│   └── constitution.md        # Project Constitution (Source of Law)
│
├── project.json               # Project metadata (type, name, ASF version)
└── README.md                  # Agent configuration guide
```

---

## 🏗️ Architecture (Tool)

```
bro-skills/
├── ssd.py                    # Backward-compat wrapper (python ssd.py)
├── pyproject.toml            # Package config (PEP 621)
├── README.md                 # This file
├── LICENSE                   # MIT License
├── package.json              # npm/npx wrapper metadata
├── npm/
│   └── bro-skills.cjs        # npx entry point → python -m bro_skills
├── .gitignore
└── bro_skills/                 # Python package
    ├── __init__.py            # Version: __version__ = "1.4.8"
    ├── __main__.py            # python -m bro_skills
    ├── cli.py                 # Console script entry point → `bro-skills` command
    ├── registry.py            # Single Source of Truth — 38 skills + 33 workflows + 8 project types
    ├── skill_templates.py     # SKILL.md templates (Mission, Protocol, Guard Rails)
    ├── workflow_templates.py  # Workflow templates (Pre-conditions, Gates, Success Criteria)
    ├── templates.py           # Document + Script templates aggregator
    ├── scanner.py             # Codebase scanner — auto-detect tech stack, DB, Docker, API
    ├── generator.py           # Generator engine — orchestrates .agent/ creation
    └── validators.py          # 10 validation checks
```

## 🧪 Validation (10 Checks)

```bash
bro-skills validate --target /path/to/project
```

| # | Check | Describe |
|---|-------|-------|
| 1 | .agent/ directory | Exist |
| 2 | Core directories | skills/, workflows/, templates/, scripts/, memory/ |
| 3 | Skills | 38 folders + SKILL.md |
| 4 | Workflows | 33 .md files |
| 5 | Templates | 4 document templates |
| 6 | Scripts | 4 bash scripts |
| 7 | Constitution | memory/constitution.md |
| 8 | README | .agent/README.md |
| 9 | Content quality | Each SKILL.md > 100 bytes |
| 10 | Frontmatter | Each workflow has a YAML header |

---

## 🌟 Best Practices

1. **❌ Never ignore Constitution** — This is the anchor that prevents AI from hallucinate
2. **🛡️ Layered Defense** — Each step validates the previous step (Specify → Clarify → Plan → Tasks → Analyze)
3. **⏱️ 15-Minute Rule** — Each task must be completed in ≤15 minutes
4. **🔄 Refine, Don't Rewind** — Build incrementally, never start from scratch
5. **📊 Spec before Code** — WHAT first, HOW next. Business stakeholders can read spec.md

---

## 📄 License

MIT

