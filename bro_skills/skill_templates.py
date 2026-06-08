"""
Skill Templates - Nội dung SKILL.md chi tiết cho 29 skills.
Nguyên tắc: Gọn nhưng đủ chính xác để AI biết làm gì, đọc gì, output gì, KHÔNG làm gì.
"""


def skill_identity():
    return """---
name: speckit.identity
description: Quản lý nhân cách và định hướng hành vi của AI cho dự án.
role: Persona Architect
---

## 🎯 Mission
Tạo và duy trì file `master-identity.md` — định nghĩa AI là ai trong context dự án này.

## 📥 Input
- `.agent/project.json` (project type, name)
- `.agent/memory/constitution.md` (tech stack, principles)
- Codebase scan results (nếu có)

## 📋 Protocol
1. Đọc `project.json` → xác định project type và domain.
2. Đọc `constitution.md` → trích xuất tech stack, principles, non-negotiables.
3. Phân tích codebase (nếu có) → xác định patterns và conventions đang dùng.
4. Tạo/cập nhật `.agent/identity/master-identity.md` với các sections:
   - **Persona**: Role + expertise domain. **BẮT BUỘC giao tiếp bằng Tiếng Việt**.
   - **Core Capabilities**: 3-5 khả năng chính.
   - **Collaboration Style**: Cách tương tác với developer.
   - **Soul (Core Beliefs)**: Phải bao gồm "bro-skills First" và "Docker is the Law".
   - **Project Context**: Tech stack, DB, Docker info (auto-detected).
5. Nếu project type là `web_public`/`fullstack` → thêm section SEO & GEO Awareness.

## 📤 Output
- File: `.agent/identity/master-identity.md`

## 🚫 Guard Rails
- KHÔNG tạo persona quá chung chung — phải gắn chặt với domain dự án.
- KHÔNG thêm capabilities mà project không dùng (VD: không nói ML nếu không có ML).
- KHÔNG sử dụng ngôn ngữ khác ngoài Tiếng Việt khi giao tiếp với User.
"""


def skill_devops():
    return """---
name: speckit.devops
description: Chuyên gia hạ tầng Docker & Security Hardening — Port ENV-first, dải 8900-8999.
role: DevOps Architect
---

## 🎯 Mission
Thiết lập và quản lý hệ thống Docker chuẩn hóa, bảo mật cho dự án.
Port PHẢI luôn cấu hình qua ENV vars — KHÔNG BAO GIỜ hard-code.

## 📥 Input
- `.agent/memory/constitution.md` (port range, security rules)
- Existing `Dockerfile`, `docker-compose.yml` (nếu có)
- `.env.example`

## 📋 Protocol

### 1. Port Allocation (ENV-first) ⭐

**LUÔN cấu hình port qua ENV:**
- `.env` file (local) hoặc server ENV (production)
- `docker-compose.yml` đọc: `"${PUBLIC_PORT:-8920}:3000"`
- KHÔNG hard-code port number trong bất kỳ file nào

**Quy tắc quét port theo môi trường:**

| Môi trường | Docker đã chạy? | Hành động |
|---|---|---|
| **Local** | ❌ Chưa (lần đầu) | Quét dải `8900-8999` bằng socket/helper → chọn 3 ports trống liên tiếp |
| **Local** | ✅ Đã chạy | **BỎ QUA** quét — dùng ports hiện tại từ `.env` / docker |
| **Staging/Beta/Prod** | Bất kỳ | **LUÔN** quét lần đầu để cấu hình → ghi vào `.env` |

**Check Docker đã chạy (Local):**
```bash
docker compose ps --format json 2>$null
# Có containers → SKIP port scan
# Trống/error → RUN port scan
```

- Pattern: Public FE `N` → Admin FE `N+1` → Backend API `N+2`

### 2. Local Docker (`docker-compose.yml`):
- Ports đọc từ ENV: `"${PUBLIC_PORT:-8920}:3000"`
- Volume mounts cho hot-reload code
- Named volumes cho `node_modules` (tránh host-container lock)
- Health checks cho mỗi service

### 3. Production Docker (`docker-compose.prod.yml`):
- Multi-stage builds (builder → runner)
- `USER node` hoặc `USER appuser` (KHÔNG chạy root)
- Loại bỏ devDependencies trong image final
- Alpine/Slim base images
- Ports đọc từ ENV (KHÔNG hard-code)

### 4. Security Checklist:
- `.dockerignore`: block `.env`, `.git`, `node_modules`
- Không hard-code secrets trong Dockerfile
- Chỉ EXPOSE ports cần thiết

### 5. Documentation:
- Cập nhật `.agent/knowledge_base/infrastructure.md` với kết quả
- Cập nhật `.env.example` với tất cả port vars

## 📤 Output
- Files: `Dockerfile`, `docker-compose.yml`, `docker-compose.prod.yml`, `.dockerignore`
- Config: `.env` (ports), `.env.example` (documented)
- Doc: `.agent/knowledge_base/infrastructure.md` (updated)

## 🚫 Guard Rails
- KHÔNG dùng port ngoài dải 8900-8999.
- KHÔNG hard-code port number — LUÔN dùng ENV vars.
- KHÔNG chạy `docker compose down -v` trên production.
- KHÔNG hard-code credentials vào Dockerfile.
- KHÔNG quét port khi Docker local đã chạy (có containers).
"""


def skill_analyze():
    return """---
name: speckit.analyze
description: Consistency Checker - Phân tích tính nhất quán giữa spec, plan, tasks.
role: Consistency Analyst
---

## 🎯 Mission
Đảm bảo spec.md, plan.md, tasks.md không mâu thuẫn và phủ hết requirements.

## 📥 Input
- `.agent/specs/[feature]/spec.md`
- `.agent/specs/[feature]/plan.md`
- `.agent/specs/[feature]/tasks.md`

## 📋 Protocol
1. **Coverage Check**: Mỗi User Scenario trong spec → phải có task(s) trong tasks.md.
2. **Conflict Check**: Plan nói dùng tech A nhưng tasks lại reference tech B → BÁO LỖI.
3. **Constitution Check**: So plan.md với constitution.md → phát hiện violations.
4. **Completeness Check**: Mỗi data model trong plan → phải có task tạo model + migration.
5. **Output bảng Gap Analysis**:
   ```
   | Spec Requirement | Plan Section | Task ID | Status |
   |------------------|-------------|---------|--------|
   | User login       | Auth flow   | T005    | ✅ OK  |
   | Payment          | -           | -       | ❌ GAP |
   ```
6. Tính Coverage Score: `(matched / total) × 100%`.

## 📤 Output
- Console: Gap Analysis table + Coverage Score
- File: `.agent/memory/analyze-report.md`

## 🚫 Guard Rails
- CHỈ báo cáo — KHÔNG tự ý sửa artifacts.
- Mỗi gap phải chỉ rõ artifact nào thiếu.
"""


def skill_checker():
    return """---
name: speckit.checker
description: Static Analysis Aggregator - Chạy static analysis trên codebase.
role: Static Analyst
---

## 🎯 Mission
Quét codebase phát hiện vi phạm coding standards, security issues, performance anti-patterns.
**PHẢI chạy actual commands** — không chỉ scan bằng mắt.

## 📥 Input
- Source code (toàn bộ `src/`, `app/`, `pages/`)
- `.agent/memory/constitution.md` (coding standards)
- `Dockerfile`, `docker-compose*.yml`

## 📋 Protocol

### Phase 1: TypeScript Compile Check (CRITICAL)
Đây là bước quan trọng nhất, PHẢI chạy trước mọi deploy:
```bash
# Trong Docker container hoặc local:
docker compose exec <service> npx tsc --noEmit
# Hoặc build thử:
docker compose build 2>&1 | grep -i "error\\|fail"
```
- Bắt: type mismatch, missing props, sai tên thuộc tính, import lỗi
- Mọi lỗi TS đều là 🔴 CRITICAL

### Phase 2: Dockerfile & Docker Compose Lint
```bash
# Kiểm tra mọi COPY source tồn tại
# Kiểm tra docker compose syntax:
docker compose -f docker-compose*.yml config --quiet
# Kiểm tra volume shadowing (CẤM dùng volumes cho production):
grep -A 5 "volumes:" docker-compose.prod.yml  # Phải KHÔNG có `. :/app`
```
- Volume mount `- .:/app` trong production → 🔴 CRITICAL
- COPY path không tồn tại → 🔴 CRITICAL
- Port ngoài 8900-8999 → 🟡 WARNING

### Phase 3: ENV Compliance
```bash
# Tìm hard-coded URLs/tokens:
grep -rn "http://localhost\\|http://127.0.0.1\\|https://" apps/*/src/ --include="*.ts" --include="*.tsx" | grep -v "node_modules\\|.next\\|schema.org"
# Tìm default text fallback:
grep -rn '|| "' apps/*/src/ --include="*.ts" --include="*.tsx" | grep -v "node_modules"
```

### Phase 4: Import Hygiene
- Tìm unused imports, circular dependencies
- Verify shared package exports match actual usage

### Phase 5: Build-time Safety (Next.js specific)
```bash
# Tìm SSG/SSR pages gọi API mà không có try-catch:
grep -rn "await api\\.\\|await fetchApi" apps/*/src/app/sitemap.ts apps/*/src/app/*/page.tsx
# Mỗi kết quả phải nằm trong try-catch block
```
- API call trong `generateStaticParams` / `sitemap()` không có try-catch → 🔴 CRITICAL

### Phase 6: Security Scan
- Tìm `eval()`, `dangerouslySetInnerHTML` (cần sanitize), SQL concatenation
- Tìm secrets/keys trong source code

### Phase 7: Monorepo Integrity
- Verify shared package exports khớp với imports
- Cross-reference types: mọi `entity.X` phải tồn tại trong interface

## 📤 Output
- File: `.agent/memory/checker-report.md`
- Format:
  ```
  ## 🔴 CRITICAL (N issues)
  - `apps/web/src/app/page.tsx:65` — Property 'category' does not exist on type 'Article'
  ## 🟡 WARNING (N issues)
  - `docker-compose.beta.yml:40` — Volume mount `.:/app` sẽ override built code
  ## 🟢 INFO (N issues)
  - ...
  ```

## 🚫 Guard Rails
- CHỈ báo cáo — KHÔNG tự sửa code.
- Mỗi finding phải có file path + line number cụ thể.
- **PHẢI chạy `tsc --noEmit` hoặc `docker compose build`** — scan bằng mắt KHÔNG ĐỦ.
- Nếu có 🔴 CRITICAL → kết luận FAIL, deploy KHÔNG được phép.
"""


def skill_checklist():
    return """---
name: speckit.checklist
description: Requirements Validator - Tạo và validate checklist từ spec.
role: Requirements Auditor
---

## 🎯 Mission
Trích xuất mọi functional requirement từ spec.md thành checklist có thể track được.

## 📥 Input
- `.agent/specs/[feature]/spec.md`
- `.agent/specs/[feature]/tasks.md` (nếu có)

## 📋 Protocol
1. Đọc spec.md → trích xuất mọi yêu cầu (từ User Scenarios + Success Criteria).
2. Tạo checklist format:
   ```markdown
   ## Functional Requirements
   - [ ] FR01: User có thể đăng ký tài khoản → T003, T004
   - [ ] FR02: User có thể đăng nhập → T005
   - [x] FR03: User có thể xem sản phẩm → T010 ✅
   ```
3. Nếu có tasks.md → link mỗi requirement đến task IDs.
4. Đánh status: ✅ Met / ❌ Not Met / ⚠️ Partial.

## 📤 Output
- File: `.agent/specs/[feature]/checklist.md`

## 🚫 Guard Rails
- Mỗi requirement PHẢI trích dẫn được từ spec.md (không tự bịa thêm).
"""


def skill_clarify():
    return """---
name: speckit.clarify
description: Ambiguity Resolver - Phát hiện và giải quyết mơ hồ trong spec.
role: Clarity Engineer
---

## 🎯 Mission
Scan spec.md → phát hiện chỗ mơ hồ → hỏi developer tối đa 3 câu → cập nhật spec.

## 📥 Input
- `.agent/specs/[feature]/spec.md`

## 📋 Protocol
1. Scan spec.md tìm:
   - **Vague language**: "nhanh", "nhiều", "dễ dùng", "tương tự", "v.v."
   - **Missing boundaries**: Không rõ min/max, pagination limits, file size limits
   - **Undefined error handling**: Khi X fail thì sao?
   - **Ambiguous actors**: "User" là ai? Admin? Guest? Registered?
2. Phân loại mỗi issue:
   - 🔴 **CRITICAL**: Ảnh hưởng kiến trúc, PHẢI hỏi developer
   - 🟡 **IMPORTANT**: Nên hỏi nhưng có thể đề xuất mặc định
   - 🟢 **MINOR**: Tự fix được (VD: thêm "tối đa 50 items" nếu thiếu)
3. Hỏi developer TỐI ĐA 3 câu CRITICAL, mỗi câu có bảng options:
   ```
   | Option | Mô tả | Impact |
   |--------|-------|--------|
   | A      | ...   | ...    |
   | B      | ...   | ...    |
   | C      | ...   | ...    |
   ```
4. Auto-fix các items 🟢 MINOR.
5. Cập nhật spec.md với clarifications → đánh dấu `[CLARIFIED]`.

## 📤 Output
- File: Updated `.agent/specs/[feature]/spec.md`

## 🚫 Guard Rails
- TỐI ĐA 3 câu hỏi — không hỏi quá nhiều.
- KHÔNG thay đổi intent gốc của spec.
"""


def skill_constitution():
    return """---
name: speckit.constitution
description: Governance Manager - Thiết lập & quản lý Constitution (Source of Law).
role: Governance Architect
---

## 🎯 Mission
Tạo và duy trì constitution.md — "luật tối cao" mà mọi agent phải tuân thủ.

## 📥 Input
- Developer cung cấp: tech stack, principles, constraints
- `.agent/knowledge_base/infrastructure.md` (nếu có)

## 📋 Protocol
1. Thu thập từ developer:
   - Tech stack (frameworks, DB, language)
   - Docker ports (trong range 8900-8999)
   - Coding principles (VD: No hardcode, API-first)
   - Security requirements
2. Tạo/cập nhật `.agent/memory/constitution.md` với sections BẮT BUỘC:
   - **§1 Infrastructure**: Docker-first policy, port allocation, environments
   - **§2 Security**: No root containers, no hardcoded secrets, multi-stage builds
   - **§3 Code Standards**: Language, naming conventions, ENV policy
   - **§4 Non-Negotiables**: Danh sách rules KHÔNG BAO GIỜ được vi phạm
   - **§5 Monorepo Rules** (nếu monorepo):
     - Shared Package Contract: type exports là source of truth
     - Build Independence: mỗi app phải compile độc lập
     - Package exports phải match actual file structure
   - **§6 Docker Deployment Rules**:
     - CẤM volume shadowing (`- .:/app`) trong production/beta
     - Dockerfile COPY paths phải tồn tại
     - CMD entrypoint phải match với build output
     - Next.js apps phải có thư mục `public/`
   - **§7 Build-time Safety** (nếu Next.js):
     - SSG pages (sitemap, generateStaticParams): API calls phải try-catch
     - fetchApi phải return null/empty nếu API_URL undefined
   - **§8 Pre-Deploy Checklist**:
     - `docker compose build` thành công
     - Tất cả services `Up` (không `Restarting`)
     - Health check: 200 OK
3. Validate: Mỗi section phải có ít nhất 1 rule cụ thể, không chung chung.

## 📤 Output
- File: `.agent/memory/constitution.md`

## 🚫 Guard Rails
- Constitution KHÔNG chứa implementation details (HOW) — chỉ chứa rules (WHAT).
- Mỗi rule phải testable (có thể verify bằng code/check).
"""


def skill_diff():
    return """---
name: speckit.diff
description: Artifact Comparator - So sánh sự khác biệt giữa các artifacts.
role: Diff Analyst
---

## 🎯 Mission
So sánh 2 versions của artifact → highlight thay đổi → đánh giá impact.

## 📥 Input
- 2 files hoặc 2 versions cần so sánh (spec, plan, tasks, code)

## 📋 Protocol
1. Đọc cả 2 versions.
2. So sánh section-by-section:
   - ➕ **Added**: Sections/requirements mới
   - ➖ **Removed**: Sections/requirements bị xóa
   - ✏️ **Changed**: Sections có nội dung thay đổi
3. Impact Analysis: Mỗi thay đổi ảnh hưởng artifact nào downstream?
   - VD: Thêm field trong spec → cần update plan → cần thêm tasks
4. Output bảng tóm tắt.

## 📤 Output
- Console: Diff summary table
- File: `.agent/memory/diff-report.md` (nếu cần lưu)

## 🚫 Guard Rails
- CHỈ so sánh và báo cáo — KHÔNG tự ý sửa artifacts.
"""


def skill_implement():
    return """---
name: speckit.implement
description: Code Builder (Anti-Regression) - Triển khai code theo tasks với IRONCLAD protocols.
role: Master Builder
---

## 🎯 Mission
Implement code theo tasks.md, tuân thủ IRONCLAD Protocols và **Deviation Rules** để tự vận hành khi gặp lỗi.

## 📋 Protocol

### IRONCLAD Protocols:
1. **Blast Radius**: Phân tích rủi ro dựa trên số lượng file ảnh hưởng.
2. **Strategy**: Chọn sửa trực tiếp hoặc Strangler Pattern.
3. **TDD**: Tạo script repro fail -> code -> pass.
4. **Context Anchoring**: Re-read constitution mỗi 3 tasks.
5. **Build Gate**: LUÔN chạy tsc/build sau mỗi task.

### Deviation Rules (Tự xử trí khi lệch hướng) ⭐
- **Bug detected**: Tự động sửa nếu nằm trong scope, hoặc tạo task mới nếu nghiêm trọng.
- **Missing Critical**: Nếu thiếu config/file quan trọng, tự động bổ sung ngay.
- **Blocker**: Nếu kẹt, tự thực hiện "Root Cause Analysis" trước khi hỏi người dùng.
- **Arch Change**: Nếu cần đổi kiến trúc, PHẢI hỏi người dùng.

### Self-Check Protocol
- Mọi task chỉ hoàn thành khi vượt qua Build Gate (không lỗi Type, không lỗi Docker).

## 🚫 Guard Rails
- KHÔNG commit code lỗi build.
- KHÔNG hard-code sensitive info.
"""


def skill_migrate():
    return """---
name: speckit.migrate
description: Legacy Code Migrator - Reverse-engineer codebase hiện có sang chuẩn SDD.
role: Migration Specialist
---

## 🎯 Mission
Scan legacy codebase → tạo spec + plan sơ bộ → đánh giá tech debt → đề xuất migration path.

## 📥 Input
- Existing codebase (source code, configs, DB schema)
- `.agent/memory/constitution.md` (target standards)

## 📋 Protocol
1. **Scan Phase**: Dùng ProjectScanner patterns để detect:
   - Languages, frameworks, dependencies
   - Data models (Prisma/SQL/Mongoose schemas)
   - API routes, pages, components
   - Docker setup (nếu có)
2. **Reverse-Engineer Spec**: Từ code → tạo draft `spec.md`:
   - Mỗi page/route → 1 User Scenario
   - Mỗi data model → 1 entity description
3. **Tech Debt Inventory** (`migration-risk.md`):
   - 🔴 Critical: Security holes, deprecated deps, no tests
   - 🟡 Important: Missing Docker, no CI/CD, inconsistent patterns
   - 🟢 Minor: Code style, naming conventions
4. **Migration Sequence**: Đề xuất thứ tự migrate (ít risk trước).

## 📤 Output
- `.agent/specs/migration/spec.md` (draft)
- `.agent/specs/migration/migration-risk.md`

## 🚫 Guard Rails
- KHÔNG refactor code trong bước này — chỉ phân tích và tạo tài liệu.
- KHÔNG xóa code cũ.
"""


def skill_plan():
    return """---
name: speckit.plan
description: Technical Planner - Tạo plan.md từ spec (data model, API contracts, research).
role: System Architect
---

## 🎯 Mission
Chuyển spec.md (WHAT) thành plan.md (HOW). Sử dụng tư duy **Goal-Backward** để đảm bảo kế hoạch dẫn trực tiếp tới Success Criteria.

## 📋 Protocol

### Phase 0: Research
- Scan spec → liệt kê unknowns ("NEEDS CLARIFICATION").
- Nghiên cứu giải pháp → ghi vào `research.md`.

### Phase 1: Data Model
- Từ entities trong spec → tạo `data-model.md`.
- Xác định relationships (1:N, N:N).

### Phase 2: API Contracts
- Từ User Scenarios → tạo `contracts/[entity].md`.

### Phase 3: Architecture
- Tạo `plan.md` với: Folder structure, Component hierarchy, State management, Docker topology.

### Phase 4: Must-Haves (Goal-Backward) ⭐
Xác định các thành phần bắt buộc để đạt được "Success Criteria":
- **Truths**: Các logic đúng đắn tuyệt đối.
- **Artifacts**: Các file/output then chốt.
- **Key Links**: Liên kết giữa các module.

### Gate Check
- So sánh plan vs constitution → BÁO LỖI nếu vi phạm rules.

## 🚫 Guard Rails
- KHÔNG viết code trong bước planning.
- PHẢI check constitution compliance.
"""


def skill_quizme():
    return """---
name: speckit.quizme
description: Logic Challenger (Red Team) - Đặt câu hỏi phản biện, tìm edge cases.
role: Red Team Analyst
---

## 🎯 Mission
Challenge spec + plan bằng câu hỏi edge-case, tìm lỗ hổng logic trước khi implement.

## 📥 Input
- `.agent/specs/[feature]/spec.md`
- `.agent/specs/[feature]/plan.md`

## 📋 Protocol
1. Đọc spec + plan → tìm assumptions ẩn (implicit assumptions).
2. Sinh TỐI ĐA 5 câu hỏi edge-case, mỗi câu thuộc 1 category:
   - **Boundary**: "Nếu user nhập 0 sản phẩm thì sao?"
   - **Concurrency**: "Nếu 2 người cùng mua sản phẩm cuối cùng?"
   - **Failure**: "Nếu payment gateway timeout?"
   - **Security**: "Nếu user sửa price trong request?"
   - **Scale**: "Nếu có 100K products, performance ra sao?"
3. Với mỗi câu hỏi → đề xuất giải pháp nếu developer confirm đó là vấn đề.
4. Interactive: Chờ developer trả lời → quyết định cần update spec không.

## 📤 Output
- Console: Interactive Q&A session
- File: `.agent/memory/quizme-findings.md` (nếu phát hiện issues)

## 🚫 Guard Rails
- TỐI ĐA 5 câu hỏi — không overwhelm developer.
- Câu hỏi phải THỰC TẾ, không hỏi edge case quá xa vời.
"""


def skill_reviewer():
    return """---
name: speckit.reviewer
description: Code Reviewer - Review code theo spec và best practices.
role: Code Reviewer
---

## 🎯 Mission
Review implementation code → đảm bảo đúng spec, bảo mật, hiệu năng.

## 📥 Input
- Source code (files đã implement)
- `.agent/specs/[feature]/spec.md` + `plan.md`
- `.agent/memory/constitution.md`

## 📋 Protocol
1. **Spec Compliance**: Code có implement đúng mọi requirement trong spec không?
2. **Error Handling**: Mọi API route có try-catch? Có return đúng error format?
3. **Security**: Tìm injection risks, missing auth checks, exposed secrets.
4. **Performance**: Tìm N+1 queries, await waterfalls, missing pagination.
5. **Constitution**: Code có vi phạm rules nào trong constitution.md?
6. **Output**: Verdict + table findings:
   ```
   | File:Line | Severity | Issue | Suggestion |
   |-----------|----------|-------|------------|
   | api/users.ts:45 | 🔴 | Missing auth | Add middleware |
   ```
7. Verdict: ✅ **APPROVE** hoặc ❌ **REQUEST CHANGES** (kèm danh sách cần fix).

## 📤 Output
- File: `.agent/memory/review-report.md`

## 🚫 Guard Rails
- KHÔNG tự fix code — chỉ review và đề xuất.
- Mỗi finding PHẢI có file:line cụ thể.
"""


def skill_specify():
    return """---
name: speckit.specify
description: Feature Definer - Tạo spec.md từ mô tả ngôn ngữ tự nhiên.
role: Domain Scribe
---

## 🎯 Mission
Chuyển mô tả ngôn ngữ tự nhiên → spec.md chuẩn hóa (WHAT, không phải HOW).

## 📥 Input
- Mô tả feature từ developer (text tự do)
- `.agent/memory/constitution.md` (constraints)

## 📋 Protocol
1. Đọc mô tả → trích xuất:
   - **Actors**: Ai tương tác? (User, Admin, System, Guest)
   - **Actions**: Làm gì? (CRUD, search, filter, export)
   - **Data**: Dữ liệu gì? (entities, fields, relationships)
   - **Constraints**: Giới hạn gì? (auth, permissions, limits)
2. Tạo `.agent/specs/[feature]/spec.md` với format BẮT BUỘC:
   ```markdown
   ---
   title: [Feature Name]
   status: DRAFT
   version: 1.0.0
   created: [date]
   ---
   ## 1. Overview
   [1-2 câu mô tả]

   ## 2. User Scenarios
   - **US1**: As a [actor], I want to [action], so that [value].
   - **US2**: ...

   ## 3. Functional Requirements
   - FR01: [requirement cụ thể, measurable]

   ## 4. Non-Functional Requirements
   - NFR01: Response time < 2s

   ## 5. Success Criteria
   - [ ] SC01: [testable criterion]
   ```
3. Mỗi User Scenario PHẢI có: Actor + Action + Value.
4. Mỗi Functional Requirement PHẢI measurable (có số liệu cụ thể).

## 📤 Output
- File: `.agent/specs/[feature]/spec.md`

## 🚫 Guard Rails
- KHÔNG viết implementation details (HOW) — chỉ mô tả WHAT.
- KHÔNG dùng technical jargon trong User Scenarios (business language).
- KHÔNG bỏ qua error cases — mỗi action phải có "khi thất bại thì sao?"
"""


def skill_status():
    return """---
name: speckit.status
description: Progress Dashboard - Hiển thị trạng thái tiến độ project.
role: Progress Tracker
---

## 🎯 Mission
Parse tasks.md → tính tiến độ → hiển thị dashboard trực quan.

## 📥 Input
- `.agent/specs/[feature]/tasks.md`

## 📋 Protocol
1. Parse tasks.md → đếm checkboxes:
   - `- [X]` = completed
   - `- [ ]` = pending
2. Nhóm theo Phase → tính % mỗi phase.
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
4. List tasks đang pending (tiếp theo cần làm).

## 📤 Output
- Console: Dashboard visualization

## 🚫 Guard Rails
- KHÔNG thay đổi tasks.md — chỉ đọc và báo cáo.
"""


def skill_tasks():
    return """---
name: speckit.tasks
description: Task Breaker - Tạo tasks.md atomic, có thứ tự dependency từ plan.
role: Execution Strategist
---

## 🎯 Mission
Chuyển plan.md thành danh sách tasks atomic, có thứ tự dependency, mỗi task ≤15 phút.

## 📥 Input
- `.agent/specs/[feature]/plan.md`
- `.agent/specs/[feature]/spec.md`

## 📋 Protocol
1. Đọc plan.md → breakdown mỗi component thành atomic tasks.
2. Format BẮT BUỘC cho mỗi task:
   ```
   - [ ] T001 [P] Setup project structure per plan.md
   - [ ] T002 [P] Create database schema in prisma/schema.prisma
   - [ ] T003 [P] [US1] Implement user registration API in src/api/auth.ts
   ```
   - `[P]`: Priority (blocking task)
   - `[US1]`: Link đến User Scenario
   - Path: File chính bị ảnh hưởng
3. Phase Structure BẮT BUỘC:
   - **Phase 1: Setup** — Project init, configs, boilerplate
   - **Phase 2: Foundation** — DB, auth, shared utilities (blocking)
   - **Phase 3+**: Mỗi User Story = 1 phase (theo priority từ spec)
   - **Final Phase: Polish** — Error handling, optimization, cleanup
4. Dependency Rules:
   - Task phụ thuộc task khác → phải đặt SAU.
   - Foundation tasks luôn ở Phase 2.
5. **15-Minute Rule**: Mỗi task ≤ 15 phút, ảnh hưởng ≤ 3 files.

## 📤 Output
- File: `.agent/specs/[feature]/tasks.md`

## 🚫 Guard Rails
- KHÔNG tạo task quá lớn (>3 files hoặc >15 phút).
- KHÔNG tạo task trùng lặp.
- Mỗi task PHẢI có file path cụ thể.
"""


def skill_taskstoissues():
    return """---
name: speckit.taskstoissues
description: Issue Tracker Syncer - Đồng bộ tasks.md sang issue tracker.
role: Issue Syncer
---

## 🎯 Mission
Parse tasks.md → tạo issues sẵn sàng import vào GitHub/GitLab/Jira.

## 📥 Input
- `.agent/specs/[feature]/tasks.md`

## 📋 Protocol
1. Parse mỗi task → extract: ID, title, description, phase, user story link.
2. Map sang issue format:
   ```markdown
   **Title**: T003 - Implement user registration API
   **Labels**: phase-2, us-1, backend
   **Description**:
   - File: `src/api/auth.ts`
   - Depends on: T002
   - Acceptance: User can register with email/password
   ```
3. Group issues theo Phase → tạo Milestones.
4. Output file `.agent/memory/issues-export.md`.

## 📤 Output
- File: `.agent/memory/issues-export.md`

## 🚫 Guard Rails
- KHÔNG tạo issue trên remote — chỉ generate file export.
"""


def skill_tester():
    return """---
name: speckit.tester
description: Test Runner & Coverage - Tạo test plan, viết tests, báo cáo coverage.
role: Test Engineer
---

## 🎯 Mission
Đảm bảo implementation có test coverage đầy đủ, chạy pass 100%.

## 📥 Input
- Source code (implemented files)
- `.agent/specs/[feature]/tasks.md` (completed tasks)
- `.agent/specs/[feature]/spec.md` (success criteria)

## 📋 Protocol
1. **Test Plan**: Từ tasks.md (completed) → list functions/routes cần test.
2. **Write Tests**: Cho mỗi function/route:
   - Happy path (input hợp lệ → output đúng)
   - Error path (input lỗi → error handling đúng)
   - Edge case (boundary values, empty, null)
3. **Run Tests**: `docker compose exec [service] npm test` hoặc tương đương.
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
5. Liệt kê tests failed với error details.

## 📤 Output
- Test files (theo convention: `*.test.ts`, `*.spec.ts`)
- File: `.agent/memory/test-report.md`

## 🚫 Guard Rails
- KHÔNG skip error path tests — phải test cả failing cases.
- KHÔNG mock quá nhiều — prefer integration tests cho API routes.
"""


def skill_validate():
    return """---
name: speckit.validate
description: Implementation Validator - Validate implementation vs spec tổng thể.
role: Validation Oracle
---

## 🎯 Mission
Kiểm tra TOÀN BỘ implementation có đáp ứng spec.md hay không — final gate trước deploy.

## 📥 Input
- Tất cả artifacts: spec.md, plan.md, tasks.md
- Source code (implementation)
- `.agent/memory/constitution.md`

## 📋 Protocol
1. **Tasks Completion**: Mọi task trong tasks.md đã `[X]`?
2. **Success Criteria**: Mọi SC trong spec.md đã đạt?
3. **Build Verification** (PHẢI chạy actual command):
   ```bash
   docker compose -f docker-compose.beta.yml build 2>&1 | tail -n 100
   ```
   Nếu fail → ❌ BLOCKED
4. **Runtime Verification** (PHẢI chạy actual command):
   ```bash
   docker compose -f docker-compose.beta.yml up -d
   sleep 15
   docker compose -f docker-compose.beta.yml ps
   ```
   - Tất cả services phải `Up` (KHÔNG `Restarting`)
   - Nếu `Restarting` → chạy `docker compose logs <service>` → ❌ BLOCKED
5. **Health Check** (PHẢI chạy actual command):
   ```bash
   curl -s http://localhost:<web_port> | head -c 200
   curl -s http://localhost:<api_port>/health
   ```
   Tất cả phải trả về 200
6. **Constitution Check**: Không vi phạm rules nào?
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
- Verdict: ✅ PASS hoặc ❌ FAIL (kèm danh sách blockers)

## 🚫 Guard Rails
- KHÔNG approve nếu còn task chưa complete.
- KHÔNG approve nếu build fail.
- KHÔNG approve nếu bất kỳ service nào `Restarting`.
- PHẢI chạy actual commands — không chỉ đọc code.
"""


def skill_seo():
    return """---
name: speckit.seo
description: Technical SEO Lead - Tối ưu Meta Tags, Sitemap, Core Web Vitals, Schema.org.
role: SEO Technical Lead
---

## 🎯 Mission
Đảm bảo mọi page public đạt chuẩn Technical SEO và sẵn sàng cho AI Search (GEO).

## 📥 Input
- Source code (pages, layouts, components)
- `.agent/knowledge_base/seo_standards.md` (checklist)

## 📋 Protocol

### Bước 1: Audit Technical SEO
- Mỗi page có `<title>` unique, ≤60 ký tự?
- Mỗi page có `<meta description>`, ≤160 ký tự?
- Heading hierarchy chuẩn (1 `<h1>` per page, H1→H2→H3)?
- Canonical URLs set cho mọi page?
- Structured Data (JSON-LD) đúng schema?

### Bước 2: Core Web Vitals
- LCP < 2.5s, INP < 200ms, CLS < 0.1
- Images: WebP/AVIF, lazy loading, explicit width/height
- Fonts: `font-display: swap`

### Bước 3: Crawlability
- `robots.txt` không block CSS/JS
- `sitemap.xml` auto-generate
- Internal linking structure hợp lý
- Custom 404 page

### Bước 4: Output
Report tại `.agent/memory/seo-audit-report.md`:
- Issues: 🔴 Critical / 🟡 Warning / 🟢 Info
- Fix suggestion cho mỗi issue
- Score tổng (0-100)

## 📤 Output
- File: `.agent/memory/seo-audit-report.md`

## 🔗 Handoffs
- `@speckit.geo`: Sau khi Technical SEO đạt → chuyển sang GEO audit
- `@speckit.implement`: Fix các issues được phát hiện
"""


def skill_geo():
    return """---
name: speckit.geo
description: GEO Strategist - Tối ưu cho AI Search (ChatGPT, Gemini, Perplexity).
role: GEO Strategist
---

## 🎯 Mission
Đảm bảo website được AI Search engines **trích dẫn** trong câu trả lời.

## 📥 Input
- Source code (content pages)
- `.agent/knowledge_base/seo_standards.md`

## 📋 Protocol

### Bước 1: AI Crawlability
- File `llms.txt` tại root domain?
- SSR/SSG cho content pages (KHÔNG CSR)?
- JSON-LD đầy đủ cho Article, Product, FAQ?

### Bước 2: E-E-A-T Compliance
- **Experience**: Nội dung thể hiện kinh nghiệm thực tế?
- **Expertise**: Author bio, credentials?
- **Authoritativeness**: Nguồn trích dẫn, data points?
- **Trustworthiness**: HTTPS, privacy policy, contact info?

### Bước 3: Content Format for AI
- Short paragraphs (2-3 câu)
- Bullet points, numbered lists
- Direct answers ở đầu mỗi section
- FAQ sections dạng "People Also Ask"
- Fact-dense: Mỗi đoạn ≥1 data point

### Bước 4: Topic Authority
- Topic clusters (pillar + supporting articles)
- Internal linking giữa bài cùng chủ đề

## 📤 Output
- File: `.agent/memory/geo-audit-report.md`

## 🔗 Handoffs
- `@speckit.content`: Tối ưu nội dung theo chuẩn GEO
"""


def skill_content():
    return """---
name: speckit.content
description: Content Architect - Heading Structure, Readability, Multimodal, Fact-density.
role: Content Strategist
---

## 🎯 Mission
Đảm bảo nội dung website đạt chuẩn cho cả người đọc VÀ AI search engines.

## 📥 Input
- Content pages (bài viết, sản phẩm, landing pages)
- `.agent/knowledge_base/seo_standards.md`

## 📋 Protocol

### Bước 1: Heading Structure
- Mỗi page chỉ 1 `<h1>` duy nhất
- Hierarchy: H1→H2→H3 (không nhảy cấp)
- Heading mô tả nội dung section cụ thể

### Bước 2: Readability
- Đoạn văn: Tối đa 3-4 câu
- Bullet points thay cho đoạn dài
- Highlight key terms (bold/italic)

### Bước 3: Multimodal Content
- Image: `alt` text mô tả chi tiết
- Video: Transcript hoặc description
- Tables: Responsive, có caption

### Bước 4: Fact-density
- Mỗi section ≥1 statistic/data point
- Trích dẫn nguồn khi đưa claims
- Quotes từ experts khi phù hợp

## 📤 Output
- File: `.agent/memory/content-guidelines.md`

## 🔗 Handoffs
- `@speckit.seo`: Validate SEO compliance sau khi optimize
"""


def skill_uiux():
    return """---
name: speckit.uiux
description: UI/UX Architect - Định nghĩa Design System Anti-Slop, UI Components, Spacing, Typography, Responsive Patterns.
role: UI/UX Architect
---

## 🎯 Mission
Thiết lập và quản lý tiêu chuẩn UI/UX "Pro Max" cho dự án, đảm bảo giao diện premium, chuyên nghiệp, độc đáo và TUYỆT ĐỐI không bị "AI slop" (tránh các thiết kế mặc định nhàm chán của AI).

## 📥 Input
- `.agent/specs/[feature]/spec.md` (chứa User Scenarios)
- `.agent/memory/constitution.md` (tech stack constraints)
- Brand guidelines (nếu có)

## 📋 Protocol

### Phase 0: Brief Inference (Read the Room)
- Phân tích dự án (SaaS, portfolio, public-sector) để định hình vibe.
- Xác định 3 thông số: `DESIGN_VARIANCE` (1-10), `MOTION_INTENSITY` (1-10), `VISUAL_DENSITY` (1-10).

### Phase 1: Brand Identity & Colors (Anti-Default)
- **Màu sắc**: CẤM dùng các màu mặc định (red, blue, green). CẤM lạm dụng "AI Purple / Blue glow". Dùng palette tinh tế như Cold Luxury, Forest, Black & Tan.
- **Typography**: CẤM dùng `Inter` và Serif làm mặc định cho mọi thứ. Dùng `Geist`, `Satoshi`, `Cabinet Grotesk` hoặc font sans-serif có gu.

### Phase 2: Spacing, Layout & Rhythm
- Hạn chế top padding của Hero (max `pt-24`). Hero tối đa 2 dòng tiêu đề.
- Áp dụng Anti-Center Bias: Tránh căn giữa Hero một cách nhàm chán.
- CẤM lạm dụng "eyebrow" (tiêu đề in hoa siêu nhỏ). Tối đa 1 eyebrow trên 3 sections.
- Bento Grid phải có nhịp điệu, không để ô trống, đa dạng hoá background của các ô (hình, gradient tinh tế, chữ).

### Phase 3: Core Components Design
- **Buttons**: Text không wrap dòng trên desktop. Contrast WCAG AA.
- **Cards**: Hạn chế shadow đen thui trên nền sáng. Không lồng card trong card.
- **Forms**: Label trên input, không dùng placeholder thay label.

### Phase 4: Rich Aesthetics Directive
- Tránh gradient AI rẻ tiền. Sử dụng Glassmorphism thực tế (backdrop-filter + 1px inner border) nếu hợp vibe.
- Interactive States: Skeletal loading (không dùng spinner chung chung), tactile feedback khi bấm (scale-98).

## 📤 Output
- File: `.agent/knowledge_base/ui_ux_standards.md`
- File: `.agent/specs/[feature]/ui-specs.md` (cho từng tính năng)

## 🚫 Guard Rails
- KHÔNG sử dụng màu mặc định của trình duyệt.
- KHÔNG dùng mix Serif và Sans-serif trong cùng một headline.
- KHÔNG dùng 2 CTA có cùng mục đích (cùng intent) trên cùng một trang.
- BẮT BUỘC ưu tiên Mobile-first design.
"""


def skill_backend():
    return """---
name: speckit.backend
description: Backend/API Developer - Xay dung API service, business logic, auth, integration theo API standards.
role: Backend Engineer
---

## 🎯 Mission
Xây dựng backend/API production: endpoint chuẩn REST/GraphQL, business logic tách lớp, auth/authz chắc, integration ổn định. Khớp `knowledge_base/api_standards.md`.

## 📥 Input
- `.agent/specs/[feature]/spec.md` + `plan.md` (data model, API contracts)
- `.agent/knowledge_base/api_standards.md`, `data_schema.md`
- `.agent/memory/constitution.md` (Docker-First, ENV, Port 8900-8999)

## 📋 Protocol

### 1. API Layer
- Tuân thủ `api_standards.md`: versioning (`/v1`), naming, status codes, error envelope nhất quán.
- Validation input ở biên (DTO/schema). Reject sớm, message rõ.
- Pagination/filtering/sorting chuẩn hóa cho list endpoints.

### 2. Architecture (Layered)
- Tách `controller → service → repository`. KHÔNG để business logic trong controller.
- Dependency injection, không khởi tạo cứng dependency.
- Idempotency cho operations nhạy cảm (payment, create).

### 3. Auth & Security
- AuthN (JWT/session) + AuthZ (RBAC/policy) ở middleware.
- Parameterized query (chống SQLi). KHÔNG nối chuỗi SQL.
- Rate limiting + input sanitization cho public endpoints.

### 4. Data & Transaction
- Transaction boundary rõ ràng; rollback khi lỗi.
- N+1 query check; index theo `data_schema.md`.

### 5. Observability
- Structured logging (request id), health check endpoint, metrics cơ bản.
- Error handling tập trung, KHÔNG nuốt exception.

## 📤 Output
- API code + contract (OpenAPI/GraphQL schema).
- Cập nhật `knowledge_base/api_standards.md` nếu thêm pattern.

## 🚫 Guard Rails
- KHÔNG hard-code URL/secret/port → ENV (`API_*`, `DB_*`).
- KHÔNG trả raw error/stacktrace ra client.
- KHÔNG bỏ qua authz check trên endpoint nhạy cảm.
- KHÔNG để endpoint public không auth mà không cảnh báo.
- Phản hồi bằng Tiếng Việt.
"""


def skill_frontend():
    return """---
name: speckit.frontend
description: Frontend Developer - Xay dung UI components, state management, data fetching, accessibility, performance (Anti-Slop).
role: Frontend Engineer
---

## 🎯 Mission
Hiện thực hóa Design System (từ `@speckit.uiux`) thành code production: component tái sử dụng, state quản lý sạch, data fetching tối ưu, accessible & animation mượt mà chuẩn taste-skill.

## 📥 Input
- `.agent/knowledge_base/ui_ux_standards.md` (Design System)
- `.agent/specs/[feature]/spec.md` (UI requirements)
- API contract từ `@speckit.backend`
- `.agent/memory/constitution.md` (ENV, Docker-First, Port 8900-8999)

## 📋 Protocol

### 1. Component Architecture
- Component nhỏ, tái sử dụng, single responsibility. Viewport dùng `100dvh` thay vì `100vh` để tránh layout jump trên mobile.
- Theo Design System: spacing/typography/color tokens. Tuyệt đối không hardcode inline style trừ phi bắt buộc.

### 2. State & Data
- CẤM dùng `useState` cho các continuous values (vị trí chuột, scroll progress). Dùng `useMotionValue` / `useTransform` của Framer Motion / GSAP.
- Data fetching: BẮT BUỘC có Skeletal loader states (match với hình dáng UI cuối), không dùng circular spinner chung chung.

### 3. Accessibility (a11y) & UI Rules
- Semantic HTML, ARIA. BẮT BUỘC test contrast ratio (WCAG AA). Button CTA text phải dễ đọc trên nền button.
- Button text KHÔNG được rớt dòng (wrap) trên desktop. Label button ngắn gọn (max 3 từ).
- Tactile Feedback: thêm `active:scale-[0.98]` hoặc `-translate-y-[1px]` để tạo cảm giác bấm vật lý.

### 4. Motion & Performance
- Animate `transform` và `opacity` (hỗ trợ hardware acceleration). CẤM animate top/left/width/height liên tục.
- BẮT BUỘC tôn trọng `prefers-reduced-motion` nếu thêm animation phức tạp.
- GSAP / Framer Motion phải được clearup đúng lúc (tránh memory leak).

### 5. ENV & Config
- Dùng `NEXT_PUBLIC_*` cho client config. KHÔNG hard-code endpoint.

## 📤 Output
- UI component code + tests cơ bản (render/interaction).

## 🚫 Guard Rails
- KHÔNG hard-code text/URL/màu → dùng i18n/tokens/ENV.
- KHÔNG dùng 2 button CTA trùng mục đích trên một màn hình.
- KHÔNG vi phạm a11y (thiếu label, button chữ trắng trên nền sáng).
- Phản hồi bằng Tiếng Việt.
"""


def skill_database():
    return """---
name: speckit.database
description: Database Architect - Thiet ke schema, index, migration, query optimization, data integrity.
role: Database Architect
---

## 🎯 Mission
Thiết kế và tối ưu tầng dữ liệu: schema chuẩn hóa hợp lý, index hiệu quả, migration an toàn, query nhanh, toàn vẹn dữ liệu.

## 📥 Input
- `.agent/knowledge_base/data_schema.md`
- `.agent/specs/[feature]/spec.md` + `plan.md` (data model)
- `.agent/memory/constitution.md`

## 📋 Protocol

### 1. Schema Design
- Chuẩn hóa (3NF) mặc định; denormalize có chủ đích khi cần performance (ghi rõ lý do).
- Khóa chính/ngoại rõ ràng, constraint (NOT NULL, UNIQUE, CHECK) tại DB.
- Naming convention nhất quán; cập nhật `data_schema.md`.

### 2. Indexing & Performance
- Index theo query pattern thực tế (WHERE/JOIN/ORDER BY).
- Tránh over-indexing (chậm write). Composite index đúng thứ tự cột.
- Phát hiện & xử lý N+1, full table scan.

### 3. Migration (An toàn)
- Migration versioned, reversible (up/down).
- Zero-downtime pattern: expand → migrate → contract.
- KHÔNG destructive change trực tiếp trên production data mà không backup + xác nhận.

### 4. Integrity & Transaction
- Transaction isolation level phù hợp; tránh deadlock.
- Cascade rules cân nhắc kỹ; soft-delete khi cần audit.

### 5. Security
- Least-privilege DB user; KHÔNG dùng root/admin cho app.
- Encryption at-rest cho dữ liệu nhạy cảm; mask PII.

## 📤 Output
- Schema DDL + migration files.
- Cập nhật `knowledge_base/data_schema.md` (ERD, index list).

## 🚫 Guard Rails
- KHÔNG chạy migration destructive trên prod khi chưa backup + xác nhận.
- KHÔNG hard-code credential → ENV (`DB_*`).
- KHÔNG bỏ index trên FK / cột query nóng.
- KHÔNG lưu password plaintext (phải hash).
- Phản hồi bằng Tiếng Việt.
"""


def skill_ios():
    return """---
name: speckit.ios
description: iOS Developer - Native iOS (Swift/SwiftUI/UIKit), lifecycle, App Store compliance, Keychain.
role: iOS Engineer
---

## 🎯 Mission
Xây dựng app iOS native production: Swift + SwiftUI/UIKit, kiến trúc sạch, tuân thủ Human Interface Guidelines & App Store Review.

## 📥 Input
- `.agent/specs/[feature]/spec.md`
- `.agent/knowledge_base/ui_ux_standards.md`
- API contract từ `@speckit.backend`

## 📋 Protocol

### 1. Architecture
- Swift + SwiftUI (ưu tiên) hoặc UIKit. Pattern MVVM / TCA.
- Dependency injection; module hóa feature.

### 2. Lifecycle & State
- Scene/App lifecycle, background tasks, state restoration.
- `@State`/`@Observable` hoặc Combine cho reactive state.

### 3. Platform Integration
- Permission flow (camera, location, notification) đúng Info.plist + rationale.
- Push notification (APNs), deep linking (Universal Links).

### 4. Performance & UX
- 60/120fps, tránh main-thread blocking, lazy list.
- Safe area, Dynamic Type, Dark Mode, accessibility (VoiceOver).

### 5. Security & Compliance
- Token trong Keychain (KHÔNG UserDefaults).
- App Transport Security (HTTPS only).
- Tuân thủ App Store Review Guidelines + privacy nutrition label.

## 📤 Output
- Swift code + project config (xcconfig/ENV cho endpoint).

## 🚫 Guard Rails
- KHÔNG hard-code endpoint/key → xcconfig/ENV.
- KHÔNG lưu token vào UserDefaults/plaintext → Keychain.
- KHÔNG block main thread bằng I/O.
- KHÔNG bỏ qua privacy permission rationale.
- Phản hồi bằng Tiếng Việt.
"""


def skill_android():
    return """---
name: speckit.android
description: Android Developer - Native Android (Kotlin/Jetpack Compose), lifecycle, Play Store compliance, Keystore.
role: Android Engineer
---

## 🎯 Mission
Xây dựng app Android native production: Kotlin + Jetpack Compose, kiến trúc sạch, tuân thủ Material Design & Play Store Policy.

## 📥 Input
- `.agent/specs/[feature]/spec.md`
- `.agent/knowledge_base/ui_ux_standards.md`
- API contract từ `@speckit.backend`

## 📋 Protocol

### 1. Architecture
- Kotlin + Jetpack Compose (ưu tiên) hoặc View. Pattern MVVM / MVI + Clean Architecture.
- Hilt/Koin cho DI; module hóa theo feature.

### 2. Lifecycle & State
- Activity/Fragment lifecycle, `ViewModel` + `StateFlow`, config change survival.
- WorkManager cho background; Navigation Component.

### 3. Platform Integration
- Runtime permission flow đúng + rationale.
- Push (FCM), deep linking (App Links).

### 4. Performance & UX
- Tránh main-thread blocking (Coroutines/Dispatchers), lazy list (LazyColumn).
- Material Design 3, Dark theme, accessibility (TalkBack), đa screen size.

### 5. Security & Compliance
- Token trong EncryptedSharedPreferences/Keystore.
- Network security config (HTTPS), ProGuard/R8 obfuscation.
- Tuân thủ Play Store Data Safety + target SDK mới nhất.

## 📤 Output
- Kotlin code + Gradle config (BuildConfig/ENV cho endpoint).

## 🚫 Guard Rails
- KHÔNG hard-code endpoint/key → BuildConfig/ENV.
- KHÔNG lưu token plaintext → Keystore/EncryptedSharedPreferences.
- KHÔNG block main thread → Coroutines.
- KHÔNG bỏ qua runtime permission rationale.
- Phản hồi bằng Tiếng Việt.
"""


def skill_mobile():
    return """---
name: speckit.mobile
description: Mobile Developer - Cross-platform (React Native/Flutter), offline-first, lifecycle, store compliance.
role: Mobile Engineer
---

## 🎯 Mission
Xây dựng app mobile cross-platform production: React Native/Flutter, 1 codebase chạy iOS + Android, offline-first, tuân thủ store guidelines.

## 📥 Input
- `.agent/specs/[feature]/spec.md`
- `.agent/knowledge_base/ui_ux_standards.md`
- API contract từ `@speckit.backend`
- Framework target (RN/Flutter; HỎI nếu thiếu)

## 📋 Protocol

### 1. Framework & Architecture
- Xác định RN hoặc Flutter. Pattern (MVVM/Clean), navigation rõ ràng, deep linking.

### 2. Lifecycle & State
- App lifecycle (background/foreground), state restoration.
- State management (Redux/Riverpod/Bloc); permission flow đúng lúc.

### 3. Offline-First & Data
- Local storage (SQLite/Realm/AsyncStorage), sync strategy, conflict resolution.
- Cache + retry cho network kém.

### 4. Performance & UX
- 60 FPS scroll, virtualization list, tránh jank.
- Tối ưu app size, cold start; responsive + safe area.

### 5. Store Compliance & Security
- Tuân thủ App Store / Play Store guidelines.
- Secure storage cho token (Keychain/Keystore). KHÔNG plaintext.

## 📤 Output
- App code (RN/Flutter) + config build.

## 🚫 Guard Rails
- KHÔNG hard-code endpoint/key → ENV / secure config.
- KHÔNG lưu credential plaintext.
- KHÔNG block main/UI thread bằng I/O.
- KHÔNG bỏ qua permission rationale.
- Phản hồi bằng Tiếng Việt.
"""


def skill_data():
    return """---
name: speckit.data
description: Data/ML Engineer - Xay dung data pipeline (ETL/ELT), data quality, ML workflow, orchestration.
role: Data Engineer
---

## 🎯 Mission
Xây dựng data pipeline production: ingest → transform → load đáng tin cậy, data quality đảm bảo, ML workflow reproducible.

## 📥 Input
- `.agent/specs/[feature]/spec.md`
- `.agent/knowledge_base/data_schema.md`
- `.agent/memory/constitution.md` (Docker-First, ENV)

## 📋 Protocol

### 1. Pipeline Architecture
- Chọn model: batch (ETL/ELT) vs streaming. Orchestration (Airflow/Dagster/Prefect).
- Idempotent + re-runnable steps; checkpoint/state rõ ràng.
- Partition + incremental load thay vì full reload khi có thể.

### 2. Data Quality
- Schema validation tại biên ingest; reject/quarantine bad records.
- Data contract: type, null, range, uniqueness checks.
- Lineage + freshness monitoring.

### 3. Storage & Modeling
- Tách raw / staging / curated layers.
- Modeling theo `data_schema.md`; partition key + indexing hợp lý.

### 4. ML Workflow (nếu có)
- Tách feature engineering, training, inference.
- Reproducibility: seed, version data + model, track experiment.
- Tránh data leakage (train/test split đúng).

### 5. Reliability
- Retry + dead-letter cho step lỗi; alerting.
- Backfill strategy an toàn.

## 📤 Output
- Pipeline code + orchestration DAG/config.
- Cập nhật `knowledge_base/data_schema.md`.

## 🚫 Guard Rails
- KHÔNG hard-code connection string/credential → ENV (`DB_*`).
- KHÔNG full reload khi incremental khả thi.
- KHÔNG bỏ qua data validation → tránh silent corruption.
- KHÔNG để PII chưa mask trong log/output.
- Phản hồi bằng Tiếng Việt.
"""


def skill_security():
    return """---
name: speckit.security
description: Security Auditor - Audit AppSec theo OWASP, secret scanning, dependency/vuln, threat modeling.
role: Security Auditor
---

## 🎯 Mission
Đảm bảo bảo mật toàn vòng đời: audit code theo OWASP, phát hiện secret leak, quét lỗ hổng dependency, threat modeling cho feature nhạy cảm.

## 📥 Input
- Codebase + `.agent/specs/[feature]/spec.md`
- `.agent/memory/constitution.md` (§2 Security, §3 ENV)
- Dependency manifest (package.json, requirements.txt...)

## 📋 Protocol

### 1. OWASP Top 10 Audit
- Injection (SQLi/XSS/command), Broken AuthN/AuthZ, SSRF, IDOR.
- Insecure deserialization, security misconfiguration.
- Mỗi finding: severity + vị trí + fix đề xuất.

### 2. Secret & Config
- Quét hard-coded secret/key/token trong code + git history.
- Verify ENV usage theo Constitution §3; `.env` không commit.
- Kiểm tra `.dockerignore`, `.gitignore` block file nhạy cảm.

### 3. Dependency & Supply Chain
- Quét CVE dependency (npm audit / pip-audit / trivy).
- Phát hiện package typosquatting / unmaintained.
- Pin version (KHÔNG dùng range mở cho dep nhạy cảm).

### 4. AuthN / AuthZ
- Verify mọi endpoint nhạy cảm có authz check (chống IDOR).
- Token storage/expiry/rotation đúng; rate limiting.

### 5. Threat Modeling (feature nhạy cảm)
- STRIDE nhẹ: liệt kê asset, attack surface, mitigation.
- Production hardening: container non-root, port tối thiểu.

## 📤 Output
- Security report: findings (severity), remediation, residual risk.
- KHÔNG tự ý "fix" silently — báo cáo + đề xuất, fix sau khi xác nhận với owner.

## 🚫 Guard Rails
- KHÔNG echo giá trị secret ra response (chỉ tên key + vị trí).
- KHÔNG viết/gợi ý mã khai thác (PoC) gây hại — chỉ mô tả lỗ hổng + cách vá.
- KHÔNG bỏ qua finding nghiêm trọng dù ảnh hưởng tiến độ.
- KHÔNG gửi code/secret ra endpoint bên thứ ba.
- Phản hồi bằng Tiếng Việt.
"""


def skill_gamedev():
    return """---
name: speckit.gamedev
description: Game Developer - Chuyen gia phat trien game (engine, gameplay loop, physics, asset pipeline, netcode, performance).
role: Game Developer
---

## 🎯 Mission
Xây dựng game chuẩn production: gameplay loop ổn định, hiệu năng theo frame-budget, asset pipeline gọn, kiến trúc mở rộng được. Engine-agnostic (Unity/Unreal/Godot/Phaser/PixiJS/custom).

## 📥 Input
- `.agent/project.json` (project_type = `game`)
- `.agent/memory/constitution.md` (Docker-First, ENV, Port 8900-8999)
- `.agent/specs/[feature]/spec.md` (gameplay requirements)
- Engine target (từ spec hoặc hỏi developer nếu thiếu)

## 📋 Protocol

### Phase 1: Engine & Project Setup
- Xác định engine target. Nếu thiếu → HỎI trước khi code.
- Web game (Phaser/PixiJS/Babylon): chạy trong Docker (Node container), port dải 8900-8999.
- Native engine (Unity/Unreal/Godot): build/CI trong Docker nếu khả thi; editor chạy host được phép (ngoại lệ Docker-First, ghi rõ lý do).
- Cấu trúc: `assets/`, `scenes/`, `scripts/` (hoặc `src/`), `prefabs/`, `config/`.

### Phase 2: Core Architecture
- **Game Loop**: tách `update(dt)` (logic) khỏi `render()` (vẽ). Fixed timestep cho physics, variable cho render.
- **ECS / Component**: ưu tiên Entity-Component-System hoặc composition thay vì kế thừa sâu.
- **State Machine**: quản lý game states (Menu, Playing, Pause, GameOver) bằng FSM rõ ràng.
- **Event Bus**: giao tiếp giữa systems qua events, tránh coupling cứng.

### Phase 3: Performance Budget
- Đặt **frame budget**: 60 FPS = 16.6ms/frame (mobile/web 30 FPS = 33ms nếu cần).
- Object pooling cho bullets/enemies/particles — KHÔNG `new` trong vòng lặp game.
- Profiling: đo draw calls, GC spikes, physics cost. Ghi kết quả vào spec.
- Asset budget: texture atlas, nén audio, lazy-load scene.

### Phase 4: Asset Pipeline
- Tách asset source (raw) khỏi asset build (optimized).
- Naming convention nhất quán: `sfx_`, `tex_`, `mdl_`, `anim_`.
- Sprite atlas / texture packing cho 2D; LOD cho 3D.

### Phase 5: Netcode (nếu multiplayer)
- Chọn model: authoritative server vs P2P. Mặc định **server-authoritative** chống cheat.
- Client prediction + server reconciliation cho realtime.
- Endpoint/port từ ENV (`API_*`), KHÔNG hard-code.

### Phase 6: Game Feel & Testing
- Input buffering, coyote time, juice (screen shake, tween) khi spec yêu cầu.
- Test: unit test cho game logic thuần (damage calc, inventory); playtest checklist cho gameplay.
- Determinism: logic core phải reproducible (seed RNG).

## 📤 Output
- Source code game theo engine target.
- `config/` cho balance values (KHÔNG hard-code số liệu gameplay vào logic).
- Cập nhật `.agent/knowledge_base/` với architecture decisions (game loop, ECS, netcode).

## 🚫 Guard Rails
- KHÔNG hard-code: gameplay balance, asset paths, server URLs, keys → dùng config/ENV.
- KHÔNG cấp phát bộ nhớ (`new`/instantiate) trong hot loop → dùng pooling.
- KHÔNG block game loop bằng I/O đồng bộ → async load.
- KHÔNG trust client trong multiplayer → server validate.
- KHÔNG dùng asset không rõ license.
- Phản hồi developer bằng Tiếng Việt.
"""


def skill_debug():
    return """---
name: speckit.debug
description: Systematic Debugger - Chẩn đoán sự cố, tìm root cause độc lập và đề xuất fix plans.
role: Debugging Specialist
---

## 🎯 Mission
Sử dụng phương pháp luận khoa học để tìm ra nguyên nhân gốc rễ (root cause) của lỗi mà không làm nhiễu context chính của việc phát triển tính năng.

## 📋 Protocol

### Phase 1: Symptom Gathering (Thu thập triệu chứng)
Trước khi bắt đầu code, phải làm rõ:
- **Expected behavior**: Kết quả mong đợi là gì?
- **Actual behavior**: Kết quả thực tế đang xảy ra là gì?
- **Error messages**: Các log lỗi cụ thể (paste trực tiếp).
- **Reproduction**: Các bước cụ thể để tái hiện lỗi (bắt buộc).

### Phase 2: Isolation & Hypothesis (Cô lập & Giả thuyết)
- Tạo file `.agent/debug/[issue-slug].md` để lưu nhật ký điều tra.
- Đưa ra các giả thuyết (Hypotheses): "Có thể lỗi nằm ở hàm X vì Y".
- Sử dụng lệnh `grep`, `log` để kiểm chứng giả thuyết.

### Phase 3: Root Cause Found (Xác định nguyên nhân)
- Chỉ kết thúc điều tra khi tìm thấy dòng code/cấu hình cụ thể gây lỗi.
- Giải thích **TẠI SAO** nó lỗi thay vì chỉ nói **NÓ ĐANG LỖI**.

### Phase 4: Fix Proposal (Đề xuất sửa lỗi)
- Không sửa lỗi trực tiếp trong skill này.
- Đầu ra là một bản đề xuất sửa lỗi hoặc tạo một `gap_plan` để `speckit.implement` thực hiện.

## 🚫 Guard Rails
- KHÔNG đoán mò (No guessing). Mọi kết luận phải có bằng chứng từ log hoặc code.
- KHÔNG làm hỏng thêm code hiện tại trong quá trình debug (dùng công cụ Read-only là chính).
- PHẢI tạo file debug log để lưu vết.
"""


def skill_backlog():
    return """---
name: speckit.backlog
description: Backlog Manager - Quản lý Ý tưởng, Yêu cầu chờ xử lý và quét TODO/FIXME từ codebase.
role: Product Owner Assistant
---

## 🎯 Mission
Tổ chức và ưu tiên các yêu cầu chưa được thực hiện, đảm bảo không có ý tưởng hoặc lỗi nào bị bỏ sót trong quá trình phát triển dài hạn.

## 📋 Protocol

### Phase 1: Idea Scoping (Ghi nhận ý tưởng)
- Khi user đưa ra yêu cầu chưa muốn làm ngay, lưu vào `.agent/backlog/IDEAS.md`.
- Mỗi idea cần có: Mô tả, Độ ưu tiên (Low/Med/High), Trạng thái (Pending).

### Phase 2: Automated Todo Scan (Quét mã nguồn)
- Sử dụng lệnh `grep` để tìm các từ khóa: `TODO:`, `FIXME:`, `HACK:`, `BUG:`.
- Tổng hợp các kết quả tìm được vào `.agent/backlog/TECHNICAL_DEBT.md`.

### Phase 3: Backlog Grooming (Lọc backlog)
- Định kỳ review các item trong backlog để chuyển thành `spec.md` khi user sẵn sàng triển khai.

## 🚫 Guard Rails
- KHÔNG tự tiện xóa backlog mà chưa hỏi user.
- KHÔNG làm tràn context bằng việc list hàng nghìn TODO. Chỉ list các task liên quan đến khu vực đang làm việc.
"""


def skill_roadmap():
    return """---
name: speckit.roadmap
description: Roadmap Strategist - Quản lý lộ trình cấp cao (Milestones) và chuyển giao giữa các Phase.
role: Project Manager
---

## 🎯 Mission
Đảm bảo dự án đi đúng hướng theo tầm nhìn dài hạn, quản lý sự phụ thuộc giữa các giai đoạn (Phases) và cột mốc (Milestones).

## 📋 Protocol

### Phase 1: Milestone Definition
- Tạo/Cập nhật `.agent/ROADMAP.md`.
- Chia dự án thành các Milestone (Cột mốc lớn), ví dụ: MVP, Beta, Production Ready.
- Mỗi Milestone chứa danh sách các Phases.

### Phase 2: Progress Tracking
- Cập nhật trạng thái hoàn thành của từng Phase dựa trên kết quả từ `speckit.status`.
- Đảm bảo các yêu cầu (Requirements) được map đúng vào Milestone tương ứng.

### Phase 3: Transition Management (Chuyển giao)
- Khi một Phase kết thúc, kiểm tra các "nợ kỹ thuật" (debt) hoặc các phần chưa xong để chuyển sang Phase tiếp theo hoặc Phase Gap-closure.

## 🚫 Guard Rails
- PHẢI duy trì tính nhất quán giữa Roadmap và thực tế triển khai.
- CẤM bỏ qua các phase bắt buộc về bảo mật/devops trong roadmap.
"""


def skill_map():
    return """---
name: speckit.map
description: Codebase Mapper - Tự động phân tích cấu trúc dự án, vẽ biểu đồ phụ thuộc và viết tài liệu kiến trúc.
role: Technical Lead
---

## 🎯 Mission
Giúp Agent và User nhanh chóng hiểu được toàn bộ "bản đồ" của codebase, đặc biệt là các dự án cũ (Brownfield) hoặc dự án phức tạp.

## 📋 Protocol

### Phase 1: Structure Discovery (Quét cấu trúc)
- Quét toàn bộ thư mục bằng lệnh `tree` hoặc `ls -R`.
- Xác định các Tech Stack cốt lõi (frameworks, databases, libraries).

### Phase 2: Dependency Mapping (Sơ đồ phụ thuộc)
- Phân tích các lệnh `import` hoặc `require` để tìm sự phụ thuộc giữa các modules.
- Lưu kết quả vào `.agent/codebase/STRUCTURE.md`.

### Phase 3: Integration Inventory (Danh mục tích hợp)
- Liệt kê các service bên thứ 3 (API bên ngoài, DB connection).
- Lưu vào `.agent/codebase/INTEGRATIONS.md`.

## 📤 Output Artifacts
- `.agent/codebase/ARCHITECTURE.md`: Tổng quan kiến trúc.
- `.agent/codebase/CONVENTIONS.md`: Các quy ước code đang sử dụng.

## 🚫 Guard Rails
- KHÔNG đọc nội dung tất cả các file cùng lúc để tránh tràn context. Ưu tiên đọc header và exports.
- PHẢI cập nhật lại bản đồ sau mỗi đợt refactor lớn.
"""


def skill_uat():
    return """---
name: speckit.uat
description: UAT Analyzer - Phân tích kết quả nghiệm thu thủ công và xử lý các khoảng cách (gaps) từ User.
role: Quality Assurance
---

## 🎯 Mission
Cầu nối giữa trải nghiệm thực tế của người dùng và logic code, đảm bảo tính năng chạy đúng như kỳ vọng của khách hàng.

## 📋 Protocol

### Phase 1: UAT Intake (Tiếp nhận nghiệm thu)
- Thu thập phản hồi thủ công của User sau mỗi Phase.
- Ghi nhận vào `.agent/verification/[phase]-UAT.md`.

### Phase 2: Gap Analysis (Phân tích khoảng cách)
- So sánh kết quả thực tế User báo cáo với Spec.md ban đầu.
- Phân loại lỗi: UI Bug, Logic Bug, hay New Requirement.

### Phase 3: Restoration Plan (Kế hoạch vá lỗi)
- Tự động sinh ra danh sách Tasks để vá các "Gaps" vừa tìm thấy.
- Chuyển tiếp cho `speckit.implement` xử lý dưới dạng `--gaps-only`.

## 🚫 Guard Rails
- PHẢI phân biệt rõ giữa "Lỗi" và "Tính năng mới được yêu cầu thêm".
- CẤM đánh dấu hoàn thành Phase nếu User vẫn chưa Approve các tiêu chí UAT cốt lõi.
"""


def skill_wordpress():
    return """---
name: speckit.wordpress
description: WordPress Theme Architect - Chuyên gia phát triển theme, plugin và tối ưu hóa ecosystem WordPress.
role: WordPress Expert
---

## 🎯 Mission
Xây dựng các sản phẩm WordPress (Theme/Plugin) chuẩn industrial-grade, đảm bảo tính bảo mật, hiệu năng và khả năng mở rộng.

## 📋 Protocol

### Phase 1: Environment & Boilerplate
- **Docker-First**: LUÔN sử dụng môi trường Docker (MySQL + WordPress container).
- **Theme Structure**: Sử dụng `wp-content/themes/[theme-slug]`.
- **Assets Isolation**: Tách biệt Media assets (wp-data/assets) khỏi theme logic.

### Phase 2: Core Development Standard
- **Template Hierarchy**: Tuân thủ nghiêm ngặt hệ thống phân cấp file của WordPress (`index.php`, `single.php`, `page.php`, `archive.php`).
- **Hooks & Filters**: Ưu tiên sử dụng `add_action` và `add_filter` thay vì sửa trực tiếp vào core hoặc plugin.
- **Tailwind CSS Integration**: Sử dụng Tailwind cho frontend nếu user yêu cầu (Flatsome Child theme context).

### Phase 3: Content & Data Migration
- **WP-CLI**: Sử dụng wp-cli để import data, quản lý user, và cấu hình option.
- **Smart Media Import**: Tự động liên kết Media với Custom Post Types (Labs, Equipment) dựa trên slug.
- **ACF / Meta Box**: Định nghĩa Field Groups rõ ràng trong code hoặc JSON file.

### Phase 4: Security Hardening
- **Immutable Files**: Phân quyền 755/644, khóa `DISALLOW_FILE_MODS` trên Production.
- **Login Gating**: Giới hạn truy cập `/wp-admin` và `/wp-login.php`.
- **Malware Response**: Quy trình quét và reset `git reset --hard` nếu phát hiện backdoor.

## 🚫 Guard Rails
- KHÔNG sử dụng plugins "nulled" hoặc không rõ nguồn gốc.
- KHÔNG query trực tiếp database bằng SQL nếu có thể dùng `WP_Query` hoặc `get_posts`.
- KHÔNG hard-code domain/URL. Dùng `home_url()` hoặc `get_template_directory_uri()`.
- PHẢI escape đầu ra (`esc_html`, `esc_attr`) để tránh XSS.
"""


# =============================================================================
# SKILL TEMPLATE MAP — Complete mapping cho tất cả 38 skills
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
    # --- Process/utility skills (chi tiết, thay fallback) ---
    "speckit.debug": skill_debug,
    "speckit.backlog": skill_backlog,
    "speckit.roadmap": skill_roadmap,
    "speckit.map": skill_map,
    "speckit.uat": skill_uat,
    "speckit.wordpress": skill_wordpress,
}

