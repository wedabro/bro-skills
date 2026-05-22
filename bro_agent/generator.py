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
    doc_claude_md_template,
    doc_agents_md_template,
)
from .scanner import ProjectScanner


class ProjectGenerator:
    """Sinh cấu trúc .agent/ cho project theo chuẩn Spec-Kit & ASF 3.3."""

    def __init__(self, target_dir: str, project_name: str, project_type: str = "fullstack", scan_profile: dict = None):
        self.target_dir = target_dir
        self.project_name = project_name
        self.project_type = project_type
        self.scan_profile = scan_profile  # Kết quả từ ProjectScanner
        self.agent_dir = os.path.join(target_dir, ".agent")

        # Lọc skills/workflows theo project type
        self.filtered_skills = get_skills_for_project_type(project_type)
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
                 print(f"📡 Port assigned (9XXX): Public:{ports[0]}, Admin:{ports[1]}, API:{ports[2]}")
                 self._save_ports_to_env(ports)
             else:
                 print("⚠️  Không tìm thấy dải port 9xxx trống. Vui lòng kiểm tra lại hệ thống.")
                 self.assigned_ports = (9000, 9001, 9002) # Fallback an toàn
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
        # Path: .agent/rules/bro-agent.md
        self._write_file(
            os.path.join(self.agent_dir, "rules", "bro-agent.md"),
            doc_antigravity_rules_template(name, self.use_docker, self.is_soft_rules)
        )
        print("  ✅ Antigravity  → .agent/rules/bro-agent.md")

        # ─── 2. Cursor ──────────────────────────────────────
        # Path: .cursor/rules/bro-agent.mdc (YAML frontmatter, .mdc extension)
        cursor_dir = os.path.join(self.target_dir, ".cursor", "rules")
        os.makedirs(cursor_dir, exist_ok=True)
        self._write_file(
            os.path.join(cursor_dir, "bro-agent.mdc"),
            doc_cursor_rules_template(name, self.use_docker, self.is_soft_rules)
        )
        print("  ✅ Cursor       → .cursor/rules/bro-agent.mdc")

        # ─── 3. Windsurf (Codeium) ──────────────────────────
        # Path: .windsurf/rules/bro-agent.md
        windsurf_dir = os.path.join(self.target_dir, ".windsurf", "rules")
        os.makedirs(windsurf_dir, exist_ok=True)
        self._write_file(
            os.path.join(windsurf_dir, "bro-agent.md"),
            doc_windsurf_rules_template(name, self.use_docker, self.is_soft_rules)
        )
        print("  ✅ Windsurf     → .windsurf/rules/bro-agent.md")

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
        # Path: .aiassistant/rules/bro-agent.md
        jb_dir = os.path.join(self.target_dir, ".aiassistant", "rules")
        os.makedirs(jb_dir, exist_ok=True)
        self._write_file(
            os.path.join(jb_dir, "bro-agent.md"),
            doc_jetbrains_rules_template(name, self.use_docker, self.is_soft_rules)
        )
        print("  ✅ JetBrains    → .aiassistant/rules/bro-agent.md")

        # ─── 6. Kiro (AWS) ──────────────────────────────────
        # Path: .kiro/steering/tech.md
        kiro_dir = os.path.join(self.target_dir, ".kiro", "steering")
        os.makedirs(kiro_dir, exist_ok=True)
        self._write_file(
            os.path.join(kiro_dir, "tech.md"),
            doc_kiro_steering_template(name) # Kiro keeps original for now
        )
        print("  ✅ Kiro         → .kiro/steering/tech.md")

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
            "asf_version": "3.3",
            "bro_agent_version": "1.2.0",
            "created_at": datetime.now().isoformat(),
            "skills_count": self.stats["skills"],
            "workflows_count": self.stats["workflows"],
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

        content = f"""# 🤖 bro-agent Configuration (ASF 3.3)

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

    def _find_available_ports(self, start_port=9000, end_port=9999):
        """Tìm 3 port liên tiếp còn trống trong dải 9000-9999 (Windows)."""
        import subprocess
        try:
            # Chạy lệnh netstat để tìm các port đang bận (quét dải :9)
            output = subprocess.check_output("netstat -ano | findstr :9", shell=True).decode()
            used_ports = set()
            for line in output.splitlines():
                parts = line.split()
                if len(parts) > 1:
                    port_part = parts[1].split(':')[-1]
                    try:
                        p_val = int(port_part)
                        if start_port <= p_val <= end_port:
                            used_ports.add(p_val)
                    except: continue
            
            # Tìm 3 port liên tiếp (từ thấp đến cao)
            for p in range(start_port, end_port - 1):
                if p not in used_ports and (p+1) not in used_ports and (p+2) not in used_ports:
                    return (p, p+1, p+2)
        except Exception:
            pass
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
                f.write("\n# bro-agent Port Configuration (Auto-generated)\n")
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
