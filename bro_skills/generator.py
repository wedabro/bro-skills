"""
Scaffolder Generator - Core logic for creating the .agent/ directory structure.
Supports filtering skills/workflows by Project Type.
Automatically populates content from Scanner when the project already exists.
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
    doc_roocode_rules_template,
    doc_trae_rules_template,
    doc_continue_config_template,
)
from .scanner import ProjectScanner


class ProjectGenerator:
    """Scaffold .agent/ structure for a project compliant with Spec-Kit & ASF 3.3."""

    def __init__(self, target_dir: str, project_name: str, project_type: str = "fullstack", scan_profile: dict = None, attributes: dict = None, lang: str = "dynamic", ai_agent: str = "all", selected_skills: list = None, vault_path: str = None):
        self.target_dir = target_dir
        self.project_name = project_name
        self.project_type = project_type
        self.scan_profile = scan_profile  # Result from ProjectScanner
        self.attributes = attributes or {}  # Multi-agent attributes (architecture/platforms/flags)
        self.agent_dir = os.path.join(target_dir, ".agent")
        self.lang = lang or "dynamic"
        self.ai_agent = ai_agent or "all"
        self.selected_skills = selected_skills
        self.vault_path = vault_path

        # Filter skills/workflows by project type + attributes (multi-agent v2)
        if selected_skills:
            normalized_selected = set()
            registry_names = {s["name"].lower() for s in SKILLS_REGISTRY}
            for s in selected_skills:
                s_clean = s.strip().lower()
                if not s_clean:
                    continue
                if s_clean in registry_names:
                    normalized_selected.add(s_clean)
                elif f"speckit.{s_clean}" in registry_names:
                    normalized_selected.add(f"speckit.{s_clean}")
                else:
                    normalized_selected.add(s_clean)
            
            # Select from ALL SKILLS in registry, not just project type defaults
            self.filtered_skills = [
                s for s in SKILLS_REGISTRY
                if s["name"] in normalized_selected or s.get("project_types") == "all"
            ]
            
            # Select from ALL WORKFLOWS in registry where all referenced skills are active
            active_skill_names = {s["name"] for s in self.filtered_skills}
            self.filtered_workflows = [
                w for w in WORKFLOWS_REGISTRY
                if all(s_name in active_skill_names for s_name in w.get("skills", []))
            ]
        else:
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
        """Execute the entire scaffolding process."""
        from .registry import get_project_type_info
        type_info = get_project_type_info(self.project_type)
        self.use_docker = type_info.get("use_docker", True)
        self.is_soft_rules = type_info.get("is_soft_rules", False)

        print(f"📁 Scaffolding directory structure (ASF 3.3 Standard — {self.project_type})...")
        self._create_directories()

        # ─── 0. Check Port (Only if project uses Docker and port config is missing in .env) ───
        env_path = os.path.join(self.target_dir, ".env")
        has_ports_in_env = False
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                env_content = f.read()
                port_keys = ["PORT_FE", "NEXT_PUBLIC_PORT_FE", "ADMIN_PORT", "API_PORT", "VITE_PORT_FE"]
                if any(k in env_content for k in port_keys):
                    has_ports_in_env = True

        if self.use_docker and not has_ports_in_env:
             ports = self._find_available_ports()
             if ports:
                 self.assigned_ports = ports
                 print(f"📡 Port assigned (8900-8999): Public:{ports[0]}, Admin:{ports[1]}, API:{ports[2]}")
                 self._save_ports_to_env(ports)
             else:
                 print("⚠️  No available ports found in 8900-8999 range. Please check your system.")
                 self.assigned_ports = (8900, 8901, 8902) # Safe fallback
        else:
             self.assigned_ports = None

        print("🎭 Setting up Identity & Soul...")
        self._create_identity()

        print("🧠 Initializing Knowledge Base...")
        self._create_knowledge_base()

        print("🛠️ Creating Skills (@mentions)...")
        self._create_skills()

        print("🔄 Creating Workflows (/commands)...")
        self._create_workflows()

        print("🧭 Creating Multi-Agent (registry + orchestrator)...")
        self._create_agents()

        print("📄 Creating Templates & Memory...")
        self._create_templates()
        self._create_memory()

        print("🔧 Creating Bash Scripts...")
        self._create_scripts()

        print("🖥️  Setting up Rules for 8 IDE/Agent...")
        self._create_ide_rules()

        self._create_project_config()
        self._create_agent_readme()
        self._print_stats()

    def _create_ide_rules(self):
        """Create rule files selectively for chosen IDE/Agent or all of them."""
        name = self.project_name
        agent = self.ai_agent.lower().strip()

        # ─── 1. Antigravity (Google) ────────────────────────
        if agent in ("antigravity", "all"):
            self._write_file(
                os.path.join(self.agent_dir, "rules", "bro-skills.md"),
                doc_antigravity_rules_template(name, self.use_docker, self.is_soft_rules, self.lang)
            )
            self._write_file(
                os.path.join(self.target_dir, "AGENTS.md"),
                doc_agents_md_template(name, self.use_docker, self.is_soft_rules, self.lang)
            )
            print("  ✅ Antigravity  → .agent/rules/bro-skills.md & AGENTS.md")

        # ─── 2. Cursor ──────────────────────────────────────
        if agent in ("cursor", "all"):
            cursor_dir = os.path.join(self.target_dir, ".cursor", "rules")
            os.makedirs(cursor_dir, exist_ok=True)
            self._write_file(
                os.path.join(cursor_dir, "bro-skills.mdc"),
                doc_cursor_rules_template(name, self.use_docker, self.is_soft_rules, self.lang)
            )
            print("  ✅ Cursor       → .cursor/rules/bro-skills.mdc")

        # ─── 3. Windsurf (Codeium) ──────────────────────────
        if agent in ("windsurf", "all"):
            windsurf_dir = os.path.join(self.target_dir, ".windsurf", "rules")
            os.makedirs(windsurf_dir, exist_ok=True)
            self._write_file(
                os.path.join(windsurf_dir, "bro-skills.md"),
                doc_windsurf_rules_template(name, self.use_docker, self.is_soft_rules, self.lang)
            )
            print("  ✅ Windsurf     → .windsurf/rules/bro-skills.md")

        # ─── 4. VS Code (GitHub Copilot) ────────────────────
        if agent in ("copilot", "all"):
            github_dir = os.path.join(self.target_dir, ".github")
            os.makedirs(github_dir, exist_ok=True)
            self._write_file(
                os.path.join(github_dir, "copilot-instructions.md"),
                doc_vscode_copilot_template(name, self.use_docker, self.is_soft_rules, self.lang)
            )
            print("  ✅ VS Code      → .github/copilot-instructions.md")

        # ─── 5. JetBrains (PhpStorm, WebStorm, PyCharm) ────
        if agent in ("jetbrains", "all"):
            jb_dir = os.path.join(self.target_dir, ".aiassistant", "rules")
            os.makedirs(jb_dir, exist_ok=True)
            self._write_file(
                os.path.join(jb_dir, "bro-skills.md"),
                doc_jetbrains_rules_template(name, self.use_docker, self.is_soft_rules, self.lang)
            )
            print("  ✅ JetBrains    → .aiassistant/rules/bro-skills.md")

        # ─── 6. Kiro (AWS) ──────────────────────────────────
        if agent in ("kiro", "all"):
            kiro_dir = os.path.join(self.target_dir, ".kiro", "steering")
            os.makedirs(kiro_dir, exist_ok=True)
            self._write_file(
                os.path.join(kiro_dir, "tech.md"),
                doc_kiro_steering_template(name, self.lang)
            )
            self._create_kiro_mcp()
            self._create_kiro_skills_bridge()
            print("  ✅ Kiro         → .kiro/steering/tech.md & MCP & Skills Bridge")

        # ─── 7. Claude Code ─────────────────────────────────
        if agent in ("claude", "all"):
            self._write_file(
                os.path.join(self.target_dir, "CLAUDE.md"),
                doc_claude_md_template(name, self.use_docker, self.is_soft_rules, self.lang)
            )
            print("  ✅ Claude Code  → CLAUDE.md")

        # ─── 8. Roo Code ────────────────────────────────────
        if agent in ("roocode", "all"):
            self._write_file(
                os.path.join(self.target_dir, ".clinerules"),
                doc_roocode_rules_template(name, self.use_docker, self.is_soft_rules, self.lang)
            )
            self._write_file(
                os.path.join(self.target_dir, ".roomember"),
                doc_roocode_rules_template(name, self.use_docker, self.is_soft_rules, self.lang)
            )
            print("  ✅ Roo Code     → .clinerules & .roomember")

        # ─── 9. Trae ────────────────────────────────────────
        if agent in ("trae", "all"):
            self._write_file(
                os.path.join(self.target_dir, ".traerules"),
                doc_trae_rules_template(name, self.use_docker, self.is_soft_rules, self.lang)
            )
            print("  ✅ Trae         → .traerules")

        # ─── 10. Qoder ──────────────────────────────────────
        if agent in ("qoder", "all"):
            qoder_dir = os.path.join(self.target_dir, ".qoder", "rules")
            os.makedirs(qoder_dir, exist_ok=True)
            self._write_file(
                os.path.join(qoder_dir, "bro-skills.md"),
                doc_windsurf_rules_template(name, self.use_docker, self.is_soft_rules, self.lang)
            )
            print("  ✅ Qoder        → .qoder/rules/bro-skills.md")

        # ─── 11. OpenCode ───────────────────────────────────
        if agent in ("opencode", "all"):
            opencode_dir = os.path.join(self.target_dir, ".opencode", "rules")
            os.makedirs(opencode_dir, exist_ok=True)
            self._write_file(
                os.path.join(opencode_dir, "bro-skills.md"),
                doc_windsurf_rules_template(name, self.use_docker, self.is_soft_rules, self.lang)
            )
            print("  ✅ OpenCode     → .opencode/rules/bro-skills.md")

        # ─── 12. Gemini CLI ─────────────────────────────────
        if agent in ("gemini", "all"):
            gemini_dir = os.path.join(self.target_dir, ".gemini", "rules")
            os.makedirs(gemini_dir, exist_ok=True)
            self._write_file(
                os.path.join(gemini_dir, "bro-skills.md"),
                doc_windsurf_rules_template(name, self.use_docker, self.is_soft_rules, self.lang)
            )
            print("  ✅ Gemini CLI   → .gemini/rules/bro-skills.md")

        # ─── 13. Continue ───────────────────────────────────
        if agent in ("continue", "all"):
            continue_dir = os.path.join(self.target_dir, ".continue")
            os.makedirs(continue_dir, exist_ok=True)
            self._write_file(
                os.path.join(continue_dir, "config.json"),
                doc_continue_config_template()
            )
            print("  ✅ Continue     → .continue/config.json")

        # ─── 14. Codex ──────────────────────────────────────
        if agent in ("codex", "all"):
            self._create_codex_skills_bridge()
            self._write_file(
                os.path.join(self.target_dir, ".agents", "AGENTS.md"),
                doc_agents_md_template(name, self.use_docker, self.is_soft_rules, self.lang)
            )
            print("  ✅ Codex        → .agents/AGENTS.md & Skills Bridge")

    def _create_codex_skills_bridge(self):
        """Bridge .agent/skills -> .agents/skills for Codex customizations root."""
        import shutil

        src = os.path.join(self.agent_dir, "skills")
        dst = os.path.join(self.target_dir, ".agents", "skills")
        os.makedirs(os.path.dirname(dst), exist_ok=True)

        # Clean old links/dirs
        if os.path.islink(dst) or os.path.isfile(dst):
            os.unlink(dst)
        elif os.path.isdir(dst):
            if os.name == "nt":
                try:
                    os.rmdir(dst)
                except OSError:
                    shutil.rmtree(dst, ignore_errors=True)
            else:
                shutil.rmtree(dst, ignore_errors=True)

        rel_src = os.path.relpath(src, os.path.dirname(dst))

        # 1) POSIX: relative symlink
        if os.name != "nt":
            try:
                os.symlink(rel_src, dst, target_is_directory=True)
                print("  🔗 Codex Skills → .agents/skills (symlink → .agent/skills)")
                return
            except (OSError, NotImplementedError):
                pass
        else:
            # 2) Windows: junction
            try:
                import subprocess
                subprocess.run(
                    ["cmd", "/c", "mklink", "/J", dst, src],
                    check=True, capture_output=True, text=True,
                )
                print("  🔗 Codex Skills → .agents/skills (junction → .agent/skills)")
                return
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass

        # 3) Fallback: copy
        shutil.copytree(src, dst)
        print("  📄 Codex Skills → .agents/skills (copy — symlink/junction unavailable)")

    def _create_kiro_mcp(self):
        """Create/merge .kiro/settings/mcp.json (merge-safe).

        - File does not exist -> create new with default scaffold.
        - File exists -> ONLY add missing servers, DO NOT overwrite existing servers/configs.
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
            print("  ✅ Kiro MCP     → .kiro/settings/mcp.json (keeping existing servers)")

    def _create_kiro_skills_bridge(self):
        """Bridge .agent/skills -> .kiro/skills for Kiro (AWS) to auto-load skills.

        The SKILL.md format of bro-skills (frontmatter name + description) matches
        the Kiro skill standard so it can be used directly. Prefer symlink/junction
        (2-way sync, no duplication); fallback to copy on failure.
        """
        import shutil

        src = os.path.join(self.agent_dir, "skills")
        dst = os.path.join(self.target_dir, ".kiro", "skills")
        os.makedirs(os.path.dirname(dst), exist_ok=True)

        # Clean old links/dirs
        if os.path.islink(dst) or os.path.isfile(dst):
            os.unlink(dst)
        elif os.path.isdir(dst):
            if os.name == "nt":
                # Junction is recognized as dir; delete safely
                try:
                    os.rmdir(dst)
                except OSError:
                    shutil.rmtree(dst, ignore_errors=True)
            else:
                shutil.rmtree(dst, ignore_errors=True)

        rel_src = os.path.relpath(src, os.path.dirname(dst))

        # 1) POSIX: relative symlink
        if os.name != "nt":
            try:
                os.symlink(rel_src, dst, target_is_directory=True)
                print("  🔗 Kiro Skills  → .kiro/skills (symlink → .agent/skills)")
                return
            except (OSError, NotImplementedError):
                pass
        else:
            # 2) Windows: junction (does not need admin rights)
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

        # 3) Fallback: copy (loses 2-way sync)
        shutil.copytree(src, dst)
        print("  📄 Kiro Skills  → .kiro/skills (copy — symlink/junction unavailable)")

    def _create_directories(self):
        """Scaffold .agent/ directory structure compliant with ASF 3.3."""
        dirs = [
            ".agent/identity",       # Identity layer
            ".agent/knowledge_base", # Project knowledge base layer
            ".agent/skills",         # Skills layer (@skill)
            ".agent/workflows",      # Workflows layer (/command)
            ".agent/scripts/bash",   # Infrastructure scripts layer
            ".agent/templates",      # Scaffolding templates layer
            ".agent/memory",         # Constitution storage layer
            ".agent/rules",          # Antigravity rules layer
            ".agent/codebase",       # Structure map layer (speckit.map)
            ".agent/specs",          # Specification & Planning layer
            ".agent/agents",         # Multi-Agent layer (registry + orchestrator)
        ]

        for d in dirs:
            full_path = os.path.join(self.target_dir, d)
            os.makedirs(full_path, exist_ok=True)
            self.stats["directories"] += 1

    def _create_identity(self):
        """Create Master Identity - aware of Project Type + scan information."""
        filepath = os.path.join(self.agent_dir, "identity", "master-identity.md")
        content = doc_identity_template(self.project_name, self.project_type, self.use_docker, self.lang)

        # Append context from scanner
        if self.scan_profile and self.scan_profile.get("has_existing_code"):
            scanner = ProjectScanner(self.target_dir)
            scanner.profile = self.scan_profile
            context = scanner.generate_identity_context()
            if context:
                content += f"\n## 🔬 Project Context (Auto-detected)\n{context}\n"

        self._write_file(filepath, content)
        self.stats["identity"] += 1

    def _create_knowledge_base(self):
        """Create baseline knowledge base files - use scan data if available."""
        base_path = os.path.join(self.agent_dir, "knowledge_base")

        if self.scan_profile and self.scan_profile.get("has_existing_code"):
            # READ REAL DATA FROM SCANNER
            scanner = ProjectScanner(self.target_dir)
            scanner.profile = self.scan_profile

            print("  📖 Populating content from real codebase...")

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
            # New project - use template placeholder
            infra_path = os.path.join(base_path, "infrastructure.md")
            infra_template = DOCUMENT_TEMPLATE_MAP.get("infrastructure-template.md")
            self._write_file(infra_path, infra_template())

            files = {
                "business_logic.md": "# Business Logic\n\nDefine core business logic here.",
                "data_schema.md": "# Data Schema\n\nDefine database structure and entity relationships here.",
                "api_standards.md": "# API Standards\n\nAPI design guidelines, error codes, and auth headers.",
            }
            for name, content in files.items():
                self._write_file(os.path.join(base_path, name), content)
                self.stats["knowledge"] += 1

        # SEO & UI/UX Standards — ONLY create for Web projects
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
        """Create SKILL.md for each skill - ONLY create skills matching project type."""
        import shutil
        for skill in self.filtered_skills:
            skill_name = skill["name"]
            skill_dir = os.path.join(self.agent_dir, "skills", skill_name)

            copied_from_vault = False
            if self.vault_path:
                vault_skill_dir = os.path.join(self.vault_path, "skills", skill_name)
                if os.path.isdir(vault_skill_dir):
                    if os.path.exists(skill_dir):
                        try:
                            shutil.rmtree(skill_dir)
                        except Exception as e:
                            print(f"⚠️  Could not remove existing skill dir {skill_dir}: {e}")
                    try:
                        shutil.copytree(vault_skill_dir, skill_dir)
                        copied_from_vault = True
                        print(f"  ✅ Copied skill '{skill_name}' from vault.")
                    except Exception as e:
                        print(f"⚠️  Failed to copy skill '{skill_name}' from vault: {e}")

            if not copied_from_vault:
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
You are **{skill['role']}**.

## Task
{skill['description']}

## Execution Outline
1. Load context from `.agent/identity/master-identity.md`.
2. Check `.agent/memory/constitution.md` for rules.
3. Perform the primary task.
4. Report results.
"""

    def _create_workflows(self):
        """Create workflow .md files - ONLY create workflows matching project type."""
        for wf in self.filtered_workflows:
            cmd = wf["command"]
            filepath = os.path.join(self.agent_dir, "workflows", f"{cmd}.md")

            # Prioritize detailed templates from WORKFLOW_TEMPLATE_MAP
            template_fn = WORKFLOW_TEMPLATE_MAP.get(cmd)
            if template_fn:
                content = template_fn()
            else:
                # Fallback for workflows without templates
                content = f"---\ndescription: {wf['description']}\n---\n\n# Workflow: {cmd}\n\n1. Run @{wf['skills'][0] if wf['skills'] else 'speckit.tasks'}"

            self._write_file(filepath, content)
            self.stats["workflows"] += 1

    def _create_agents(self):
        """Scaffold .agent/agents/: registry.json + orchestrator.md (Multi-Agent v2)."""
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
description: Multi-Agent Orchestrator - Coordinate agents by project_type + attributes and pipeline Specify->Plan->Tasks->Implement.
role: Lead Orchestrator
trigger: always_on
---

# 🧭 Multi-Agent Orchestrator

## 🎯 Mission
Coordinate specialized agents in the project **{self.project_name}** (`{self.project_type}`).
Decide which agent handles which task based on `project_type` + `attributes` and pipeline phases.

## 📥 Input
- `.agent/project.json` → `project_type` + `attributes`
- `.agent/agents/registry.json` → base + modifiers
- `.agent/memory/constitution.md` → constraints (Docker-First, Port 8900-8999, ENV)

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
Same `project_type` but different `attributes` -> different agent set.

### 2. Routing by Pipeline Phase
| Phase | Coordinating Agent | Domain Agents |
|---|---|---|
| Specify | speckit.specify | review scope |
| Plan | speckit.plan | speckit.devops + builders |
| Tasks | speckit.tasks | — |
| Implement | speckit.implement | builder based on task tag |
| Verify | speckit.tester / reviewer / validate | — |

### 3. Task Tagging
Each task in `tasks.md` MUST have the tag `@agent:<name>` to route correctly.
No tag -> inferred from keyword + project_type.

### 4. Conflict Resolution
- Constitution > Orchestrator > Domain Agent.
- 2 agents conflicting over 1 file -> owner based on Task Tag, the other agent reviews.

## 🚫 Guard Rails
- DO NOT bypass core agents in pipeline.
- DO NOT allow 2 agents to write to the same file in parallel.
- DO NOT violate the Constitution even if requested by a domain agent.
- Respond in the language used by the user (supports Vietnamese and English).
"""

    def _create_templates(self):
        for filename, template_fn in DOCUMENT_TEMPLATE_MAP.items():
            # Skip internal templates
            if filename in ("identity-template.md",):
                continue
            # Skip SEO template for non-web projects
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
        self._write_file(filepath, template_fn(self.use_docker, self.is_soft_rules, self.lang))

    def _create_scripts(self):
        for filename, script_fn in SCRIPT_TEMPLATE_MAP.items():
            filepath = os.path.join(self.agent_dir, "scripts", "bash", filename)
            self._write_file(filepath, script_fn())
            try:
                os.chmod(filepath, os.stat(filepath).st_mode | stat.S_IEXEC)
            except: pass
            self.stats["scripts"] += 1

    def _create_project_config(self):
        """Save project type info to .agent/project.json."""
        import json
        config = {
            "project_name": self.project_name,
            "project_type": self.project_type,
            "attributes": self.attributes,
            "agent_language": self.lang,
            "asf_version": "3.3",
            "bro_skills_version": "1.5.3",
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
- `@speckit.seo`: Technical SEO Audit (Meta, Sitemap, Core Web Vitals)
- `@speckit.geo`: Optimized for AI Search (llms.txt, E-E-A-T, Schema.org)
- `knowledge_base/seo_standards.md`: Checklist & JSON-LD templates
"""

        content = f"""# 🤖 bro-skills Configuration (ASF 3.3)

> **Project**: {self.project_name}
> **Type**: {type_label}
> **Generated**: {today}

## 🏗️ Architecture

- `.agent/identity/`: Persona & Soul definition of the AI.
- `.agent/knowledge_base/`: Project knowledge base (Business, Data, API, SEO).
- `.agent/skills/`: Specialized AI skills (@mentions).
- `.agent/workflows/`: Automation workflows (/commands).
- `.agent/memory/`: Project Constitution (Rules of the project).
{seo_section}
## 🚀 Quick Start
1. Run `/01-speckit.constitution` to establish the project constitution.
2. Run `@speckit.identity` to refine the AI Persona.
3. Run `/02-speckit.specify` to start a new feature.
"""
        self._write_file(os.path.join(self.agent_dir, "README.md"), content)

    def _write_file(self, filepath, content):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    def _find_available_ports(self, start_port=8900, end_port=8999):
        """Find 3 consecutive available ports in the range 8900-8999."""
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
        """Write port configuration to .env file (ENV-first)."""
        env_path = os.path.join(self.target_dir, ".env")
        existing_content = ""
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                existing_content = f.read()

        # Prepare port variables (including generic & Vite variables for non-NextJS projects)
        port_vars = {
            # Next.js
            "NEXT_PUBLIC_PORT_FE": ports[0],
            "ADMIN_PORT": ports[1],
            "API_PORT": ports[2],
            "NEXT_PUBLIC_API_URL": f"http://localhost:{ports[2]}",
            # Generic / Other frameworks (Vite, Nuxt, etc.)
            "PORT_FE": ports[0],
            "VITE_PORT_FE": ports[0],
            "VITE_API_URL": f"http://localhost:{ports[2]}",
            "API_URL": f"http://localhost:{ports[2]}"
        }

        # Create or append new .env content
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
        print(f"Scaffolding stats (ASF 3.3 — {type_label}):")
        print(f"  🎭 Identity:  {self.stats['identity']}")
        print(f"  🧠 Knowledge: {self.stats['knowledge']}")
        print(f"  🛠️ Skills:    {self.stats['skills']}")
        print(f"  🔄 Workflows: {self.stats['workflows']}")
        print(f"  📄 Templates: {self.stats['templates']}")
        print(f"{'─' * 50}\n")

    def install_skills(self):
        """Install only the selected skills, workflows, and update agent registries."""
        print(f"🛠️  Installing selected skills into {self.agent_dir}...")
        
        # 1. Create skills
        self._create_skills()
        
        # 2. Create workflows
        self._create_workflows()
        
        # 3. Update agents/orchestration
        self._create_agents()
        
        # 4. Bridge if needed
        agent = self.ai_agent.lower().strip()
        if agent in ("codex", "all"):
            self._create_codex_skills_bridge()
        if agent in ("kiro", "all"):
            self._create_kiro_skills_bridge()
            
        print(f"✅ Installed {self.stats['skills']} skills and {self.stats['workflows']} workflows successfully.")

