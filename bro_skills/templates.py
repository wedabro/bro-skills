"""
Templates - Aggregator for Document, Skill, Workflow, and Script templates.
Skill and Workflow templates are separated into their own files for easier maintenance.
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
[Brief description of the feature]

## 2. User Scenarios (Stories)
- **US1**: As a [user role], I want to [action], so that [value].

## 3. Functional Requirements
- FR01: [specific, measurable requirement]

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
[Describe the technical approach]

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
[Libraries to be added — MUST be in package.json]
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
- Every public page must have a meta title, description, and canonical URL.
- Structured Data (JSON-LD) is REQUIRED for product pages and articles.
- Optimize for AI Search (GEO): Content must be fact-dense, with cited sources.
- Provide an `llms.txt` file at root so AI crawlers understand site structure.
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
5. **bro-skills First**: All changes and operations must go through bro-skills workflows.
"""

def doc_constitution_template(use_docker=True, is_soft_rules=False):
    must_label = "REQUIRED" if not is_soft_rules else "RECOMMENDED"
    shall_label = "MUST" if not is_soft_rules else "SHOULD"
    forbidden_label = "FORBIDDEN" if not is_soft_rules else "RESTRICTED"

    docker_infra = f"""
## §1 Infrastructure (DOCKER-FIRST)
- **Docker-First Policy**: Use Docker by default for both Local and Production. DO NOT run `npm`/`node`/`python` directly on host.
- **Local**: Use `docker-compose.yml` for development.
- **Production**: Use `docker-compose.prod.yml` with Security Hardening.
- **Ports**: Only use port range **8900-8999**.
  - Public FE: `N` | Admin FE: `N+1` | Backend API: `N+2`
""" if use_docker else f"""
## §1 Environment (CUSTOM)
- **Project Infrastructure**: Specifically defined by requirements, not necessarily running in Docker.
- **Port**: Optional, based on targeted system availability.
"""

    return f"""# 📜 Project Constitution

## §0 bro-skills Protocol ({must_label})
- **{must_label}**: All development (Code), testing (Test), and deployment (Deploy Production) activities {shall_label} use `bro-skills`.
- **Pipeline**: Strictly adhere to the SDLC pipeline: Specify → Plan → Tasks → Implement.
- **Tools**: Only use workflows under `.agent/workflows` to execute tasks.
{docker_infra}
## §2 Security & Production Safety
- **{forbidden_label}**: Running `docker compose down -v` on Production.
- **{forbidden_label}**: Manual deployment ({shall_label} use workflows `/deploy-production` or `/deploy-staging`).
- **Confirmation**: Require user confirmation before Deep Clean, Deploy Prod, or Delete Data.
- **Runtime**: Production containers MUST NOT run as root.

## §3 Code Standards & ENV
- **{forbidden_label} hardcoding**: URLs, Tokens, Keys, Credentials, Endpoints, Default Text.
- **Sensitive variables**: {shall_label} use ENV (`.env` local, server ENV prod).
  - Prefix: `NEXT_PUBLIC_*`, `API_*`, `DB_*`.
- **Validate**: 
  - Critical variables: `throw new Error()` if missing.
  - Optional variables: `console.error()` if missing.
- **Documentation**: Must have a complete `.env.example` file.

## §4 Workflow & Scripting
- **Automation**: Create scripts when encountering errors or repetitive tasks.
- **Git**: Save scripts in `.agent/scripts` and commit them to version control.
- **Git Auto-Commit**: {shall_label} perform git commit & push immediately after completing any function or task according to Conventional Commits standards.
- **Update**: Update corresponding workflows after creating new scripts.

## §5 UI/UX & Anti-Slop (PREMIUM DESIGN)
- **{must_label}**: Use the `design-taste-frontend` skill or `/util-speckit.uiux` for UI design.
- **{forbidden_label}**: Using standard template-like UI patterns, default browser colors, or overused AI gradients/shadows.
- **Design System**: {shall_label} comply with Anti-Slop principles (Asymmetric layout, bento grids, Typography-first, Micro-interactions).
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

## 📋 Technical SEO Checklist (Required)
- [ ] Each page has a unique `<title>`, max 60 characters
- [ ] Each page has a `<meta description>`, max 160 characters
- [ ] Only one `<h1>` per page, standard heading hierarchy (H1 → H2 → H3)
- [ ] Canonical URL for every page to avoid duplicate content
- [ ] `sitemap.xml` automatically generated and submitted to Google Search Console
- [ ] `robots.txt` correctly configured (does not block CSS/JS)
- [ ] Image: descriptive `alt` text, lazy loading, WebP/AVIF format
- [ ] URL slug: lowercase, hyphens, no accents
- [ ] Mobile-first responsive design
- [ ] Core Web Vitals targets: LCP < 2.5s, INP < 200ms, CLS < 0.1

## 🤖 GEO (Generative Engine Optimization)
- [ ] File `llms.txt` at root domain
- [ ] Structured Data (JSON-LD) for Article, Product, FAQ, BreadcrumbList
- [ ] E-E-A-T signals: Author bio, source citations, publish/update dates
- [ ] Content format: short paragraphs, bullet points, numbered lists
- [ ] Fact-density: Each paragraph has ≥1 data point or citation
- [ ] FAQ sections matching "People Also Ask" queries
- [ ] Topic clusters: Internal linking between related posts

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
```
"""

def doc_ui_ux_standards_template():
    return """# 🎨 UI/UX Standards (Anti-Slop & Premium)

## 🌈 Brand Palette & Color Calibration
- **Anti-Default**: FORBIDDEN to use default browser colors (pure red/blue/green). FORBIDDEN to overuse "AI Purple" gradients.
- **Premium Consumer Ban**: Avoid AI default beige + brass/clay palettes unless explicitly requested. Use alternatives like Cold Luxury (silver-grey + chrome), Forest (deep green + bone), or Black and Tan.
- **1 Accent Rule**: Choose a single Accent color and use it consistently across the entire site.

## 🔡 Typography (Anti-Slop)
- **Display Font**: FORBIDDEN to use `Inter` as default for creative headings. Use `Geist`, `Satoshi`, `Cabinet Grotesk`, `Outfit`, or a project-specific font.
- **Serif Discipline**: DO NOT use Serif fonts as default unless brand requires editorial/luxury/vintage styles. Forbidden to mix serif and sans-serif fonts in the same heading.
- **Hierarchy**: H1 headings max 2 lines. Subtext max 20 words.

## 📏 Layout & Rhythm
- **Hero Section**: Limit top padding (max `pt-24` on desktop).
- **Anti-Center Bias**: Avoid boring centered Hero layout unless it's a manifesto page. Prefer Split Screen or Asymmetric layouts.
- **Eyebrow Restraint**: FORBIDDEN to overuse "eyebrow" headings. Max 1 eyebrow per 3 sections.
- **Bento Grid**: Bento grids must have rhythm. Number of cells must match content. No empty cells. Diversify cells (real images, gradients, text).
- **Zigzag Ban**: Max 2 consecutive sections using alternating image-text (zigzag) layouts.

## 🧱 Core Components (Atomic) & Accessibility
- **Buttons (CTAs)**:
  - FORBIDDEN to wrap button text on desktop. Button labels max 3 words (e.g., `Get Started`).
  - FORBIDDEN to have 2 CTAs with the same intent on the same page (choose only one label).
  - Minimum WCAG AA contrast ratio 4.5:1 (Do not use white text on light grey background).
- **Interactive UI States**:
  - Skeletal loaders for loading states (do not use generic spinners).
  - Tactile Feedback: Add `-translate-y-[1px]` or `scale-[0.98]` on `:active` states for a physical button feel.
- **Images**: REQUIRED to have real images (from image gen tools, Unsplash, Picsum). FORBIDDEN to use div fake screenshots.

## ✨ Micro-animations
- Use `framer-motion` or `gsap` intentionally.
- Animations must respect `prefers-reduced-motion`.
- FORBIDDEN to repeat marquee texts more than once per page.
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
# IDE RULES TEMPLATES - Standard formats for each IDE
# =============================================================================

def _core_rules_content(project_name="Project", use_docker=True, is_soft_rules=False, lang="dynamic"):
    """Core rules content - reused for all IDE rules."""
    must_label = "Strictly follow" if not is_soft_rules else "Should follow"
    shall_label = "must" if not is_soft_rules else "should"
    forbidden_label = "DO NOT" if not is_soft_rules else "Avoid"
    
    docker_rule = f"- Docker-First: All coding and app running activities {shall_label} take place in the container. {forbidden_label} run node/python on the host." if use_docker else "- Flexibility: Run app directly or via Docker based on project needs."
    port_rule = f"- Ports: Use port range 8900-8999. {must_label} retrieve port from environment variables (.env)." if use_docker else "- Ports: Use available ports on the system."

    # Language instruction generation
    l_lower = lang.strip().lower()
    if l_lower in ("vi", "vietnamese"):
        lang_instruction = "- Respond in Vietnamese."
    elif l_lower in ("en", "english"):
        lang_instruction = "- Respond in English."
    elif l_lower == "dynamic":
        lang_instruction = "- Respond in the language used by the user (supports Vietnamese and English)."
    else:
        lang_instruction = f"- Respond in {lang.strip().capitalize()}."

    return f"""Project: {project_name}

## 1. SUPREME ORDER
- {must_label} the `.agent/memory/constitution.md` file.
{docker_rule}
{port_rule}

## 2. bro-skills PROTOCOL
- Every task {shall_label} go through the process: Specify → Plan → Tasks → Implement.
- Use Workflows in `.agent/workflows/` and Skills in `.agent/skills/`.

## 3. LANGUAGE & CODE
{lang_instruction}
- 15-Minute Rule: Each task {shall_label} be atomic, ≤ 15 minutes, affecting ≤ 3 files.
- PowerShell 5.1+, separate commands with `;` ({forbidden_label} use `&&`).
- {forbidden_label} hardcoding URLs, Tokens, Keys. Use ENV vars (`.env`).

## 4. SAFETY
- {forbidden_label} run `docker compose down -v` on Production.
- Generate automatic scripts (`.agent/scripts/`) for recurring errors.
- Check logs immediately on error: `docker compose logs -f <service>`.
- **Auto-Commit**: MUST perform git commit & push immediately after completing any function or task according to Conventional Commits standards.

## 5. AGENTIC MODE SYNC (Antigravity Only)
- **Task Tracking**: Use `task_boundary` to synchronize status with `@speckit.tasks` (tasks.md).
- **Planning Artifacts**: Always create `implementation_plan.md` when making large changes (atomic > 3 files).
- **Verification**: After completing the task, use `walkthrough.md` to compare the results with `spec.md`.
"""


def doc_antigravity_rules_template(project_name="Project", use_docker=True, is_soft_rules=False, lang="dynamic"):
    """Antigravity IDE (Google) — .agent/rules/bro-skills.md"""
    return f"""---
trigger: always_on
glob: "**/*"
description: bro-skills Workspace Rules for {project_name} - ASF 3.3 Standard
---

# 🛡️ bro-skills Workspace Rules

{_core_rules_content(project_name, use_docker, is_soft_rules, lang)}
"""


def doc_cursor_rules_template(project_name="Project", use_docker=True, is_soft_rules=False, lang="dynamic"):
    """Cursor IDE — .cursor/rules/bro-skills.mdc (YAML frontmatter + markdown)"""
    return f"""---
description: bro-skills project rules for {project_name}
globs:
alwaysApply: true
---

# bro-skills Rules

{_core_rules_content(project_name, use_docker, is_soft_rules, lang)}
"""


def doc_windsurf_rules_template(project_name="Project", use_docker=True, is_soft_rules=False, lang="dynamic"):
    """Windsurf IDE (Codeium) — .windsurf/rules/bro-skills.md"""
    return f"""# bro-skills Rules

{_core_rules_content(project_name, use_docker, is_soft_rules, lang)}
"""


def doc_vscode_copilot_template(project_name="Project", use_docker=True, is_soft_rules=False, lang="dynamic"):
    """VS Code (GitHub Copilot) — .github/copilot-instructions.md"""
    return f"""# Copilot Instructions for {project_name}

{_core_rules_content(project_name, use_docker, is_soft_rules, lang)}

## References
- Constitution: `.agent/memory/constitution.md`
- Infrastructure: `.agent/knowledge_base/infrastructure.md`
- Workflows: `.agent/workflows/`
- Skills: `.agent/skills/`
"""


def doc_jetbrains_rules_template(project_name="Project", use_docker=True, is_soft_rules=False, lang="dynamic"):
    """JetBrains AI Assistant (PhpStorm, WebStorm, PyCharm) — .aiassistant/rules/bro-skills.md"""
    return f"""# bro-skills Rules for {project_name}

{_core_rules_content(project_name, use_docker, is_soft_rules, lang)}
"""


def doc_kiro_mcp_template():
    """Kiro IDE (AWS) — .kiro/settings/mcp.json (default scaffold, merge-safe)."""
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


def doc_kiro_steering_template(project_name="Project", lang="dynamic"):
    """Kiro IDE (AWS) — .kiro/steering/tech.md"""
    l_lower = lang.strip().lower()
    if l_lower in ("vi", "vietnamese"):
        lang_instruction = "- Respond in Vietnamese."
    elif l_lower in ("en", "english"):
        lang_instruction = "- Respond in English."
    elif l_lower == "dynamic":
        lang_instruction = "- Respond in the language used by the user (supports Vietnamese and English)."
    else:
        lang_instruction = f"- Respond in {lang.strip().capitalize()}."

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
{lang_instruction}

## Safety
- NEVER run `docker compose down -v` on Production.
- Always check logs on error: `docker compose logs -f <service>`.
"""


def doc_claude_md_template(project_name="Project", use_docker=True, is_soft_rules=False, lang="dynamic"):
    """Claude Code — CLAUDE.md (root)"""
    return f"""# {project_name}

{_core_rules_content(project_name, use_docker, is_soft_rules, lang)}

## Project Structure
- `.agent/memory/constitution.md` — Project Constitution (Source of Law)
- `.agent/identity/master-identity.md` — AI Persona & Soul
- `.agent/knowledge_base/` — Domain knowledge (infrastructure, data, API)
- `.agent/skills/` — AI skills (@mentions)
- `.agent/workflows/` — Automation workflows (/commands)
- `.agent/specs/` — Feature specifications
"""


def doc_agents_md_template(project_name="Project", use_docker=True, is_soft_rules=False, lang="dynamic"):
    """GitHub Copilot Coding Agent — AGENTS.md (root)"""
    return f"""# {project_name} — Agent Instructions

{_core_rules_content(project_name, use_docker, is_soft_rules, lang)}

## Build & Test
- Build: `docker compose build` (If using Docker)
- Run: `docker compose up -d` (If using Docker)
- Logs: `docker compose logs -f <service>`
- Stop: `docker compose down`
"""


# =============================================================================
# TEMPLATE MAPS
# =============================================================================

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
