"""
Workflow Templates - Nội dung chi tiết cho 22 workflows.
Mỗi workflow có: Pre-conditions, Steps với gate checks, Success criteria.
"""


def wf_00_all():
    return """---
description: Full Pipeline (Specify → Clarify → Plan → Tasks → Analyze)
---

# 🚀 Full Pipeline

## Steps

1. **@speckit.map** — (NẾU dự án cũ) Quét cấu trúc và hiểu codebase hiện tại.
   - Output: `.agent/codebase/` docs.

2. **@speckit.specify** — Tạo spec.md từ mô tả feature.
   - Output: `.agent/specs/[feature]/spec.md`.

3. **@speckit.clarify** — Giải quyết mơ hồ và chốt User Scenarios.

4. **@speckit.roadmap** — Cập nhật `.agent/ROADMAP.md` với Phase/Milestone mới.

5. **@speckit.plan** — Tạo kiến trúc (Goal-Backward).
   - Output: plan.md, must_haves.

6. **@speckit.tasks** — Breakdown thành atomic tasks (Task Anatomy).
   - Output: tasks.md.

7. **@speckit.analyze** — Kiểm tra tính nhất quán 360 độ.

## Success Criteria
- ✅ spec.md, plan.md, tasks.md tồn tại và nhất quán
- ✅ Không vi phạm Constitution
"""


def wf_01_constitution():
    return """---
description: Thiết lập/cập nhật Constitution (Source of Law)
---

# 📜 Constitution Setup

## Pre-conditions
- `.agent/` directory đã tồn tại (chạy `bro-agent init` trước)

## Steps

1. **@speckit.constitution** — Thu thập thông tin từ developer:
   - Tech stack (language, framework, DB)
   - Docker port range (mặc định 8900-8999)
   - Coding principles (VD: No hardcode, Docker-first)
   - Security requirements
2. Tạo/cập nhật `.agent/memory/constitution.md`
3. Validate: Mỗi section có ≥1 rule cụ thể

## Success Criteria
- ✅ `constitution.md` tồn tại với ≥4 sections
- ✅ Mỗi rule testable (không chung chung)
"""


def wf_02_specify():
    return """---
description: Tạo Feature Specification (spec.md)
---

# 📝 Feature Specification

## Pre-conditions
- `.agent/memory/constitution.md` tồn tại

## Steps

1. Developer mô tả feature bằng ngôn ngữ tự nhiên
2. **@speckit.specify** — Parse mô tả → tạo spec.md chuẩn hóa
3. Review output: spec.md phải có Overview, User Scenarios, Requirements, Success Criteria

## Success Criteria
- ✅ spec.md có ≥1 User Scenario
- ✅ Mỗi scenario có Actor + Action + Value
- ✅ Success Criteria là testable
"""


def wf_03_clarify():
    return """---
description: Giải quyết mơ hồ trong Specification
---

# 🔍 Ambiguity Resolution

## Pre-conditions
- `.agent/specs/[feature]/spec.md` tồn tại

## Steps

1. **@speckit.clarify** — Scan spec.md tìm ambiguity
2. Hỏi developer tối đa 3 câu CRITICAL (bảng A/B/C options)
3. Auto-fix MINOR issues
4. Update spec.md với `[CLARIFIED]` markers

## Success Criteria
- ✅ Không còn vague language trong spec.md
- ✅ Mọi boundary conditions defined
"""


def wf_04_plan():
    return """---
description: Tạo Technical Plan (plan.md)
---

# 🏗️ Technical Planning

## Steps

1. **@speckit.plan** — Chuyển spec (WHAT) → plan (HOW):
   - Phase 0: Research unknowns.
   - Phase 1: Data model.
   - Phase 2: API contracts.
   - Phase 3: Architecture.
   - Phase 4: **Must-Haves (Goal-Backward)**.
2. **GATE**: So sánh plan vs constitution.
"""


def wf_05_tasks():
    return """---
description: Tạo Task Breakdown (tasks.md)
---

# 📋 Task Breakdown

## Pre-conditions
- `.agent/specs/[feature]/plan.md` tồn tại
- `.agent/specs/[feature]/spec.md` tồn tại

## Steps

1. **@speckit.tasks** — Breakdown plan → atomic tasks
2. Verify:
   - Mỗi task ≤15 phút
   - Mỗi task có file path
   - Dependency ordering đúng
   - Phase structure đúng (Setup → Foundation → Features → Polish)

## Success Criteria
- ✅ tasks.md có ≥1 phase
- ✅ Mỗi task format: `- [ ] T001 [P] [USx] Description affecting path/file`
- ✅ Không task nào ảnh hưởng >3 files
"""


def wf_06_analyze():
    return """---
description: Phân tích tính nhất quán giữa artifacts
---

# 🔬 Consistency Analysis

## Pre-conditions
- spec.md, plan.md, tasks.md tồn tại

## Steps

1. **@speckit.analyze** — Cross-check 3 artifacts:
   - Mỗi User Scenario → có tasks?
   - Mỗi data model → có tasks?
   - Conflicts giữa plan và constitution?
2. Output: Gap Analysis table + Coverage Score

## Success Criteria
- ✅ Coverage Score ≥ 90%
- ✅ Không gaps CRITICAL
"""


def wf_07_implement():
    return """---
description: Triển khai code theo tasks (Anti-Regression)
---

# 🛠️ Implementation

## Steps

Cho MỖI task `- [ ]` trong tasks.md:

1. **@speckit.implement** — Thực thi IRONCLAD Protocols:
   - P1: Blast Radius Analysis.
   - P2: Strategy Selection.
   - P3: TDD (Repro fail first).
   - P4: Context Anchoring.
   - P5: Build Gate (tsc/build).
   - P6: **Deviation Rules** (Auto-fix bugs/missing).
2. Mark `- [X]` khi task pass **VÀ build gate pass**.
"""


def wf_08_checker():
    return """---
description: Chạy Static Analysis
---

# 🔍 Static Analysis

## Pre-conditions
- Code đã implement (≥1 task complete)

## Steps

// turbo-all

1. **TypeScript Compile Check** (CRITICAL):
   ```bash
   docker compose build 2>&1 | grep -iE "error|fail|TS[0-9]"
   ```
   Hoặc:
   ```bash
   docker compose exec topdeli-web npx tsc --noEmit
   docker compose exec topdeli-admin npx tsc --noEmit
   docker compose exec topdeli-api npx tsc --noEmit
   ```

2. **Dockerfile Integrity** — Kiểm tra COPY paths:
   - Verify mọi thư mục được COPY tồn tại (đặc biệt `public/`)
   - Verify CMD entrypoint khớp với build output structure
   - Verify KHÔNG có volume mount `.:/app` trong production/beta compose

3. **ENV Compliance** — Scan hard-coded values:
   ```bash
   grep -rn "http://localhost\\|http://127.0.0.1" apps/*/src/ --include="*.ts" --include="*.tsx" | grep -v "node_modules"
   grep -rn '|| "' apps/*/src/ --include="*.ts" --include="*.tsx" | grep -v "node_modules"
   ```

4. **Build-time Safety** — Verify SSG pages:
   ```bash
   grep -rn "await api\\.\\|await fetchApi" apps/*/src/app/sitemap.ts apps/*/src/app/*/page.tsx
   ```
   Mỗi kết quả PHẢI nằm trong try-catch block.

5. **Monorepo Type Contract** — @speckit.checker:
   - Cross-reference shared type exports vs component usage
   - Verify shared package exports match actual file structure

6. **Security Scan**:
   - Tìm `eval()`, `dangerouslySetInnerHTML`, exposed secrets
   - Docker compliance: ports trong range 8900-8999

7. **Output Report** → `.agent/memory/checker-report.md`

## Success Criteria
- ✅ TypeScript compile: 0 errors
- ✅ Docker build: thành công hoàn toàn
- ✅ 0 issues CRITICAL (🔴)
- ✅ Report file tồn tại
- ❌ Nếu có bất kỳ 🔴 CRITICAL → BLOCK deploy
"""


def wf_09_tester():
    return """---
description: Chạy Tests & Coverage
---

# 🧪 Testing & Coverage

## Pre-conditions
- Code đã implement

## Steps

1. **@speckit.tester** — Tạo test plan → viết tests → chạy → report
2. Target: Coverage ≥ 80%

## Success Criteria
- ✅ All tests pass
- ✅ Coverage ≥ 80%
- ✅ test-report.md tồn tại
"""


def wf_10_reviewer():
    return """---
description: Code Review
---

# 👀 Code Review

## Pre-conditions
- Code đã implement + tests pass

## Steps

1. **@speckit.reviewer** — Review code:
   - Spec compliance, error handling, security, performance
2. Verdict: APPROVE hoặc REQUEST CHANGES

## Success Criteria
- ✅ Verdict: APPROVE
- ✅ Mọi CRITICAL findings đã fix
"""


def wf_11_validate():
    return """---
description: Validate Implementation vs Spec
---

# ✅ Final Validation

## Pre-conditions
- Mọi tasks complete, tests pass, review approved

## Steps

// turbo-all

1. **Tasks Completion Check**:
   - Đọc `tasks.md` → mọi task phải `[X]`
   - Nếu còn `[ ]` hoặc `[/]` → ❌ BLOCKED

2. **TypeScript Build Gate** (CRITICAL):
   ```bash
   docker compose -f docker-compose.beta.yml build 2>&1 | tail -n 100
   ```
   Nếu build fail → ❌ BLOCKED, liệt kê errors

3. **Runtime Verification**:
   ```bash
   docker compose -f docker-compose.beta.yml up -d
   sleep 15
   docker compose -f docker-compose.beta.yml ps
   ```
   - Tất cả services phải `Up` (KHÔNG `Restarting`)
   - Nếu `Restarting` → chạy `docker compose logs <service>` → ❌ BLOCKED

4. **Health Check**:
   ```bash
   curl -s http://localhost:<web_port> | head -c 200  # Public Web
   curl -s http://localhost:<admin_port> | head -c 200  # Admin Panel
   curl -s http://localhost:<api_port>/health  # API
   ```
   Tất cả phải trả về 200

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
- ❌ Nếu BẤT KỲ step nào FAIL → BLOCKED (không được deploy)
"""


def wf_12_seo():
    return """---
description: Technical SEO Audit & Optimization
---

# 🔍 SEO Audit

## Pre-conditions
- Public pages đã implement
- `.agent/knowledge_base/seo_standards.md` tồn tại

## Steps

1. **@speckit.seo** — Audit:
   - Meta tags, headings, canonical, structured data
   - Core Web Vitals, crawlability
2. Output: Score 0-100 + issues list
3. Nếu score < 80 → fix issues → re-audit

## Success Criteria
- ✅ SEO Score ≥ 80
- ✅ 0 CRITICAL issues
"""


def wf_13_geo():
    return """---
description: GEO - Tối ưu cho AI Search (ChatGPT, Gemini, Perplexity)
---

# 🤖 GEO Audit

## Pre-conditions
- SEO Audit đã pass (score ≥ 80)

## Steps

1. **@speckit.geo** — Audit:
   - AI crawlability (llms.txt, SSR, JSON-LD)
   - E-E-A-T compliance
   - Content format, topic authority
2. Output: GEO report

## Success Criteria
- ✅ llms.txt tồn tại
- ✅ JSON-LD cho mọi content pages
- ✅ E-E-A-T signals present
"""


def wf_identity():
    return """---
description: Tạo/cập nhật Master Identity cho AI Agent
---

# 🆔 Identity Setup

## Pre-conditions
- `.agent/project.json` tồn tại (chạy `bro-agent init` trước)
- `.agent/memory/constitution.md` tồn tại (khuyến nghị)

## Steps

1. **@speckit.identity** — Thu thập thông tin:
   - Đọc `project.json` → project type, name
   - Đọc `constitution.md` → tech stack, principles
   - Scan codebase → patterns, conventions hiện có
2. Tạo/cập nhật `.agent/identity/master-identity.md`:
   - Persona + Core Capabilities
   - Soul (Core Beliefs): "bro-agent First", "Docker is the Law"
   - Project Context (auto-detected)
3. Nếu `web_public`/`fullstack` → thêm SEO & GEO Awareness section

## Success Criteria
- ✅ `master-identity.md` tồn tại
- ✅ Persona gắn chặt domain dự án (không chung chung)
- ✅ Core Beliefs bao gồm mandatory items
"""


def wf_devops():
    return """---
description: Docker Infrastructure & Port Allocation (ENV-first)
---

# 🐳 DevOps Infrastructure Setup

## Pre-conditions
- `.agent/memory/constitution.md` tồn tại
- Docker Desktop (local) hoặc Docker Engine (server) đã cài đặt

## Steps

// turbo-all

### Step 1: Xác định Environment
- Detect environment: **local** / **staging** / **beta** / **production**
- Đọc `constitution.md` → port range (mặc định 8900-8999)

### Step 2: Port Allocation (ENV-first) ⭐

**Quy tắc Port — LUÔN cấu hình qua ENV:**
- Port PHẢI được khai báo trong `.env` (local) hoặc server ENV (prod)
- `docker-compose.yml` đọc port từ ENV vars (`${PUBLIC_PORT}`, `${ADMIN_PORT}`, `${API_PORT}`)
- KHÔNG hard-code port number trong bất kỳ file nào

**Quy tắc quét port theo môi trường:**

| Môi trường | Docker đã chạy? | Hành động |
|---|---|---|
| **Local** | ❌ Chưa (lần đầu) | Quét `netstat -ano \| findstr 89` → chọn 3 ports trống liên tiếp |
| **Local** | ✅ Đã chạy | **BỎ QUA** quét — dùng ports hiện tại từ `.env` / docker |
| **Staging/Beta/Prod** | Bất kỳ | **LUÔN** quét lần đầu để cấu hình → ghi vào `.env` |

**Check Docker đã chạy (Local):**
```bash
docker compose ps --format json 2>$null
# Nếu có containers → Docker đã chạy → SKIP port scan
# Nếu trống/error → Docker chưa chạy → RUN port scan
```

**Port scan khi cần:**
```bash
netstat -ano | findstr 89
```
- Pattern: Public FE `N` → Admin FE `N+1` → Backend API `N+2`
- Ghi luôn vào `.env`:
  ```env
  PUBLIC_PORT=8920
  ADMIN_PORT=8921
  API_PORT=8922
  ```

### Step 3: Docker Compose (Local)
- Tạo/cập nhật `docker-compose.yml`:
  - Ports đọc từ ENV: `"${PUBLIC_PORT:-8920}:3000"`
  - Volume mounts cho hot-reload
  - Named volumes cho `node_modules`
  - Health checks cho mỗi service

### Step 4: Docker Compose (Production/Staging/Beta)
- Tạo/cập nhật `docker-compose.prod.yml` / `docker-compose.beta.yml`:
  - Multi-stage builds (builder → runner)
  - `USER node` hoặc `USER appuser` (KHÔNG chạy root)
  - Loại bỏ devDependencies trong final image
  - Alpine/Slim base images
  - Ports đọc từ ENV (KHÔNG hard-code)

### Step 5: Security Checklist
- `.dockerignore`: block `.env`, `.git`, `node_modules`
- KHÔNG hard-code secrets trong Dockerfile
- Chỉ EXPOSE ports cần thiết

### Step 6: Documentation
- Cập nhật `.agent/knowledge_base/infrastructure.md`
- Cập nhật `.env.example` với tất cả port vars

## Success Criteria
- ✅ Ports cấu hình qua ENV (không hard-code)
- ✅ `docker-compose.yml` hoạt động local
- ✅ `docker-compose.prod.yml` tuân thủ security checklist
- ✅ `.dockerignore` tồn tại và đầy đủ
- ✅ `.env.example` document tất cả port vars
- ✅ `infrastructure.md` cập nhật

## 🚫 Guard Rails
- KHÔNG dùng port ngoài dải 8900-8999
- KHÔNG hard-code port number — LUÔN ENV vars
- KHÔNG chạy `docker compose down -v` trên production
- KHÔNG hard-code credentials vào Dockerfile
- KHÔNG quét port khi Docker local đã chạy
"""


def wf_prepare():
    return """---
description: Prep Pipeline (Specify → Clarify → Plan → Tasks → Analyze) — không Implement
---

# 📋 Prep Pipeline

## Pre-conditions
- constitution.md tồn tại

## Steps
1. **@speckit.specify** — Tạo spec.md
2. **@speckit.clarify** — Resolve ambiguity
3. **@speckit.plan** — Tạo plan.md + data-model.md
4. **GATE**: Constitution compliance check
5. **@speckit.tasks** — Tạo tasks.md
6. **@speckit.analyze** — Verify consistency

## Success Criteria
- ✅ spec.md + plan.md + tasks.md tồn tại
- ✅ Coverage ≥ 90%, no constitution violations
- ⏸️ Dừng tại đây — KHÔNG implement
"""


def wf_util_checklist():
    return """---
description: Tạo/validate Requirements Checklist
---

# ✅ Requirements Checklist

## Steps
1. **@speckit.checklist** — Parse spec.md → tạo checklist
2. Link requirements → task IDs
3. Output: checklist.md

## Success Criteria
- ✅ Mỗi requirement linked đến ≥1 task
"""


def wf_util_content():
    return """---
description: Content Strategy & Readability Audit
---

# 📝 Content Audit

## Pre-conditions
- Content pages đã tạo

## Steps
1. **@speckit.content** — Audit heading, readability, multimodal, fact-density
2. Output: content-guidelines.md

## Success Criteria
- ✅ Mỗi page có 1 H1, hierarchy đúng
- ✅ Readability guidelines documented
"""


def wf_util_diff():
    return """---
description: So sánh Artifacts (Spec vs Implementation)
---

# 🔀 Artifact Comparison

## Steps
1. **@speckit.diff** — So sánh 2 versions/artifacts
2. Output: Added/Removed/Changed table + impact analysis

## Success Criteria
- ✅ Diff report generated
"""


def wf_util_migrate():
    return """---
description: Migrate Legacy Code — Reverse-engineer codebase hiện có
---

# 🔄 Legacy Migration

## Pre-conditions
- Existing codebase với source code
- constitution.md đã setup (target standards)

## Steps
1. **@speckit.migrate** — Scan codebase:
   - Detect languages, frameworks, dependencies
   - Reverse-engineer data models, routes
   - Tạo draft spec.md
   - Assess tech debt → migration-risk.md
2. Review findings với developer
3. Tiếp tục với `/02-speckit.specify` để thêm features mới

## Success Criteria
- ✅ Draft spec.md tạo từ existing code
- ✅ migration-risk.md với tech debt inventory
"""


def wf_util_quizme():
    return """---
description: Red Team - Đặt câu hỏi phản biện tìm edge cases
---

# 🎯 Red Team Quiz

## Pre-conditions
- spec.md + plan.md tồn tại

## Steps
1. **@speckit.quizme** — Challenge spec+plan:
   - Boundary, concurrency, failure, security, scale questions
   - Max 5 questions, interactive Q&A
2. Nếu phát hiện issues → update spec.md

## Success Criteria
- ✅ Tất cả edge cases đã addressed
"""


def wf_util_status():
    return """---
description: Hiển thị Progress Dashboard
---

# 📊 Progress Dashboard

## Steps
1. **@speckit.status** — Parse tasks.md → hiển thị:
   - Per-phase progress bars
   - Total completion %
   - Pending tasks list

## Success Criteria
- ✅ Dashboard displayed
"""


def wf_util_taskstoissues():
    return """---
description: Sync tasks.md → Issue Tracker
---

# 🔗 Issue Sync

## Pre-conditions
- tasks.md tồn tại

## Steps
1. **@speckit.taskstoissues** — Parse tasks → generate issue export
2. Output: issues-export.md (ready to copy to GitHub/GitLab)

## Success Criteria
- ✅ issues-export.md generated
- ✅ Mỗi task mapped thành 1 issue
"""


def wf_util_uiux():
    return """---
description: Thiết lập/cập nhật UI/UX Design System & Standards
---

# 🎨 UI/UX Standards Setup

## Pre-conditions
- `constitution.md` đã tồn tại (để biết tech stack)

## Steps

1. **@speckit.uiux** — Phân tích domain & tech stack
2. Đề xuất Brand Palette & Typography
3. Định nghĩa Spacing & Grid system
4. Thiết lập Core Components (Buttons, Cards, Inputs)
5. Output/Update: `.agent/knowledge_base/ui_ux_standards.md`

## Success Criteria
- ✅ `ui_ux_standards.md` tồn tại với đầy đủ các section Brand, Typography, Components.
- ✅ Thiết kế tuân thủ Mobile-first.
"""


def wf_debug():
    return """---
description: Chẩn đoán và sửa lỗi hệ thống chuyên sâu (Systematic Debugging)
---

# 🐞 Systematic Debugging Pipeline

## Steps
1. **@speckit.debug** — Phân tích lỗi và tìm Root Cause.
2. Tái hiện lỗi qua script/test.
3. Đề xuất và thực hiện Fix Plan.
"""


def wf_backlog():
    return """---
description: Quản lý Ý tưởng (Backlog) và quét nợ kỹ thuật (TODO/FIXME)
---

# 📋 Backlog Management

## Steps
1. **@speckit.backlog** — Quét codebase và cập nhật danh sách việc cần làm.
2. Phân loại và ưu tiên các hạng mục công việc.
"""


def wf_roadmap():
    return """---
description: Quản lý lộ trình cấp cao (Milestones) và chuyển giao giữa các Phase
---

# 🗺️ Project Roadmap

## Steps
1. **@speckit.roadmap** — Cập nhật và theo dõi các Phase/Milestone của dự án.
"""


def wf_map():
    return """---
description: Vẽ bản đồ kiến trúc và sơ đồ phụ thuộc của Codebase
---

# 🗺️ Codebase Mapping

## Steps
1. **@speckit.map** — Quét toàn bộ project và sinh tài liệu kiến trúc.
"""


def wf_uat():
    return """---
description: UAT Analyzer - Phân tích kết quả nghiệm thu thủ công và xử lý các khoảng cách (gaps) từ User.
---

# ✅ User Acceptance Testing (UAT)

## Steps
1. **@speckit.uat** — Thu thập feedback và tạo kế hoạch hoàn thiện tính năng.
"""


def wf_wordpress():
    return """---
description: WordPress Theme & Plugin Development Workflow
---

# WordPress Development

## Steps
1. **@speckit.wordpress** — Triển khai theme/plugin theo chuẩn WordPress chuyên nghiệp.
"""


# =============================================================================
# WORKFLOW TEMPLATE MAP — Complete mapping cho tất cả các workflows
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
}

