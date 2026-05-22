"""
Skill Templates - Nội dung SKILL.md chi tiết cho 22 skills.
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
   - **Soul (Core Beliefs)**: Phải bao gồm "bro-agent First" và "Docker is the Law".
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
| **Local** | ❌ Chưa (lần đầu) | Quét `netstat -ano \\| findstr 89` → chọn 3 ports trống liên tiếp |
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
description: UI/UX Architect - Định nghĩa Design System, UI Components, Spacing, Typography, Responsive Patterns.
role: UI/UX Architect
---

## 🎯 Mission
Thiết lập và quản lý tiêu chuẩn UI/UX "Pro Max" cho dự án, đảm bảo giao diện premium, chuyên nghiệp và nhất quán.

## 📥 Input
- `.agent/specs/[feature]/spec.md` (chứa User Scenarios)
- `.agent/memory/constitution.md` (tech stack constraints)
- Brand guidelines (logo, màu sắc từ developer)

## 📋 Protocol

### Phase 1: Brand Identity & Colors
- Định nghĩa bảng màu (Primary, Secondary, Accent, State Colors).
- Định nghĩa Typography (Font families, Font sizes cho Heading/Body).
- **Tránh màu generic** (red, blue, green nguyên bản). Dùng HSL hoặc palette bài bản.

### Phase 2: Spacing & Layout
- Định nghĩa Container max-width (7xl, 1280px, v.v.).
- Spacing system (Padding/Margin chuẩn: 4, 8, 16, 24, 32px).
- Responsive Grid system cho Mobile/Tablet/Desktop.

### Phase 3: Core Components Design
- **Buttons**: Các trạng thái default, hover, active, disabled.
- **Cards**: Shadow, border-radius, hover transitions.
- **Forms**: Input styles, error states, focus rings.
- **Badges/Tags**: Trạng thái Sale, Hot, New, v.v.

### Phase 4: Rich Aesthetics Directive
- Sử dụng Glassmorphism, Vibrancy, Gradients nếu phù hợp.
- Định nghĩa Micro-animations (framer-motion, CSS transitions).

## 📤 Output
- File: `.agent/knowledge_base/ui_ux_standards.md`
- File: `.agent/specs/[feature]/ui-specs.md` (cho từng tính năng)

## 🚫 Guard Rails
- KHÔNG sử dụng màu mặc định của trình duyệt.
- KHÔNG thiết kế quá phức tạp gây chậm performance.
- PHẢI ưu tiên Mobile-first design.
"""


# =============================================================================
# SKILL TEMPLATE MAP — Complete mapping cho tất cả 22 skills
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
}

