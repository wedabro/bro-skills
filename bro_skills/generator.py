"""
Generator - Core logic tạo cấu trúc .agent/ chuẩn ASF 3.3.
Hỗ trợ lọc skills/workflows theo Project Type.
Tự động populate nội dung từ Scanner khi dự án có sẵn.
"""

import os
import stat
from datetime import datetime

from .registry import (
    SKILLS_REGISTRY, WORKFLOWS_REGISTRY, PROJECT_TYPES,
    get_skills_for_project_type, get_workflows_for_project_type,
    BASE_BUILDERS_BY_TYPE, MODIFIERS, resolve_builder_skills,
)
from .templates import (
    SKILL_TEMPLATE_MAP,
    WORKFLOW_TEMPLATE_MAP,
    SCRIPT_TEMPLATE_MAP,
    DOCUMENT_TEMPLATE_MAP,
    doc_identity_template,
    doc_seo_standards_template,
    doc_ui_ux_standards_template,
    doc_antigravity_rules_template,
    doc_cursor_rules_template,
    doc_windsurf_rules_template,
    doc_vscode_copilot_template,
    doc_jetbrains_rules_template,
    doc_kiro_steering_template,
    doc_kiro_mcp_template,
    doc_claude_md_template,
    doc_agents_md_template,
)
from .scanner import ProjectScanner


class ProjectGenerator:
    """Sinh cấu trúc .agent/ cho project theo chuẩn Spec-Kit & ASF 3.3."""

    def __init__(self, target_dir: str, project_name: str, project_type: str = "fullstack", scan_profile: dict = None, attributes: dict = None):
        self.target_dir = target_dir
        self.project_name = project_name
        self.project_type = project_type
        self.scan_profile = scan_profile  # Kết quả từ ProjectScanner
        self.attributes = attributes or {}  # Multi-agent attributes (architecture/platforms/flags)
        self.agent_dir = os.path.join(target_dir, ".agent")

        # Lọc skills/workflows theo project type + attributes (multi-agent v2)
        self.filtered_skills = get_skills_for_project_type(project_type, self.attributes)
        self.filtered_workflows = get_workflows_for_project_type(project_type)

        self.stats = {
            "skills": 0,
            "workflows": 0,
            "templates": 0,
            "scripts": 0,
            "directories": 0,
            "identity": 0,
            "knowledge": 0
        }

    def generate(self):
        """Thực thi toàn bộ quá trình sinh cấu trúc."""
        from .registry import get_project_type_info
        type_info = get_project_type_info(self.project_type)
        self.use_docker = type_info.get("use_docker", True)
        self.is_soft_rules = type_info.get("is_soft_rules", False)

        print(f"📁 Tạo cấu trúc thư mục (ASF 3.3 Standard — {self.project_type})...")
        self._create_directories()

        # ─── 0. Check Port (Chỉ cho dự án MỚI & dùng Docker) ───
        project_config_path = os.path.join(self.agent_dir, "project.json")
        is_new_project = not os.path.exists(project_config_path)

        if is_new_project and self.use_docker:
             ports = self._find_available_ports()
             if ports:
                 self.assigned_ports = ports
                 print(f"📡 Port assigned (8900-8999): Public:{ports[0]}, Admin:{ports[1]}, API:{ports[2]}")
                 self._save_ports_to_env(ports)
             else:
                 print("⚠️  Không tìm thấy dải port 8900-8999 trống. Vui lòng kiểm tra lại hệ thống.")
                 self.assigned_ports = (8900, 8901, 8902) # Fallback an toàn
        else:
             self.assigned_ports = None

        print("🎭 Thiết lập Identity & Soul...")
        self._create_identity()

        print("🧠 Khởi tạo Knowledge Base...")
        self._create_knowledge_base()

        print("🛠️ Tạo Skills (@mentions)...")
        self._create_skills()

        print("🔄 Tạo Workflows (/commands)...")
        self._create_workflows()

        print("🧭 Tạo Multi-Agent (registry + orchestrator)...")
        self._create_agents()

        print("📄 Tạo Templates & Memory...")
        self._create_templates()
        self._create_memory()

        print("🔧 Tạo Bash Scripts...")
        self._create_scripts()

        print("🖥️  Thiết lập Rules cho 8 IDE/Agent...")
        self._create_ide_rules()

        self._create_project_config()
        self._create_agent_readme()
        self._print_stats()

    def _create_ide_rules(self):
        """Tạo rules files chuẩn cho 8 IDE/Agent — đúng path + format từng IDE."""
        name = self.project_name

        # ─── 1. Antigravity (Google) ────────────────────────
        # Path: .agent/rules/bro-skills.md
        self._write_file(
            os.path.join(self.agent_dir, "rules", "bro-skills.md"),
            doc_antigravity_rules_template(name, self.use_docker, self.is_soft_rules)
        )
        print("  ✅ Antigravity  → .agent/rules/bro-skills.md")

        # ─── 2. Cursor ──────────────────────────────────────
        # Path: .cursor/rules/bro-skills.mdc (YAML frontmatter, .mdc extension)
        cursor_dir = os.path.join(self.target_dir, ".cursor", "rules")
        os.makedirs(cursor_dir, exist_ok=True)
        self._write_file(
            os.path.join(cursor_dir, "bro-skills.mdc"),
            doc_cursor_rules_template(name, self.use_docker, self.is_soft_rules)
        )
        print("  ✅ Cursor       → .cursor/rules/bro-skills.mdc")

        # ─── 3. Windsurf (Codeium) ──────────────────────────
        # Path: .windsurf/rules/bro-skills.md
        windsurf_dir = os.path.join(self.target_dir, ".windsurf", "rules")
        os.makedirs(windsurf_dir, exist_ok=True)
        self._write_file(
            os.path.join(windsurf_dir, "bro-skills.md"),
            doc_windsurf_rules_template(name, self.use_docker, self.is_soft_rules)
        )
        print("  ✅ Windsurf     → .windsurf/rules/bro-skills.md")

        # ─── 4. VS Code (GitHub Copilot) ────────────────────
        # Path: .github/copilot-instructions.md
        github_dir = os.path.join(self.target_dir, ".github")
        os.makedirs(github_dir, exist_ok=True)
        self._write_file(
            os.path.join(github_dir, "copilot-instructions.md"),
            doc_vscode_copilot_template(name, self.use_docker, self.is_soft_rules)
        )
        print("  ✅ VS Code      → .github/copilot-instructions.md")

        # ─── 5. JetBrains (PhpStorm, WebStorm, PyCharm) ────
        # Path: .aiassistant/rules/bro-skills.md
        jb_dir = os.path.join(self.target_dir, ".aiassistant", "rules")
        os.makedirs(jb_dir, exist_ok=True)
        self._write_file(
            os.path.join(jb_dir, "bro-skills.md"),
            doc_jetbrains_rules_template(name, self.use_docker, self.is_soft_rules)
        )
        print("  ✅ JetBrains    → .aiassistant/rules/bro-skills.md")

        # ─── 6. Kiro (AWS) ──────────────────────────────────
        # Path: .kiro/steering/tech.md
        kiro_dir = os.path.join(self.target_dir, ".kiro", "steering")
        os.makedirs(kiro_dir, exist_ok=True)
        self._write_file(
            os.path.join(kiro_dir, "tech.md"),
            doc_kiro_steering_template(name) # Kiro keeps original for now
        )
        print("  ✅ Kiro         → .kiro/steering/tech.md")

        # MCP config cho Kiro (merge-safe, không ghi đè server đã có)
        self._create_kiro_mcp()

        # Bridge skills cho Kiro auto-load (.kiro/skills → .agent/skills)
        self._create_kiro_skills_bridge()

        # ─── 7. Claude Code ─────────────────────────────────
        # Path: CLAUDE.md (root)
        self._write_file(
            os.path.join(self.target_dir, "CLAUDE.md"),
            doc_claude_md_template(name, self.use_docker, self.is_soft_rules)
        )
        print("  ✅ Claude Code  → CLAUDE.md")

        # ─── 8. GitHub Copilot Agent ────────────────────────
        # Path: AGENTS.md (root)
        self._write_file(
            os.path.join(self.target_dir, "AGENTS.md"),
            doc_agents_md_template(name, self.use_docker, self.is_soft_rules)
        )
        print("  ✅ GitHub Agent → AGENTS.md")


    def _create_kiro_mcp(self):
        """Tạo/merge .kiro/settings/mcp.json (merge-safe).

        - File chưa có → tạo mới với scaffold mặc định.
        - File đã có → CHỈ thêm server còn thiếu, KHÔNG ghi đè server/config hiện có.
        """
        import json

        mcp_path = os.path.join(self.target_dir, ".kiro", "settings", "mcp.json")
        os.makedirs(os.path.dirname(mcp_path), exist_ok=True)

        scaffold = doc_kiro_mcp_template()

        existing = {}
        if os.path.exists(mcp_path):
            try:
                with open(mcp_path, "r", encoding="utf-8") as f:
                    existing = json.load(f)
            except (json.JSONDecodeError, UnicodeDecodeError, OSError):
                existing = {}

        existing.setdefault("mcpServers", {})
        added = []
        for name, cfg in scaffold["mcpServers"].items():
            if name not in existing["mcpServers"]:
                existing["mcpServers"][name] = cfg
                added.append(name)

        self._write_file(mcp_path, json.dumps(existing, indent=2, ensure_ascii=False))
        if added:
            print(f"  ✅ Kiro MCP     → .kiro/settings/mcp.json (+{', '.join(added)})")
        else:
            print("  ✅ Kiro MCP     → .kiro/settings/mcp.json (giữ nguyên server hiện có)")

    def _create_kiro_skills_bridge(self):
        """Bridge .agent/skills → .kiro/skills để Kiro (AWS) auto-load skills.

        Format SKILL.md của bro-skills (frontmatter name + description) trùng
        chuẩn Kiro skill nên dùng trực tiếp. Ưu tiên symlink/junction (sync 2
        chiều, không nhân bản); fail thì fallback sang copy.
        """
        import shutil

        src = os.path.join(self.agent_dir, "skills")
        dst = os.path.join(self.target_dir, ".kiro", "skills")
        os.makedirs(os.path.dirname(dst), exist_ok=True)

        # Dọn link/dir cũ để tái tạo sạch
        if os.path.islink(dst) or os.path.isfile(dst):
            os.unlink(dst)
        elif os.path.isdir(dst):
            if os.name == "nt":
                # Junction được nhận diện là dir; xoá an toàn
                try:
                    os.rmdir(dst)
                except OSError:
                    shutil.rmtree(dst, ignore_errors=True)
            else:
                shutil.rmtree(dst, ignore_errors=True)

        rel_src = os.path.relpath(src, os.path.dirname(dst))

        # 1) POSIX: symlink tương đối
        if os.name != "nt":
            try:
                os.symlink(rel_src, dst, target_is_directory=True)
                print("  🔗 Kiro Skills  → .kiro/skills (symlink → .agent/skills)")
                return
            except (OSError, NotImplementedError):
                pass
        else:
            # 2) Windows: junction (không cần quyền admin)
            try:
                import subprocess
                subprocess.run(
                    ["cmd", "/c", "mklink", "/J", dst, src],
                    check=True, capture_output=True, text=True,
                )
                print("  🔗 Kiro Skills  → .kiro/skills (junction → .agent/skills)")
                return
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass

        # 3) Fallback: copy (mất sync 2 chiều)
        shutil.copytree(src, dst)
        print("  📄 Kiro Skills  → .kiro/skills (copy — symlink không khả dụng)")

    def _create_directories(self):
        """Tạo cấu trúc thư mục .agent/ theo chuẩn ASF 3.3."""
        dirs = [
            ".agent/identity",       # Tầng nhân cách
            ".agent/knowledge_base", # Tầng tri thức dự án
            ".agent/skills",         # Tầng kỹ năng (@skill)
            ".agent/workflows",      # Tầng điều hướng (/command)
            ".agent/scripts/bash",   # Tầng hạ tầng
            ".agent/templates",      # Tầng khuôn mẫu
            ".agent/memory",         # Tầng lưu trữ Constitution
            ".agent/rules",          # Tầng Rules cho Antigravity
            ".agent/codebase",       # Tầng bản đồ cấu trúc (speckit.map)
            ".agent/specs",          # Tầng Specification & Planning
            ".agent/agents",         # Tầng Multi-Agent (registry + orchestrator)
        ]

        for d in dirs:
            full_path = os.path.join(self.target_dir, d)
            os.makedirs(full_path, exist_ok=True)
            self.stats["directories"] += 1

    def _create_identity(self):
        """Tạo Master Identity — có nhận biết Project Type + thông tin scan."""
        filepath = os.path.join(self.agent_dir, "identity", "master-identity.md")
        content = doc_identity_template(self.project_name, self.project_type, self.use_docker)

        # Bổ sung context từ scanner
        if self.scan_profile and self.scan_profile.get("has_existing_code"):
            scanner = ProjectScanner(self.target_dir)
            scanner.profile = self.scan_profile
            context = scanner.generate_identity_context()
            if context:
                content += f"\n## 🔬 Project Context (Auto-detected)\n{context}\n"

        self._write_file(filepath, content)
        self.stats["identity"] += 1

    def _create_knowledge_base(self):
        """Tạo các file tri thức nền tảng — dùng scan data nếu có."""
        base_path = os.path.join(self.agent_dir, "knowledge_base")

        if self.scan_profile and self.scan_profile.get("has_existing_code"):
            # ĐỌC DỮ LIỆU THẬT TỪ SCANNER
            scanner = ProjectScanner(self.target_dir)
            scanner.profile = self.scan_profile

            print("  📖 Đang điền nội dung từ codebase thật...")

            self._write_file(
                os.path.join(base_path, "infrastructure.md"),
                scanner.generate_infrastructure_content()
            )
            self._write_file(
                os.path.join(base_path, "data_schema.md"),
                scanner.generate_data_schema_content()
            )
            self._write_file(
                os.path.join(base_path, "api_standards.md"),
                scanner.generate_api_standards_content()
            )
            self._write_file(
                os.path.join(base_path, "business_logic.md"),
                scanner.generate_business_logic_content()
            )
            self.stats["knowledge"] += 4
        else:
            # Dự án mới — dùng template placeholder
            infra_path = os.path.join(base_path, "infrastructure.md")
            infra_template = DOCUMENT_TEMPLATE_MAP.get("infrastructure-template.md")
            self._write_file(infra_path, infra_template())

            files = {
                "business_logic.md": "# Business Logic\n\nĐịnh nghĩa logic nghiệp vụ cốt lõi tại đây.",
                "data_schema.md": "# Data Schema\n\nĐịnh nghĩa cấu trúc database, quan hệ thực thể tại đây.",
                "api_standards.md": "# API Standards\n\nQuy tắc thiết kế API, error codes, auth headers.",
            }
            for name, content in files.items():
                self._write_file(os.path.join(base_path, name), content)
                self.stats["knowledge"] += 1

        # SEO & UI/UX Standards — CHỈ tạo cho Web projects
        type_info = PROJECT_TYPES.get(self.project_type, {})
        allowed_skills = type_info.get("includes_skills", [])
        
        if "web" in allowed_skills or "web_public" in allowed_skills:
            # SEO
            seo_path = os.path.join(base_path, "seo_standards.md")
            self._write_file(seo_path, doc_seo_standards_template())
            self.stats["knowledge"] += 1
            print("  🔍 SEO & GEO Standards → knowledge_base/seo_standards.md")

            # UI/UX
            uiux_path = os.path.join(base_path, "ui_ux_standards.md")
            self._write_file(uiux_path, doc_ui_ux_standards_template())
            self.stats["knowledge"] += 1
            print("  🎨 UI/UX Standards → knowledge_base/ui_ux_standards.md")

    def _create_skills(self):
        """Tạo SKILL.md cho mỗi skill — CHỈ tạo skills phù hợp project type."""
        for skill in self.filtered_skills:
            skill_name = skill["name"]
            skill_dir = os.path.join(self.agent_dir, "skills", skill_name)
            os.makedirs(skill_dir, exist_ok=True)
            skill_file = os.path.join(skill_dir, "SKILL.md")

            template_fn = SKILL_TEMPLATE_MAP.get(skill_name)
            if template_fn:
                content = template_fn()
            else:
                content = self._generate_basic_skill(skill)

            self._write_file(skill_file, content)
            self.stats["skills"] += 1

    def _generate_basic_skill(self, skill):
        return f"""---
name: {skill['name']}
description: {skill['description']}
role: {skill['role']}
---

## Role
Bạn là **{skill['role']}**.

## Task
{skill['description']}

## Execution Outline
1. Load context from `.agent/identity/master-identity.md`.
2. Check `.agent/memory/constitution.md` for rules.
3. Perform the primary task.
4. Report results.
"""

    def _create_workflows(self):
        """Tạo workflow .md files — CHỈ tạo workflows phù hợp project type."""
        for wf in self.filtered_workflows:
            cmd = wf["command"]
            filepath = os.path.join(self.agent_dir, "workflows", f"{cmd}.md")

            # Ưu tiên template chi tiết từ WORKFLOW_TEMPLATE_MAP
            template_fn = WORKFLOW_TEMPLATE_MAP.get(cmd)
            if template_fn:
                content = template_fn()
            else:
                # Fallback cho workflows không có template
                content = f"---\ndescription: {wf['description']}\n---\n\n# Workflow: {cmd}\n\n1. Run @{wf['skills'][0] if wf['skills'] else 'speckit.tasks'}"

            self._write_file(filepath, content)
            self.stats["workflows"] += 1

    def _create_agents(self):
        """Sinh .agent/agents/: registry.json + orchestrator.md (Multi-Agent v2)."""
        import json

        agents_dir = os.path.join(self.agent_dir, "agents")
        os.makedirs(agents_dir, exist_ok=True)

        active_skill_names = [s["name"] for s in self.filtered_skills]
        builder_names = resolve_builder_skills(self.project_type, self.attributes)

        registry = {
            "registry_version": "2.0.0",
            "asf_version": "3.3",
            "description": "Agent Registry v2 - Attribute-based. active = core + base[type] + modifiers[attr].",
            "project_type": self.project_type,
            "attributes": self.attributes,
            "active_agents": active_skill_names,
            "builder_agents": builder_names,
            "base_by_type": BASE_BUILDERS_BY_TYPE,
            "modifiers": MODIFIERS,
            "orchestration": {
                "entry": ".agent/agents/orchestrator.md",
                "selection_rule": "active = core + base_by_type[type] + flatten(modifiers[attr] for attr in attributes)",
                "fallback_project_type": "fullstack",
            },
        }
        self._write_file(
            os.path.join(agents_dir, "registry.json"),
            json.dumps(registry, indent=2, ensure_ascii=False),
        )
        self._write_file(
            os.path.join(agents_dir, "orchestrator.md"),
            self._orchestrator_content(active_skill_names, builder_names),
        )

    def _orchestrator_content(self, active_skill_names, builder_names):
        active_list = ", ".join(active_skill_names) if active_skill_names else "(none)"
        builder_list = ", ".join(builder_names) if builder_names else "(none)"
        return f"""---
name: orchestrator
description: Multi-Agent Orchestrator - Dieu phoi agent theo project_type + attributes va pipeline Specify->Plan->Tasks->Implement.
role: Lead Orchestrator
trigger: always_on
---

# 🧭 Multi-Agent Orchestrator

## 🎯 Mission
Điều phối nhiều agent chuyên biệt trong dự án **{self.project_name}** (`{self.project_type}`).
Quyết định agent nào xử lý task nào dựa trên `project_type` + `attributes` và giai đoạn pipeline.

## 📥 Input
- `.agent/project.json` → `project_type` + `attributes`
- `.agent/agents/registry.json` → base + modifiers
- `.agent/memory/constitution.md` → ràng buộc (Docker-First, Port 8900-8999, ENV)

## 🎛️ Resolved Agent Set (auto-generated)
- **Active agents**: {active_list}
- **Builder agents**: {builder_list}

## 📋 Protocol

### 1. Resolve Agent Set (Attribute-based)
```
active = core_agents
       + base_by_type[project_type]
       + modifiers.architecture[attributes.architecture]
       + modifiers.platforms[p] for p in attributes.platforms
       + modifiers.flags[f] for f in attributes.flags
active = unique(active)
```
Cùng `project_type` nhưng `attributes` khác → tập agent KHÁC nhau.

### 2. Routing theo Pipeline Phase
| Phase | Agent điều phối | Domain agents |
|---|---|---|
| Specify | speckit.specify | review scope |
| Plan | speckit.plan | speckit.devops + builders |
| Tasks | speckit.tasks | — |
| Implement | speckit.implement | builder theo task tag |
| Verify | speckit.tester / reviewer / validate | — |

### 3. Task Tagging
Mỗi task trong `tasks.md` PHẢI có tag `@agent:<name>` để route đúng.
Không có tag → suy luận từ keyword + project_type.

### 4. Conflict Resolution
- Constitution > Orchestrator > Domain Agent.
- 2 agent tranh chấp 1 file → owner theo Task Tag, agent còn lại review.

## 🚫 Guard Rails
- KHÔNG bỏ qua core agents trong pipeline.
- KHÔNG để 2 agent ghi cùng 1 file song song.
- KHÔNG vi phạm Constitution dù domain agent yêu cầu.
- Phản hồi bằng Tiếng Việt.
"""

    def _create_templates(self):
        for filename, template_fn in DOCUMENT_TEMPLATE_MAP.items():
            # Skip internal templates
            if filename in ("identity-template.md",):
                continue
            # Skip SEO template cho non-web projects
            type_info = PROJECT_TYPES.get(self.project_type, {})
            allowed_skills = type_info.get("includes_skills", [])
            if filename == "seo-standards-template.md" and "web" not in allowed_skills:
                continue
            if filename == "ui-ux-standards-template.md" and "web" not in allowed_skills:
                continue

            filepath = os.path.join(self.agent_dir, "templates", filename)
            self._write_file(filepath, template_fn())
            self.stats["templates"] += 1

    def _create_memory(self):
        filepath = os.path.join(self.agent_dir, "memory", "constitution.md")
        template_fn = DOCUMENT_TEMPLATE_MAP.get("constitution-template.md")
        self._write_file(filepath, template_fn(self.use_docker, self.is_soft_rules))

    def _create_scripts(self):
        for filename, script_fn in SCRIPT_TEMPLATE_MAP.items():
            filepath = os.path.join(self.agent_dir, "scripts", "bash", filename)
            self._write_file(filepath, script_fn())
            try:
                os.chmod(filepath, os.stat(filepath).st_mode | stat.S_IEXEC)
            except: pass
            self.stats["scripts"] += 1

    def _create_project_config(self):
        """Lưu thông tin project type vào .agent/project.json."""
        import json
        config = {
            "project_name": self.project_name,
            "project_type": self.project_type,
            "attributes": self.attributes,
            "asf_version": "3.3",
            "bro_skills_version": "1.2.0",
            "created_at": datetime.now().isoformat(),
            "skills_count": self.stats["skills"],
            "workflows_count": self.stats["workflows"],
            "multi_agent": True,
            "agent_registry": ".agent/agents/registry.json",
        }
        filepath = os.path.join(self.agent_dir, "project.json")
        self._write_file(filepath, json.dumps(config, indent=2, ensure_ascii=False))

    def _create_agent_readme(self):
        today = datetime.now().strftime("%Y-%m-%d")
        type_info = PROJECT_TYPES.get(self.project_type, {})
        type_label = type_info.get("label", self.project_type)

        seo_section = ""
        allowed_skills = type_info.get("includes_skills", [])
        if "web" in allowed_skills:
            seo_section = """
## 🔍 SEO & GEO
- `@speckit.seo`: Audit Technical SEO (Meta, Sitemap, Core Web Vitals)
- `@speckit.geo`: Tối ưu cho AI Search (llms.txt, E-E-A-T, Schema.org)
- `knowledge_base/seo_standards.md`: Checklist & JSON-LD templates
"""

        content = f"""# 🤖 bro-skills Configuration (ASF 3.3)

> **Project**: {self.project_name}
> **Type**: {type_label}
> **Generated**: {today}

## 🏗️ Architecture

- `.agent/identity/`: Định nghĩa Persona & Soul của AI.
- `.agent/knowledge_base/`: Kho tri thức về Business, Data, API, SEO.
- `.agent/skills/`: Các kỹ năng AI chuyên biệt (@mentions).
- `.agent/workflows/`: Các quy trình tự động hóa (/commands).
- `.agent/memory/`: Project Constitution (Luật dự án).
{seo_section}
## 🚀 Quick Start
1. Run `/01-speckit.constitution` để thiết lập luật dự án.
2. Run `@speckit.identity` để tinh chỉnh Persona của AI.
3. Run `/02-speckit.specify` để bắt đầu tính năng mới.
"""
        self._write_file(os.path.join(self.agent_dir, "README.md"), content)

    def _write_file(self, filepath, content):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    def _find_available_ports(self, start_port=8900, end_port=8999):
        """Tìm 3 port liên tiếp còn trống trong dải 8900-8999."""
        import socket

        def is_port_available(port):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                try:
                    sock.bind(("127.0.0.1", port))
                except OSError:
                    return False
                return True

        for p in range(start_port, end_port - 1):
            if all(is_port_available(port) for port in (p, p + 1, p + 2)):
                return (p, p + 1, p + 2)
        return None

    def _save_ports_to_env(self, ports):
        """Ghi cấu hình port vào file .env (ENV-first)."""
        env_path = os.path.join(self.target_dir, ".env")
        lines = []
        
        # Nếu đã có file .env, đọc nội dung cũ để tránh ghi đè dữ liệu quan trọng
        existing_content = ""
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                existing_content = f.read()

        # Chuẩn bị dữ liệu port
        port_vars = {
            f"NEXT_PUBLIC_PORT_FE": ports[0],
            f"ADMIN_PORT": ports[1],
            f"API_PORT": ports[2],
            f"NEXT_PUBLIC_API_URL": f"http://localhost:{ports[2]}"
        }

        # Tạo nội dung .env mới hoặc bổ sung
        new_lines = [f"{k}={v}" for k, v in port_vars.items() if k not in existing_content]
        
        if new_lines:
            with open(env_path, "a" if existing_content else "w", encoding="utf-8") as f:
                if existing_content and not existing_content.endswith("\n"):
                    f.write("\n")
                f.write("\n# bro-skills Port Configuration (Auto-generated)\n")
                f.write("\n".join(new_lines) + "\n")
            print("  🔐 Ports saved to .env")

    def _print_stats(self):
        type_info = PROJECT_TYPES.get(self.project_type, {})
        type_label = type_info.get("label", self.project_type)
        print(f"\n{'─' * 50}")
        print(f"📊 Thống kê khởi tạo (ASF 3.3 — {type_label}):")
        print(f"  🎭 Identity:  {self.stats['identity']}")
        print(f"  🧠 Knowledge: {self.stats['knowledge']}")
        print(f"  🛠️ Skills:    {self.stats['skills']}")
        print(f"  🔄 Workflows: {self.stats['workflows']}")
        print(f"  📄 Templates: {self.stats['templates']}")
        print(f"{'─' * 50}\n")
