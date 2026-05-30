# ⚡ bro-skills - Spec-Driven Development CLI

> **Python CLI tool** để khởi tạo bất kỳ project nào theo chuẩn Spec-Driven Development (SDD) của Antigravity.

## 🎯 Mục đích

Tool này tự động tạo cấu trúc `.agent/` chuẩn cho Antigravity IDE, bao gồm:

- **Skills** (29 skills) — Khả năng AI tự trị cho từng phase SDLC, thêm Debug, Backlog, Roadmap, Map, UAT, WordPress, UI/UX Pro Max
- **Workflows** (31 workflows) — Orchestration commands với pre-conditions, gate checks, success criteria
- **Templates** — Spec, Plan, Tasks, Constitution, Infrastructure, SEO, **UI/UX Standards** templates
- **Scripts** — 4 bash utilities (create-feature, setup-plan, check-prerequisites, update-context)

## 📋 Requirements

- Python 3.9+ (Windows, Linux, macOS)
- Node.js 16+ nếu muốn chạy bằng `npx`
- Không cần thêm thư viện ngoài (Pure Python stdlib)

---

## 📦 Cài đặt / chạy CLI (Mọi OS)

### Cách 1: Chạy bằng `npx` (không cài global)

```bash
# Chạy trực tiếp từ GitHub qua npm/npx
npx github:wedabro/bro-skills version
npx github:wedabro/bro-skills init --target /path/to/project

# Truyền tham số như CLI bình thường
npx github:wedabro/bro-skills init --name "My Project" --type fullstack

# Sau khi package được publish lên npm registry
npx bro-skills version
npx bro-skills init --target /path/to/project
```

Ghi chú:
- `npx` cần Node.js/npm và Python 3.9+ có trong PATH.
- Wrapper npm chỉ gọi lại Python CLI gốc, không cài dependency npm riêng.
- Nếu muốn cố định Python executable, đặt ENV `PYTHON=/path/to/python`.

### Cách 2: `pip install` từ GitHub (Khuyến nghị cho dùng lâu dài)

```bash
# Windows / Linux / macOS — Cài global, lệnh `bro-skills` dùng được ở mọi nơi
pip install git+https://github.com/wedabro/bro-skills.git

# Kiểm tra
bro-skills version
# → bro-skills v1.2.0
```

### Cách 3: `pipx install` (Isolated - Không ảnh hưởng system Python)

```bash
# Cài pipx nếu chưa có
pip install pipx
pipx ensurepath

# Cài bro-skills
pipx install git+https://github.com/wedabro/bro-skills.git

# Kiểm tra
bro-skills version
```

### Cách 4: Clone + Install (Development)

```bash
git clone https://github.com/wedabro/bro-skills.git
cd bro-skills

# Cài editable mode (thay đổi code tự động có hiệu lực)
pip install -e .

# Hoặc chạy trực tiếp không cần install
python ssd.py init
```

### Cách 5: Chạy trực tiếp (Không cài)

```bash
# Clone về và chạy trực tiếp
git clone https://github.com/wedabro/bro-skills.git
python bro-skills/ssd.py init --target /path/to/project
```

### Gỡ cài đặt

```bash
pip uninstall bro-skills
# hoặc
pipx uninstall bro-skills
# hoặc nếu cài global bằng npm từ GitHub
npm uninstall -g bro-skills
```

---

## 🚀 Cách sử dụng

```bash
# Init project mới
bro-skills init

# Init tại thư mục cụ thể
bro-skills init --target /path/to/project

# Init với project name
bro-skills init --name "My Awesome Project"

# Init và ghi đè không hỏi
bro-skills init --force

# Xem danh sách skills
bro-skills list-skills

# Xem danh sách workflows
bro-skills list-workflows

# Validate cấu trúc .agent
bro-skills validate --target /path/to/project

# Xem version
bro-skills version
bro-skills -v
```

### Chọn nhanh skill/workflow cho AI

| Nhu cầu | Dùng workflow/skill |
|---|---|
| Thiết lập luật dự án, tech stack, nguyên tắc bắt buộc | `/01-speckit.constitution` |
| Viết spec từ mô tả tự nhiên | `/02-speckit.specify` |
| Làm rõ yêu cầu mơ hồ trước khi code | `/03-speckit.clarify` |
| Tạo kiến trúc, data model, API contracts | `/04-speckit.plan` |
| Chia task atomic theo 15-Minute Rule | `/05-speckit.tasks` |
| Implement có kiểm soát blast radius và test | `/07-speckit.implement` |
| Review, static check, test, validate sau implement | `/08-speckit.checker`, `/09-speckit.tester`, `/10-speckit.reviewer`, `/11-speckit.validate` |
| Migration dự án có sẵn | `/util-speckit.migrate` |
| Debug sự cố, quản lý backlog/roadmap, map codebase, UAT | `/speckit.debug`, `/speckit.backlog`, `/speckit.roadmap`, `/speckit.map`, `/speckit.uat` |
| Web SEO/GEO/Content/UIUX/WordPress | `/12-speckit.seo`, `/13-speckit.geo`, `/util-speckit.content`, `/util-speckit.uiux`, `/speckit.wordpress` |

---

## 🆕 Quy trình A: Dự án MỚI (Greenfield)

> Dùng khi bạn bắt đầu từ con số 0 — chưa có code.

### Bạn cần chuẩn bị gì?

| # | Thông tin | Ví dụ | Bắt buộc? |
|---|-----------|-------|-----------|
| 1 | **Tên project** | "E-Commerce Platform" | ✅ Có |
| 2 | **Mô tả feature** bằng ngôn ngữ tự nhiên | "Hệ thống đặt hàng hải sản online..." | ✅ Có |
| 3 | **Tech stack** (ngôn ngữ, framework) | Next.js 15, Python, Go... | ✅ Có (bước Constitution) |
| 4 | **Nguyên tắc project** (principles) | "Docker-first", "No hardcode"... | ✅ Có (bước Constitution) |
| 5 | **User stories** chi tiết | Các kịch bản người dùng cụ thể | ⚪ Không (AI suy luận) |

### Pipeline (7 bước)

```
Bước 0: Init         →  bro-skills init --name "My Project"
    ↓                    Tạo ~70 files trong .agent/
    ↓
Bước 1: Constitution  →  /01-speckit.constitution
    ↓                    Thiết lập "luật" cho project (tech stack, principles)
    ↓                    ⚠️ KHÔNG ĐƯỢC BỎ QUA — đây là "Context Anchor"
    ↓
Bước 2: Specify       →  /02-speckit.specify "Mô tả feature bằng tiếng Việt hoặc Anh"
    ↓                    AI tạo spec.md — CHỈ nói WHAT (cái gì), KHÔNG nói HOW
    ↓                    Output: User scenarios, functional requirements, success criteria
    ↓
Bước 3: Clarify       →  /03-speckit.clarify
    ↓                    AI phát hiện chỗ mơ hồ, hỏi tối đa 3 câu (bảng A/B/C)
    ↓                    Update lại spec.md sau khi bạn trả lời
    ↓
Bước 4: Plan          →  /04-speckit.plan
    ↓                    AI tạo plan.md — Technical architecture
    ↓                    Output: data-model.md, contracts/, research.md
    ↓                    Gate Check: Kiểm tra Constitution compliance
    ↓
Bước 5: Tasks         →  /05-speckit.tasks
    ↓                    AI tạo tasks.md — Atomic tasks (15-Minute Rule)
    ↓                    Format: - [ ] T001 [US1] Description with file path
    ↓                    Organized by User Story, có dependency graph
    ↓
Bước 6: Implement     →  /07-speckit.implement
                         AI code theo tasks.md với 4 IRONCLAD Protocols
                         (Blast Radius → Strangler Pattern → TDD → Context Anchoring)
```

### Shortcut

```bash
# Chạy pipeline Specify → Clarify → Plan → Tasks → Analyze trong 1 lệnh:
/00-speckit.all "Mô tả feature..."

# Hoặc chạy prep pipeline (không có Implement):
/speckit.prepare "Mô tả feature..."
```

### Chi tiết từng bước

#### Bước 0 — `bro-skills init`

```bash
bro-skills init --target /path/to/project --name "My Project"
```

- Tạo cấu trúc `.agent/` (~70 files: 29 skills, 31 workflows, 7 templates, 4 scripts, identity, knowledge base, constitution, README)
- Mở project trong Antigravity IDE — agent tự động nhận diện `.agent/` folder

#### Bước 1 — `/01-speckit.constitution` ⚠️ BẮT BUỘC

- **Input**: Bạn cung cấp tech stack, coding principles, non-negotiables
- **Output**: `constitution.md` — "Source of Law" cho toàn bộ project
- **Tại sao quan trọng**: Mọi bước sau đều check lại Constitution để AI không hallucinate
- **Ví dụ input**:

  ```
  /01-speckit.constitution
  Tech: Next.js 15, Prisma, PostgreSQL
  Principles:
  1. Docker-first — mọi thứ chạy trong Docker
  2. No hardcode — dùng ENV vars
  3. API-first — backend API trước, frontend sau
  ```

#### Bước 2 — `/02-speckit.specify`

- **Input**: Mô tả feature bằng ngôn ngữ tự nhiên
- **Output**: `spec.md` — Feature specification (WHAT, không phải HOW)
- **AI tự động**: Extract actors, actions, data, constraints → User scenarios → Functional requirements → Success criteria
- **Ví dụ**:

  ```
  /02-speckit.specify "Xây dựng hệ thống quản lý đơn hàng hải sản 
  với giỏ hàng, thanh toán COD/chuyển khoản, và tracking đơn hàng"
  ```

#### Bước 3 — `/03-speckit.clarify`

- **Input**: Không cần — AI tự đọc spec.md
- **Output**: Updated `spec.md` với mọi mơ hồ được giải quyết
- **Quy trình**:
  1. AI scan spec → phát hiện vague language, missing boundaries, undefined error handling
  2. Phân loại: 🔴 CRITICAL / 🟡 IMPORTANT / 🟢 MINOR
  3. Hỏi bạn tối đa 3 câu CRITICAL (bảng options A/B/C)
  4. Auto-fix các vấn đề MINOR

#### Bước 4 — `/04-speckit.plan`

- **Input**: Không cần — AI đọc spec.md + constitution.md
- **Output**: `plan.md`, `data-model.md`, `contracts/`, `research.md`
- **2 Phases**:
  - Phase 0 (Research): Giải quyết mọi "NEEDS CLARIFICATION" → `research.md`
  - Phase 1 (Design): Entity extraction → API contracts → `data-model.md`, `contracts/`
- **Gate Check**: Kiểm tra plan có vi phạm Constitution không → ERROR nếu có

#### Bước 5 — `/05-speckit.tasks`

- **Input**: Không cần — AI đọc plan.md + spec.md
- **Output**: `tasks.md` — Atomic, dependency-ordered task list
- **Format bắt buộc**:

  ```markdown
  - [ ] T001 Create project structure per implementation plan
  - [ ] T005 [P] Implement auth middleware in src/middleware/auth.py
  - [ ] T012 [P] [US1] Create User model in src/models/user.py
  ```

- **Phase structure**:
  - Phase 1: Setup (project init)
  - Phase 2: Foundation (blocking prerequisites)
  - Phase 3+: Mỗi User Story 1 phase (priority order từ spec)
  - Final: Polish & cross-cutting

#### Bước 6 — `/07-speckit.implement`

- **Input**: Không cần — AI đọc tasks.md + plan.md
- **Quy trình cho MỖI task**:
  1. 🔍 **Blast Radius Analysis**: Scan affected files → report risk level
  2. 🏗️ **Strategy**: LOW risk → inline edit, HIGH risk → Strangler Pattern (tạo file mới)
  3. 🧪 **TDD**: Tạo `repro_task_[ID]` script → chạy fail → code fix → chạy pass
  4. ✅ **Mark complete**: `- [X] T001 ...` trong tasks.md
- **Anti-Hallucination**: Không import magic, strict diff-only, stop & ask nếu sửa >3 files

---

## 🔄 Quy trình B: Dự án CÓ SẴN (Legacy Migration)

> Dùng khi bạn đã có codebase và muốn áp dụng SDD methodology lên project hiện tại.

### Khác biệt với Dự án Mới

| Aspect | Dự án MỚI | Dự án CÓ SẴN |
|--------|-----------|--------------|
| Xuất phát | Từ ý tưởng → code | Từ code → spec |
| Bước đặc biệt | `/02-speckit.specify` | `/util-speckit.migrate` |
| Constitution | Thiết lập từ đầu | Reverse-engineer từ codebase |
| Tasks | Tạo mới 100% | Mix: migration tasks + new features |

### Pipeline (7 bước)

```
Bước 0: Init          →  bro-skills init --target /path/to/existing --name "Legacy Project"
    ↓                     Tạo .agent/ BÊN TRONG project hiện tại
    ↓
Bước 1: Constitution   →  /01-speckit.constitution
    ↓                     Khai báo tech stack HIỆN TẠI + principles MỚI
    ↓
Bước 2: Migrate        →  /util-speckit.migrate
    ↓                     AI scan codebase → reverse-engineer spec + plan sơ bộ
    ↓                     Output: Technical debt inventory, migration risk assessment
    ↓
Bước 3: Specify        →  /02-speckit.specify "Feature mới cần thêm..."
    ↓                     Spec cho feature MỚI, kế thừa context từ migrate
    ↓
Bước 4: Plan → Tasks   →  /04-speckit.plan → /05-speckit.tasks
    ↓
Bước 5: Implement      →  /07-speckit.implement
                          Code với Strangler Pattern — KHÔNG phá code cũ
```

### Chi tiết bước Migrate

**`/util-speckit.migrate`** thực hiện:

1. **Scan codebase**: Detect languages, frameworks, project structure
2. **Extract entities**: Tìm data models, routes, endpoints từ code hiện tại
3. **Reverse-engineer spec**: Tạo `spec.md` ban đầu từ code
4. **Assess technical debt**: Inventory các vấn đề cần fix
5. **Recommend migration sequence**: Đề xuất thứ tự migrate features

### Ví dụ thực tế

```bash
# 1. Init — tạo .agent/ trong project hiện tại
bro-skills init --target /path/to/dinhchopmonngon --name "DinhChopMonNgon"

# 2. Constitution — khai báo stack hiện tại
/01-speckit.constitution
# → "Next.js 15, Prisma 6, PostgreSQL, Docker-first, Port 8900-8999"

# 3. Migrate — AI đọc và phân tích code hiện tại
/util-speckit.migrate
# → AI tạo spec.md từ features đã có + technical debt report

# 4. Thêm feature mới trên nền tảng hiện tại
/02-speckit.specify "Sync data từ API cũ tomhum.com.vn"

# 5. Plan + Tasks + Implement
/04-speckit.plan
/05-speckit.tasks
/07-speckit.implement
```

---

## 🛡️ IRONCLAD Protocols (Áp dụng cho cả 2 quy trình)

Mỗi khi AI implement code, 4 protocols này được thực thi **bắt buộc**:

| Protocol | Mục đích | Khi nào |
|----------|----------|---------|
| **1. Blast Radius Analysis** | Đánh giá ảnh hưởng trước khi sửa | TRƯỚC mỗi modification |
| **2. Strangler Pattern** | Tạo file mới thay vì sửa file critical | Khi >2 files bị ảnh hưởng |
| **3. Reproduction Script First** | Chứng minh bug/feature trước khi code | TRƯỚC mỗi implementation |
| **4. Context Anchoring** | Re-orient project structure | Mỗi 3 tasks |

---

## 📂 Cấu trúc .agent/ được tạo

```
.agent/
├── identity/                  # Tầng nhân cách AI
│   └── master-identity.md     # Persona, Soul, Core Capabilities
│
├── knowledge_base/            # Tầng tri thức dự án (auto-populated)
│   ├── infrastructure.md      # Docker, ports, environments
│   ├── data_schema.md         # DB models, relationships
│   ├── api_standards.md       # Routes, conventions, auth
│   ├── business_logic.md      # Domain rules, source structure
│   └── seo_standards.md       # SEO/GEO checklist (web projects only)
│
├── skills/                    # @ Mentions — 29 Agentic Capabilities
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
├── workflows/                 # / Slash Commands — 31 Orchestrations
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
    ├── __init__.py            # Version: __version__ = "1.2.0"
    ├── __main__.py            # python -m bro_skills
    ├── cli.py                 # Console script entry point → `bro-skills` command
    ├── registry.py            # Single Source of Truth — 29 skills + 31 workflows + 7 project types
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

| # | Check | Mô tả |
|---|-------|-------|
| 1 | Thư mục .agent/ | Tồn tại |
| 2 | Core directories | skills/, workflows/, templates/, scripts/, memory/ |
| 3 | Skills | 29 thư mục + SKILL.md |
| 4 | Workflows | 31 .md files |
| 5 | Templates | 4 document templates |
| 6 | Scripts | 4 bash scripts |
| 7 | Constitution | memory/constitution.md |
| 8 | README | .agent/README.md |
| 9 | Content quality | Mỗi SKILL.md > 100 bytes |
| 10 | Frontmatter | Mỗi workflow có YAML header |

---

## 🌟 Best Practices

1. **❌ Không bao giờ bỏ qua Constitution** — Đây là anchor ngăn AI hallucinate
2. **🛡️ Layered Defense** — Mỗi bước validate bước trước (Specify → Clarify → Plan → Tasks → Analyze)
3. **⏱️ 15-Minute Rule** — Mỗi task phải hoàn thành trong ≤15 phút
4. **🔄 Refine, Don't Rewind** — Build incrementally, không bao giờ bắt đầu lại từ đầu
5. **📊 Spec trước Code** — WHAT trước, HOW sau. Business stakeholders đọc được spec.md

---

## CI/CD

- CI: GitHub Actions chạy `pytest` cho pull requests và mọi push.
- Release: tạo tag `vX.Y.Z` để build sdist/wheel và tạo GitHub Release kèm artifacts.

```bash
git tag v1.2.3
git push origin v1.2.3
```

---

## 📄 License

MIT

