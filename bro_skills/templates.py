"""
Templates - Aggregator cho Document, Skill, Workflow, Script templates.
Skill và Workflow templates được tách ra file riêng để dễ maintain.
"""

from datetime import datetime
from .skill_templates import SKILL_TEMPLATE_MAP
from .workflow_templates import WORKFLOW_TEMPLATE_MAP


# =============================================================================
# DOCUMENT TEMPLATES
# =============================================================================

def doc_spec_template():
    return """---
title: Feature Specification
status: DRAFT
version: 1.0.0
---

# 📝 Specification: [FEATURE_NAME]

## 1. Overview
[Mô tả ngắn gọn về tính năng]

## 2. User Scenarios (Stories)
- **US1**: As a [user role], I want to [action], so that [value].

## 3. Functional Requirements
- FR01: [requirement cụ thể, measurable]

## 4. Non-Functional Requirements
- NFR01: Response time < 2s

## 5. Success Criteria
- [ ] SC01: [testable criterion]
"""

def doc_plan_template():
    return """---
title: Implementation Plan
status: DRAFT
depends_on: spec.md
---

# 🏗️ Implementation Plan: [FEATURE_NAME]

## 1. Technical Architecture
[Mô tả cách tiếp cận kỹ thuật]

## 2. Data Model Changes
```prisma/sql
```

## 3. API Contracts
- **Endpoint**: `POST /api/v1/...`
- **Body**: `{ field: type }`
- **Response**: `{ data: ..., meta: ... }`
- **Errors**: `400 | 401 | 404 | 500`

## 4. Folder Structure
```
src/
├── app/
├── components/
├── lib/
└── api/
```

## 5. Dependencies
[Thư viện cần thêm — PHẢI có trong package.json]
"""

def doc_tasks_template():
    return """# 📋 Task Registry

## 📊 Progress Overview
- [ ] Phase 1: Setup & Foundation (0%)
- [ ] Phase 2: Core Features (0%)
- [ ] Phase 3: Polish (0%)

## 🛠️ Tasks

### Phase 1: Setup
- [ ] T001 [P] Setup project structure per plan.md

### Phase 2: Core Features
- [ ] T002 [P] [US1] Implement feature per spec.md

### Phase 3: Polish
- [ ] T003 Error handling & edge cases
"""

def doc_identity_template(project_name="Project", project_type="fullstack", use_docker=True):
    type_labels = {
        "web_public": "Web Public (B2C)",
        "web_saas": "Web SaaS (B2B)",
        "mobile_app": "Mobile App",
        "desktop_cli": "Desktop / CLI Tool",
        "fullstack": "Full-stack (Web + API)",
        "simple_script": "Simple Script / Automation",
        "custom_infra": "Custom Infrastructure",
    }
    label = type_labels.get(project_type, "Full-stack")

    seo_section = ""
    if project_type in ("web_public", "fullstack", "web_saas"):
        seo_section = """
## 🔍 SEO & GEO Awareness
- Mọi page public phải có meta title, description, canonical URL.
- Structured Data (JSON-LD) là BẮT BUỘC cho các trang sản phẩm, bài viết.
- Tối ưu cho AI Search (GEO): Nội dung phải fact-dense, có nguồn trích dẫn.
- Cung cấp file `llms.txt` tại root để AI crawlers hiểu cấu trúc site.
"""

    docker_soul = "- Strictly follow Docker-First Policy." if use_docker else "- Flexibility-First: Infrastructure is project-specific."
    docker_belief = "1. **Docker is the Law**: Everything runs in containers." if use_docker else "1. **Environment is Custom**: Run code as per direct requirements."

    return f"""# 🧠 Master Identity: {project_name} Agent

## 🎭 Persona
You are the **Lead Architect & Senior Developer** for the **{project_name}** project.
Project Type: **{label}**
{docker_soul}
You follow **ASF 3.3** standards.

## 🛠️ Core Capabilities
- Internalizing complex business logic and mapping it to scalable code.
- Enforcing the **Project Constitution** in every action.
- Maintaining zero-regression standards through automated testing.
{seo_section}
## 🤝 Collaboration Style
- Proactive but cautious.
- Ask for clarification when ambiguity is detected.
- Provide "Blast Radius Analysis" before any major refactoring.

## 📜 Soul (Core Beliefs)
{docker_belief}
2. **Security is non-negotiable**: Production environments must be hardened.
3. **Spec-Driven**: No code without a plan.
4. **Context is King**: Never code without understanding the "Why".
5. **bro-skills First**: Mọi thay đổi và vận hành phải thông qua bro-skills workflows.
"""

def doc_constitution_template(use_docker=True, is_soft_rules=False):
    must_label = "BẮT BUỘC" if not is_soft_rules else "KHUYẾN NGHỊ"
    shall_label = "PHẢI" if not is_soft_rules else "NÊN"
    forbidden_label = "CẤM" if not is_soft_rules else "HẠN CHẾ"

    docker_infra = f"""
## §1 Infrastructure (DOCKER-FIRST)
- **Mặc định dùng Docker** cho cả Local và Production. KHÔNG chạy `npm`/`node`/`python` trực tiếp trên host.
- **Local**: Dùng `docker-compose.yml` để dev.
- **Production**: Dùng `docker-compose.prod.yml` kèm Security Hardening.
- **Ports**: Chỉ dùng dải **8900-8999**.
  - Public FE: `N` | Admin FE: `N+1` | Backend API: `N+2`
""" if use_docker else f"""
## §1 Environment (CUSTOM)
- **Hạ tầng dự án**: Được định nghĩa cụ thể theo từng nhu cầu, không nhất thiết chạy trong Docker.
- **Port**: Tùy chọn dựa trên sự sẵn có của hệ thống mục tiêu.
"""

    return f"""# 📜 Project Constitution

## §0 bro-skills Protocol ({must_label})
- **{must_label}**: Mọi hoạt động phát triển (Code), kiểm thử (Test), và triển khai (Deploy Production) {shall_label} sử dụng `bro-skills`.
- **Pipeline**: Tuân thủ nghiêm ngặt quy trình: Specify → Plan → Tasks → Implement.
- **Tools**: Chỉ sử dụng các workflows trong `.agent/workflows` để thực hiện task.
{docker_infra}
## §2 Security & Production Safety
- **{forbidden_label}**: `docker compose down -v` trên Production.
- **{forbidden_label}**: Deploy thủ công ({shall_label} dùng workflows `/deploy-production` hoặc `/deploy-staging`).
- **Xác nhận**: Yêu cầu xác nhận trước khi Deep Clean, Deploy Prod, hoặc Delete Data.
- **Runtime**: Production containers KHÔNG chạy quyền root.

## §3 Code Standards & ENV
- **{forbidden_label} hard-code**: URLs, Tokens, Keys, Credentials, Endpoints, Default Text.
- **Sensitive vars**: {shall_label} dùng ENV (`.env` local, server ENV prod).
  - Prefix: `NEXT_PUBLIC_*`, `API_*`, `DB_*`.
- **Validate**: 
  - Critical vars: `throw new Error()` nếu thiếu.
  - Optional vars: `console.error()` nếu thiếu.
- **Documentation**: Phải có `.env.example` đầy đủ.

## §4 Workflow & Scripting
- **Tự động hóa**: Tạo script khi gặp lỗi hoặc task lặp lại.
- **Git**: Lưu script vào `.agent/scripts`, commit vào hệ thống version control.
- **Update**: Cập nhật workflow tương ứng sau khi tạo script mới.
"""

def doc_infrastructure_template():
    return """# 🏗️ Infrastructure & Docker Standards

## 📂 Environment Mapping
- **Local**: `docker-compose.yml` (Hot-reload, Dev-tools)
- **Production**: `docker-compose.prod.yml` (Standalone, Hardened)
- **Beta/Staging**: [None - Create only on request]

## 🔒 Security Protocol
- Use `.env.example` for all sensitive variables.
- Production images use Alpine/Slim versions.
- Firewall rules: Only expose mapped ports 89XX.
"""

def doc_seo_standards_template():
    return """# 🔍 SEO & GEO Standards

## 📋 Technical SEO Checklist (Bắt buộc)
- [ ] Mỗi page có `<title>` unique, tối đa 60 ký tự
- [ ] Mỗi page có `<meta description>`, tối đa 160 ký tự
- [ ] Chỉ 1 `<h1>` per page, heading hierarchy chuẩn (H1 → H2 → H3)
- [ ] Canonical URL cho mọi page để tránh duplicate content
- [ ] `sitemap.xml` tự động generate và submit lên Google Search Console
- [ ] `robots.txt` cấu hình đúng (không block CSS/JS)
- [ ] Image: `alt` text mô tả, lazy loading, format WebP/AVIF
- [ ] URL slug: lowercase, dấu gạch ngang, không dấu tiếng Việt
- [ ] Mobile-first responsive design
- [ ] Core Web Vitals targets: LCP < 2.5s, INP < 200ms, CLS < 0.1

## 🤖 GEO (Generative Engine Optimization)
- [ ] File `llms.txt` tại root domain
- [ ] Structured Data (JSON-LD) cho Article, Product, FAQ, BreadcrumbList
- [ ] E-E-A-T signals: Author bio, nguồn trích dẫn, ngày publish/update
- [ ] Content format: short paragraphs, bullet points, numbered lists
- [ ] Fact-density: Mỗi đoạn văn ≥1 data point hoặc trích dẫn
- [ ] FAQ sections dạng "People Also Ask"
- [ ] Topic clusters: Liên kết nội bộ giữa bài viết cùng chủ đề

## 📊 Schema.org (JSON-LD Templates)

### Article
```json
{"@context":"https://schema.org","@type":"Article","headline":"...","author":{"@type":"Person","name":"..."},"datePublished":"...","image":"..."}
```

### Product
```json
{"@context":"https://schema.org","@type":"Product","name":"...","image":"...","offers":{"@type":"Offer","price":"...","priceCurrency":"VND"}}
```

### FAQ
```json
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"...","acceptedAnswer":{"@type":"Answer","text":"..."}}]}
```json
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"...","acceptedAnswer":{"@type":"Answer","text":"..."}}]}
```
"""

def doc_ui_ux_standards_template():
    return """# 🎨 UI/UX Standards (Pro Max)

## 🌈 Brand Palette
```typescript
colors: {
  primary: {
    DEFAULT: '#0048c4', // Update with brand primary
    dark: '#003399',
    light: '#3366ff',
  },
  accent: '#FFD700',
  success: '#10B981',
  error: '#EF4444',
  gray: {
    bg: '#f8fafc',
    border: '#e2e8f0',
  }
}
```

## 🔡 Typography (Inter/Sans)
- **H1 (Page Title)**: `text-3xl font-extrabold tracking-tight`
- **H2 (Section)**: `text-2xl font-bold`
- **H3 (Subtitle)**: `text-xl font-semibold`
- **Body**: `text-base leading-relaxed`
- **Small/Caption**: `text-sm text-gray-500`

## 📏 Spacing & Layout
- **Page Container**: `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`
- **Section Spacing**: `py-12 md:py-20`
- **Grid Gap**: `gap-6 md:gap-8`

## 🧱 Core Components (Atomic)

### Cards
- **Style**: `bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden`
- **Hover**: `hover:shadow-xl hover:-translate-y-1 transition-all duration-300`

### Buttons
- **Primary**: `bg-primary text-white px-6 py-3 rounded-xl font-bold hover:brightness-110 active:scale-95 transition-all`
- **Ghost**: `bg-transparent border border-gray-200 text-gray-700 hover:bg-gray-50 rounded-xl transition-colors`

### Inputs
- **Style**: `w-full px-4 py-3 bg-gray-50 border-transparent focus:bg-white focus:ring-2 focus:ring-primary/20 focus:border-primary rounded-xl transition-all`

## ✨ Micro-animations
- Sử dụng `framer-motion` cho các chuyển cảnh.
- Staggered children transitions (0.1s delay).
- Hover scale effect: `whileHover={{ scale: 1.02 }}`.

## ✅ UI/UX Checklist
- [ ] Tailwind class-first (No inline CSS).
- [ ] Mobile-first responsive grid.
- [ ] Accessible color contrast.
- [ ] Loading skeleton states cho async data.
- [ ] Smooth transitions cho mọi tương tác hover/click.
"""


# =============================================================================
# SCRIPT TEMPLATES
# =============================================================================

def script_create_feature():
    return """#!/bin/bash
# Create new feature branch + specs directory
set -e
FEATURE_NAME=${1:?"Usage: ./create-new-feature.sh <feature-name>"}
SPECS_DIR=".agent/specs/$FEATURE_NAME"
mkdir -p "$SPECS_DIR"
echo "✅ Created specs directory: $SPECS_DIR"
echo "📋 Next: Run /02-speckit.specify to create spec.md"
"""

def script_setup_plan():
    return """#!/bin/bash
# Locate feature spec for planning
set -e
FEATURE_NAME=${1:?"Usage: ./setup-plan.sh <feature-name>"}
SPEC_FILE=".agent/specs/$FEATURE_NAME/spec.md"
if [ ! -f "$SPEC_FILE" ]; then
  echo "❌ spec.md not found at $SPEC_FILE"
  echo "💡 Run /02-speckit.specify first"
  exit 1
fi
echo "✅ Found spec: $SPEC_FILE"
echo "📋 Next: Run /04-speckit.plan"
"""

def script_check_prerequisites():
    return """#!/bin/bash
# Verify prerequisite artifacts exist
set -e
FEATURE_NAME=${1:?"Usage: ./check-prerequisites.sh <feature-name>"}
SPECS_DIR=".agent/specs/$FEATURE_NAME"
ERRORS=0
for f in spec.md plan.md tasks.md; do
  if [ ! -f "$SPECS_DIR/$f" ]; then
    echo "❌ Missing: $SPECS_DIR/$f"
    ERRORS=$((ERRORS + 1))
  else
    echo "✅ Found: $SPECS_DIR/$f"
  fi
done
if [ $ERRORS -gt 0 ]; then
  echo "⚠️  $ERRORS prerequisite(s) missing"
  exit 1
fi
echo "✅ All prerequisites met"
"""

def script_update_context():
    return """#!/bin/bash
# Update agent context files after changes
set -e
echo "🔄 Updating agent context..."
if [ -f ".agent/memory/constitution.md" ]; then
  echo "✅ Constitution: OK"
else
  echo "⚠️  Constitution missing — run /01-speckit.constitution"
fi
if [ -d ".agent/identity" ]; then
  echo "✅ Identity: OK"
else
  echo "⚠️  Identity missing — run bro-skills init"
fi
echo "✅ Context update complete"
"""


# =============================================================================
# IDE RULES TEMPLATES — Chuẩn format cho từng IDE
# Research date: 2026-02-21
# =============================================================================

def _core_rules_content(project_name="Project", use_docker=True, is_soft_rules=False):
    """Nội dung rules chung — được tái sử dụng cho mọi IDE."""
    must_label = "Tuân thủ" if not is_soft_rules else "Nên tuân thủ"
    shall_label = "phải" if not is_soft_rules else "nên"
    forbidden_label = "KHÔNG" if not is_soft_rules else "Hạn chế"
    
    docker_rule = f"- Docker-First: Mọi hoạt động code và chạy app {shall_label} diễn ra trong container. {forbidden_label} chạy node/python trên host." if use_docker else "- Flexibility: Chạy app trực tiếp hoặc qua Docker tùy nhu cầu dự án."
    port_rule = f"- Ports: Sử dụng dải port 8900-8999. {must_label} lấy port từ biến môi trường (.env)." if use_docker else "- Ports: Sử dụng port khả dụng trên hệ thống."

    return f"""Dự án: {project_name}

## 1. PHÁP LỆNH TỐI CAO
- {must_label} nghiêm ngặt file `.agent/memory/constitution.md`.
{docker_rule}
{port_rule}

## 2. bro-skills PROTOCOL
- Mọi task {shall_label} đi qua quy trình: Specify → Plan → Tasks → Implement.
- Sử dụng Workflows trong `.agent/workflows/` và Skills trong `.agent/skills/`.

## 3. NGÔN NGỮ & CODE
- Phản hồi developer hoàn toàn bằng Tiếng Việt.
- 15-Minute Rule: Mỗi task {shall_label} atomic, ≤ 15 phút, ảnh hưởng ≤ 3 files.
- PowerShell 5.1+, ngăn cách lệnh bằng dấu `;` ({forbidden_label} dùng `&&`).
- {forbidden_label} hard-code URLs, Tokens, Keys. Dùng ENV vars (`.env`).

## 4. AN TOÀN
- {forbidden_label} chạy `docker compose down -v` trên Production.
- Tạo script tự động (`.agent/scripts/`) cho lỗi lặp lại.
- Kiểm tra logs ngay khi lỗi: `docker compose logs -f <service>`.

## 5. AGENTIC MODE SYNC (Antigravity Only)
- **Task Tracking**: Sử dụng `task_boundary` để đồng bộ trạng thái với `@speckit.tasks` (tasks.md).
- **Planning Artifacts**: Luôn tạo `implementation_plan.md` khi thực hiện các thay đổi lớn (atomic > 3 files).
- **Verification**: Sau khi hoàn thành task, sử dụng `walkthrough.md` để đối chiếu kết quả với `spec.md`.
"""


def doc_antigravity_rules_template(project_name="Project", use_docker=True, is_soft_rules=False):
    """Antigravity IDE (Google) — .agent/rules/bro-skills.md"""
    return f"""---
trigger: always_on
glob: "**/*"
description: bro-skills Workspace Rules cho {project_name} - ASF 3.3 Standard
---

# 🛡️ bro-skills Workspace Rules

{_core_rules_content(project_name, use_docker, is_soft_rules)}
"""


def doc_cursor_rules_template(project_name="Project", use_docker=True, is_soft_rules=False):
    """Cursor IDE — .cursor/rules/bro-skills.mdc (YAML frontmatter + markdown)"""
    return f"""---
description: bro-skills project rules for {project_name}
globs:
alwaysApply: true
---

# bro-skills Rules

{_core_rules_content(project_name, use_docker, is_soft_rules)}
"""


def doc_windsurf_rules_template(project_name="Project", use_docker=True, is_soft_rules=False):
    """Windsurf IDE (Codeium) — .windsurf/rules/bro-skills.md"""
    return f"""# bro-skills Rules

{_core_rules_content(project_name, use_docker, is_soft_rules)}
"""


def doc_vscode_copilot_template(project_name="Project", use_docker=True, is_soft_rules=False):
    """VS Code (GitHub Copilot) — .github/copilot-instructions.md"""
    return f"""# Copilot Instructions for {project_name}

{_core_rules_content(project_name, use_docker, is_soft_rules)}

## References
- Constitution: `.agent/memory/constitution.md`
- Infrastructure: `.agent/knowledge_base/infrastructure.md`
- Workflows: `.agent/workflows/`
- Skills: `.agent/skills/`
"""


def doc_jetbrains_rules_template(project_name="Project", use_docker=True, is_soft_rules=False):
    """JetBrains AI Assistant (PhpStorm, WebStorm, PyCharm) — .aiassistant/rules/bro-skills.md"""
    return f"""# bro-skills Rules for {project_name}

{_core_rules_content(project_name, use_docker, is_soft_rules)}
"""


def doc_kiro_mcp_template():
    """Kiro IDE (AWS) — .kiro/settings/mcp.json (scaffold mặc định, merge-safe).

    Trả về dict; generator sẽ MERGE vào file hiện có (không ghi đè server đã có).
    Server scaffold để disabled=true để user tự bật khi cần.
    """
    return {
        "mcpServers": {
            "fetch": {
                "command": "uvx",
                "args": ["mcp-server-fetch"],
                "env": {"FASTMCP_LOG_LEVEL": "ERROR"},
                "disabled": True,
                "autoApprove": [],
            }
        }
    }


def doc_kiro_steering_template(project_name="Project"):
    """Kiro IDE (AWS) — .kiro/steering/tech.md"""
    return f"""# Technology & Development Standards

Project: {project_name}
Build System: Docker (docker compose)
Port Range: 8900-8999
Shell: PowerShell 5.1+ (Windows)

## Development Protocol
- Follow Spec-Driven Development (SDD): Specify → Plan → Tasks → Implement.
- Specs directory: `.agent/specs/`
- Constitution: `.agent/memory/constitution.md`
- 15-Minute Rule: Each task must be atomic, ≤ 15 minutes, affecting ≤ 3 files.

## Environment
- Docker-First: All apps run inside containers. Never run npm/python on host directly.
- ENV vars required for all sensitive config (`.env` files).
- No hardcoded URLs, Tokens, Keys, or Credentials.

## Language
- Respond in Vietnamese (Tiếng Việt).

## Safety
- NEVER run `docker compose down -v` on Production.
- Always check logs on error: `docker compose logs -f <service>`.
"""


def doc_claude_md_template(project_name="Project", use_docker=True, is_soft_rules=False):
    """Claude Code — CLAUDE.md (root)"""
    return f"""# {project_name}

{_core_rules_content(project_name, use_docker, is_soft_rules)}

## Project Structure
- `.agent/memory/constitution.md` — Project Constitution (Source of Law)
- `.agent/identity/master-identity.md` — AI Persona & Soul
- `.agent/knowledge_base/` — Domain knowledge (infrastructure, data, API)
- `.agent/skills/` — AI skills (@mentions)
- `.agent/workflows/` — Automation workflows (/commands)
- `.agent/specs/` — Feature specifications
"""


def doc_agents_md_template(project_name="Project", use_docker=True, is_soft_rules=False):
    """GitHub Copilot Coding Agent — AGENTS.md (root)"""
    return f"""# {project_name} — Agent Instructions

{_core_rules_content(project_name, use_docker, is_soft_rules)}

## Build & Test
- Build: `docker compose build` (Nếu dùng Docker)
- Run: `docker compose up -d` (Nếu dùng Docker)
- Logs: `docker compose logs -f <service>`
- Stop: `docker compose down`
"""


# =============================================================================
# TEMPLATE MAPS — Re-exported from sub-modules + local definitions
# =============================================================================

# Re-export from sub-modules (for backward compat)
# SKILL_TEMPLATE_MAP imported from skill_templates
# WORKFLOW_TEMPLATE_MAP imported from workflow_templates

DOCUMENT_TEMPLATE_MAP = {
    "spec-template.md": doc_spec_template,
    "plan-template.md": doc_plan_template,
    "tasks-template.md": doc_tasks_template,
    "constitution-template.md": doc_constitution_template,
    "infrastructure-template.md": doc_infrastructure_template,
    "seo-standards-template.md": doc_seo_standards_template,
    "ui-ux-standards-template.md": doc_ui_ux_standards_template,
}

SCRIPT_TEMPLATE_MAP = {
    "create-new-feature.sh": script_create_feature,
    "setup-plan.sh": script_setup_plan,
    "check-prerequisites.sh": script_check_prerequisites,
    "update-agent-context.sh": script_update_context,
}

