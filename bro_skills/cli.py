#!/usr/bin/env python3
"""⚡ bro-skills - Spec-Driven Development CLI
Entry point for console script `bro-skills`.

Global settings:
    pip install bro-skills
    bro-skills init --name "My Project"

Or run directly:
    python -m bro_skills init --name "My Project"
"""

import argparse
import sys
import os

from bro_skills import __version__
from bro_skills.generator import ProjectGenerator
from bro_skills.scanner import ProjectScanner
from bro_skills.validators import validate_agent_structure
from bro_skills.registry import (
    SKILLS_REGISTRY, WORKFLOWS_REGISTRY, PROJECT_TYPES,
    get_skills_for_project_type, get_workflows_for_project_type,
)


def select_menu(options, title="", lang="en"):
    """
    options: list of tuples (value, label_en, label_vi)
    title: Title of the menu
    """
    import sys
    import shutil
    
    selected_idx = 0
    is_windows = sys.platform.startswith('win')
    
    # Track the last printed visual lines count to move cursor back down
    last_total_lines = [0]
    
    def print_menu():
        cols = shutil.get_terminal_size().columns
        
        # Calculate visual lines with wrapping
        visual_lines = 0
        for i, opt in enumerate(options):
            label = opt[2] if lang == "vi" else opt[1]
            text_len = len(label) + 4
            visual_lines += max(1, (text_len + cols - 1) // cols)
            
        title_lines = max(1, (len(title) + cols - 1) // cols)
        total_lines = visual_lines + title_lines
        last_total_lines[0] = total_lines
        
        # Clear lines as we print
        sys.stdout.write(f"\r\033[K{title}\n")
        for i, opt in enumerate(options):
            label = opt[2] if lang == "vi" else opt[1]
            if i == selected_idx:
                sys.stdout.write(f"\033[K\033[96m  ➔ {label}\033[0m\n")
            else:
                sys.stdout.write(f"\033[K    {label}\n")
        sys.stdout.write(f"\033[{total_lines}A")
        sys.stdout.flush()

    if not sys.stdout.isatty():
        return options[0][0]

    cols = shutil.get_terminal_size().columns
    initial_visual_lines = 0
    for opt in options:
        label = opt[2] if lang == "vi" else opt[1]
        text_len = len(label) + 4
        initial_visual_lines += max(1, (text_len + cols - 1) // cols)
    initial_title_lines = max(1, (len(title) + cols - 1) // cols)
    initial_total_lines = initial_visual_lines + initial_title_lines

    sys.stdout.write("\033[?25l") # hide cursor
    sys.stdout.write("\n" * initial_total_lines)
    sys.stdout.write(f"\033[{initial_total_lines}A")
    sys.stdout.flush()

    try:
        if is_windows:
            import msvcrt
            while True:
                print_menu()
                ch = msvcrt.getch()
                if ch == b'\r':
                    break
                elif ch == b'\x1b' or ch in (b'q', b'Q'):
                    return "cancel"
                elif ch in (b'\xe0', b'\x00'):
                    ch2 = msvcrt.getch()
                    if ch2 == b'H':
                        selected_idx = (selected_idx - 1) % len(options)
                    elif ch2 == b'P':
                        selected_idx = (selected_idx + 1) % len(options)
        else:
            import tty
            import termios
            import select
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                while True:
                    print_menu()
                    char1 = sys.stdin.read(1)
                    if char1 == '\r' or char1 == '\n':
                        break
                    elif char1 in ('q', 'Q'):
                        return "cancel"
                    elif char1 == '\x1b':
                        rlist, _, _ = select.select([sys.stdin], [], [], 0.05)
                        if rlist:
                            char2 = sys.stdin.read(1)
                            if char2 == '[':
                                char3 = sys.stdin.read(1)
                                if char3 == 'A':
                                    selected_idx = (selected_idx - 1) % len(options)
                                elif char3 == 'B':
                                    selected_idx = (selected_idx + 1) % len(options)
                        else:
                            return "cancel"
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    finally:
        # Move cursor down by the last printed total lines so we don't overwrite the final output
        sys.stdout.write(f"\033[{last_total_lines[0]}B\033[?25h\n")
        sys.stdout.flush()
        
    return options[selected_idx][0]


def _ask_project_type(lang="en"):
    """Ask the user to select a project type using arrow keys."""
    options = []
    vi_translations = {
        "web_public": ("Web Công cộng / B2C (Web Public)", "Trang đích (Landing Page), Blog, Thương mại điện tử, Tin tức — Cần tối ưu SEO + GEO"),
        "web_saas": ("Web SaaS / B2B (Web SaaS)", "Dashboard, Trang quản trị, Hệ thống nội bộ, Dịch vụ API — Ít cần SEO"),
        "mobile_app": ("Ứng dụng Di động (Mobile App)", "iOS/Android (React Native, Flutter, Swift, Kotlin) — Cần ASO, không cần SEO"),
        "desktop_cli": ("Desktop / Công cụ CLI", "Electron, WPF, công cụ dòng lệnh CLI — Không cần SEO"),
        "fullstack": ("Full-stack Web & API (Fullstack)", "Cả Frontend (Web) & Backend (API) — Nền tảng cho dự án có cả Web & Mobile App (Cần SEO + GEO + DevOps)"),
        "game": ("Phát triển Game (Game Dev)", "Game (Unity, Unreal, Godot, Phaser) — Game loop, ECS, netcode"),
        "simple_script": ("Script đơn giản / Tự động hóa", "Script Python/Bash/JS nhỏ — Không Docker, không Next.js"),
        "custom_infra": ("Hạ tầng tùy chỉnh (Custom)", "Dự án có hạ tầng riêng — Không bắt buộc chuẩn Docker 89XX"),
    }
    
    for key, info in PROJECT_TYPES.items():
        vi_label, vi_desc = vi_translations.get(key, (info["label"], info["description"]))
        options.append((
            key, 
            f"{info['label']} — {info['description']}", 
            f"{vi_label} — {vi_desc}"
        ))
    options.append(("back", "⬅️ Back to Agent Selection", "⬅️ Quay lại chọn AI Agent"))
    options.append(("cancel", "❌ Cancel & Exit", "❌ Hủy & Thoát"))
        
    title = "🏗️ Chọn loại dự án (Project type):" if lang == "vi" else "🏗️ Select project type:"
    selected_key = select_menu(options, title, lang)
    if selected_key in ("back", "cancel"):
        return selected_key, None
    return selected_key, PROJECT_TYPES[selected_key]


def _ask_agent_language():
    """Ask the user to select the agent response language using arrow keys."""
    options = [
        ("en", "English (en)", "Tiếng Anh (en)"),
        ("vi", "Vietnamese (vi)", "Tiếng Việt (vi)"),
        ("dynamic", "Dynamic (Detect dynamically)", "Tự động nhận diện (Dynamic)"),
        ("cancel", "❌ Cancel & Exit", "❌ Hủy & Thoát"),
    ]
    title = "🌐 Select Agent Response Language / Chọn ngôn ngữ của Agent:"
    return select_menu(options, title, lang="en")


def _ask_agent_selection(lang="en"):
    """Ask the user to select a target AI agent using arrow keys."""
    agents = [
        ("claude", "Claude Code (CLAUDE.md)", "Claude Code (CLAUDE.md)"),
        ("cursor", "Cursor (.cursor/rules/bro-skills.mdc)", "Cursor (.cursor/rules/bro-skills.mdc)"),
        ("windsurf", "Windsurf (.windsurf/rules/bro-skills.md)", "Windsurf (.windsurf/rules/bro-skills.md)"),
        ("antigravity", "Antigravity (.agent/rules/bro-skills.md + AGENTS.md)", "Antigravity (.agent/rules/bro-skills.md + AGENTS.md)"),
        ("copilot", "GitHub Copilot (.github/copilot-instructions.md)", "GitHub Copilot (.github/copilot-instructions.md)"),
        ("kiro", "Kiro (.kiro/steering/tech.md + MCP)", "Kiro (.kiro/steering/tech.md + MCP)"),
        ("codex", "Codex (skills.json in customizations root)", "Codex (skills.json trong customizations root)"),
        ("roocode", "Roo Code (.clinerules + .roomember)", "Roo Code (.clinerules + .roomember)"),
        ("qoder", "Qoder (.qoder/rules/bro-skills.md)", "Qoder (.qoder/rules/bro-skills.md)"),
        ("gemini", "Gemini CLI (.gemini/rules/bro-skills.md)", "Gemini CLI (.gemini/rules/bro-skills.md)"),
        ("trae", "Trae (.traerules)", "Trae (.traerules)"),
        ("opencode", "OpenCode (.opencode/rules/bro-skills.md)", "OpenCode (.opencode/rules/bro-skills.md)"),
        ("continue", "Continue (.continue/config.json)", "Continue (.continue/config.json)"),
        ("all", "All Assistants", "Tất cả trợ lý (All Assistants)"),
        ("back", "⬅️ Back to Language Selection", "⬅️ Quay lại chọn Ngôn ngữ"),
        ("cancel", "❌ Cancel & Exit", "❌ Hủy & Thoát"),
    ]
    title = "🤖 Chọn cấu hình trợ lý AI (Target AI Agent):" if lang == "vi" else "🤖 Select target AI agent configuration:"
    return select_menu(agents, title, lang)


def cmd_init(args):
    """Initialize the .agent/ structure for the project."""
    target = os.path.abspath(args.target or os.getcwd())
    name = args.name or os.path.basename(target)
    force = getattr(args, 'force', False)
    project_type = getattr(args, 'type', None)
    agent_dir = os.path.join(target, ".agent")

    print(f"\n⚡ bro-skills v{__version__} - Spec-Driven Development")
    print(f"{'─' * 50}")
    print(f"  📁 Target:  {target}")
    print(f"  📛 Project: {name}")
    print(f"{'─' * 50}\n")

    # MIGRATION AUDIT LOGIC
    existing_config = {}
    if os.path.exists(agent_dir) and not force:
        project_config_path = os.path.join(agent_dir, "project.json")
        if os.path.exists(project_config_path):
            try:
                import json
                with open(project_config_path, "r", encoding="utf-8") as f:
                    existing_config = json.load(f)
            except Exception:
                pass

    if os.path.exists(agent_dir) and not force:
        print("🔍 Scanning existing .agent/ structure...")
        audit_report = _audit_existing_agent(agent_dir)

        if audit_report["is_legacy"]:
            print("\n⚠️ DETECTED OLD STRUCTURE (LEGACY AGENT)\n")
            print(f"  {'File/Folder':<25} {'Status':<15} {'Action'}")
            print(f"  {'─' * 23}   {'─' * 13}   {'─' * 18}")

            for item in audit_report["items"]:
                print(f"  {item['name']:<25} {item['status']:<15} {item['action']}")

            print("\n💡 Optimal recommendation:")
            print(f" - Upgrade core skills & workflows to version {__version__} (ASF 3.3 standard)")
            print(" - Set up Identity & Knowledge Base layer to orient AI")
            print(" - Move old constitution to memory/constitution.md")

            response = input("\n🚀 Upgrade & Optimize to ASF 3.3 now? (y/N): ").strip().lower()
            if response != 'y':
                print("❌ Canceled.")
                return
        else:
            print("✅ The current structure meets ASF 3.3 standards.")
            response = input("♻️ Do you still want to reinstall (Re-init)? (y/N): ").strip().lower()
            if response != 'y':
                print("❌ Canceled.")
                return

    # LANGUAGE, AGENT, AND PROJECT TYPE SELECTION FLOW
    lang = getattr(args, 'lang', None) or existing_config.get("agent_language") or existing_config.get("language")
    ai_agent = getattr(args, 'ai', None) or existing_config.get("ai_agent") or existing_config.get("ai") or "all"
    project_type = getattr(args, 'type', None) or existing_config.get("project_type")
    type_info = None

    # Check if we can auto-apply existing configurations without interactive prompt
    is_upgrade = os.path.exists(agent_dir) and not force
    if is_upgrade and lang and ai_agent and project_type:
        type_info = PROJECT_TYPES.get(project_type, PROJECT_TYPES["fullstack"])
        print(f"ℹ️  Reusing existing configurations:")
        print(f"   - Language:  {lang}")
        print(f"   - AI Agent:  {ai_agent}")
        print(f"   - Type:      {type_info['label']}\n")
    else:
        # Fallback to interactive prompts if not fully specified in existing config or arguments
        step = 1
        lang = getattr(args, 'lang', None)
        ai_agent = getattr(args, 'ai', None)
        project_type = getattr(args, 'type', None)
        type_info = None

        while True:
            if step == 1:
                if getattr(args, 'lang', None):
                    lang = args.lang
                    step = 2
                else:
                    lang = _ask_agent_language()
                    if lang == "cancel" or lang == "back":
                        print("❌ Canceled / Đã hủy.")
                        return
                    if lang == "vi":
                        print(f"\n✅ Ngôn ngữ đã chọn: Tiếng Việt (vi)")
                    else:
                        print(f"\n✅ Selected language: {lang}")
                    step = 2
                    
            elif step == 2:
                if getattr(args, 'ai', None):
                    ai_agent = args.ai
                    step = 3
                else:
                    ai_agent = _ask_agent_selection(lang)
                    if ai_agent == "cancel":
                        print("❌ Canceled / Đã hủy.")
                        return
                    elif ai_agent == "back":
                        if getattr(args, 'lang', None):
                            print("❌ Canceled / Đã hủy.")
                            return
                        print("\n⬅️ Going back to Language Selection...")
                        step = 1
                    else:
                        if lang == "vi":
                            print(f"\n✅ Cấu hình Agent đã chọn: {ai_agent}")
                        else:
                            print(f"\n✅ Selected AI Agent: {ai_agent}")
                        step = 3
                        
            elif step == 3:
                if getattr(args, 'type', None):
                    project_type = args.type
                    type_info = PROJECT_TYPES.get(project_type, PROJECT_TYPES["fullstack"])
                    if lang == "vi":
                        vi_labels = {
                            "web_public": "Web Public (B2C)",
                            "web_saas": "Web SaaS (B2B)",
                            "mobile_app": "Mobile App",
                            "desktop_cli": "Desktop / CLI Tool",
                            "fullstack": "Full-stack (Web + API)",
                            "game": "Phát triển Game",
                            "simple_script": "Kịch bản đơn giản / Tự động hóa",
                            "custom_infra": "Hạ tầng tùy chỉnh"
                        }
                        lbl = vi_labels.get(project_type, type_info['label'])
                        print(f"  🏗️ Loại dự án: {lbl}")
                    else:
                        print(f"  🏗️ Project Type: {type_info['label']}")
                    step = 4
                    break
                else:
                    project_type, type_info = _ask_project_type(lang)
                    if project_type == "cancel":
                        print("❌ Canceled / Đã hủy.")
                        return
                    elif project_type == "back":
                        if getattr(args, 'ai', None):
                            if getattr(args, 'lang', None):
                                print("❌ Canceled / Đã hủy.")
                                return
                            print("\n⬅️ Going back to Language Selection...")
                            step = 1
                        else:
                            print("\n⬅️ Going back to Agent Selection...")
                            step = 2
                    else:
                        if lang == "vi":
                            vi_labels = {
                                "web_public": "Web Public (B2C)",
                                "web_saas": "Web SaaS (B2B)",
                                "mobile_app": "Mobile App",
                                "desktop_cli": "Desktop / CLI Tool",
                                "fullstack": "Full-stack (Web + API)",
                                "game": "Phát triển Game",
                                "simple_script": "Kịch bản đơn giản / Tự động hóa",
                                "custom_infra": "Hạ tầng tùy chỉnh"
                            }
                            lbl = vi_labels.get(project_type, type_info['label'])
                            print(f"\n✅ Đã chọn loại dự án: {lbl}")
                        else:
                            print(f"\n✅ Selected: {type_info['label']}")
                        step = 4
                        break

    # Parse selected skills if provided
    selected_skills = None
    if getattr(args, "skills", None):
        selected_skills = [s.strip() for s in args.skills.split(",") if s.strip()]

    # Filter skills by project type and selected_skills
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
        
        filtered_skills = [
            s for s in SKILLS_REGISTRY
            if s["name"] in normalized_selected or s.get("project_types") == "all"
        ]
        
        active_skill_names = {s["name"] for s in filtered_skills}
        filtered_workflows = [
            w for w in WORKFLOWS_REGISTRY
            if all(s_name in active_skill_names for s_name in w.get("skills", []))
        ]
    else:
        filtered_skills = get_skills_for_project_type(project_type)
        filtered_workflows = get_workflows_for_project_type(project_type)

    # Show skills enabled/disabled
    all_skill_names = {s["name"] for s in SKILLS_REGISTRY}
    active_skill_names = {s["name"] for s in filtered_skills}
    skipped_skill_names = all_skill_names - active_skill_names

    if skipped_skill_names:
        print(f"\n🟢 Enabled: {len(active_skill_names)} skills")
        print(f"🔴 Disabled: {', '.join(sorted(skipped_skill_names))} (not suitable for project type)")
    else:
        print(f"\n🟢 Enabled: {len(active_skill_names)} skills (all)")

    print()

    # SCAN EXISTING CODEBASE
    print("🔬 Scanning the codebase...")
    scanner = ProjectScanner(target)
    scan_profile = scanner.scan()

    if scan_profile["has_existing_code"]:
        print(scanner.generate_report())
        print("✅ Will auto-populate Knowledge Base from real data!\n")
    else:
        print("📭 Empty project — use default templates.\n")


    # Generate
    generator = ProjectGenerator(
        target_dir=target,
        project_name=name,
        project_type=project_type,
        scan_profile=scan_profile,
        lang=lang,
        ai_agent=ai_agent,
        selected_skills=selected_skills,
        vault_path=getattr(args, 'vault', None) or os.environ.get("ANTIGRAVITY_SKILLS_VAULT"),
    )
    generator.generate()

    is_vi = lang.strip().lower() in ("vi", "vietnamese")
    
    if is_vi:
        print(f"\n✅ Khởi tạo/Nâng cấp thành công!")
        print(f"  📁 Thư mục .agent/ đã được tối ưu tại: {agent_dir}")
        print(f"  🏗️ Loại dự án: {type_info['label']}")
        print(f"  🎯 Kỹ năng:    {len(filtered_skills)} skills (Chuẩn ASF 3.3)")
        print(f"  🔄 Quy trình:  {len(filtered_workflows)} workflows")
        
        print(f"\n💡 Các bước tiếp theo:")
        print(f"  1. Kiểm tra '.agent/identity/master-identity.md' để AI nhận diện dự án")
        print(f"  2. Chạy /01-speckit.constitution để cập nhật Tech Stack & Docker Ports")
        if project_type in ("web_public", "fullstack"):
            print(f"  3. Chạy @speckit.seo để kiểm tra Technical SEO")
            print(f"  4. Chạy @speckit.geo để tối ưu hóa cho công cụ tìm kiếm AI (ChatGPT, Gemini)")
            print(f"  5. Kiểm tra '.agent/knowledge_base/seo_standards.md' để xem danh sách SEO checklist")
        elif project_type == "web_saas":
            print(f"  3. Chạy @speckit.seo cho Landing Page & Blog")
        else:
            print(f"  3. Chạy @speckit.devops để tạo môi trường Docker chuẩn bảo mật")
    else:
        print(f"\n✅ Initialization/Upgrade successful!")
        print(f"  📁 .agent/ has been optimized at: {agent_dir}")
        print(f"  🏗️ Type:      {type_info['label']}")
        print(f"  🎯 Skills:    {len(filtered_skills)} skills (ASF 3.3 Standard)")
        print(f"  🔄 Workflows: {len(filtered_workflows)} workflows")
        
        print(f"\n💡 Next steps:")
        print(f"  1. Check '.agent/identity/master-identity.md' to let AI identify the project")
        print(f"  2. Run /01-speckit.constitution to update Tech Stack & Docker Ports")
        if project_type in ("web_public", "fullstack"):
            print(f"  3. Run @speckit.seo to audit Technical SEO")
            print(f"  4. Run @speckit.geo to optimize for AI Search (ChatGPT, Gemini)")
            print(f"  5. Check '.agent/knowledge_base/seo_standards.md' for SEO checklist")
        elif project_type == "web_saas":
            print(f"  3. Run @speckit.seo for Landing Page & Blog")
        else:
            print(f"  3. Run @speckit.devops to create a Security-standard Docker environment")


    print()


def cmd_install(args):
    """Install specific skills into an existing .agent/ structure."""
    target = os.path.abspath(args.target or os.getcwd())
    agent_dir = os.path.join(target, ".agent")

    if not os.path.exists(agent_dir):
        print(f"❌ Error: Cannot find .agent/ folder at {target}")
        print("💡 Run: 'bro-skills init' to initialize the project first.")
        sys.exit(1)

    skills_input = args.skills
    if not skills_input:
        print("❌ Error: Please specify skills to install. Example: 'bro-skills install 3d'")
        sys.exit(1)

    selected_skills = [s.strip() for s in skills_input.split(",") if s.strip()]

    # Read existing project config to get project_type, lang, ai_agent, name
    import json
    project_type = "fullstack"
    project_name = os.path.basename(target)
    lang = "dynamic"
    ai_agent = "all"

    project_config_path = os.path.join(agent_dir, "project.json")
    if os.path.exists(project_config_path):
        try:
            with open(project_config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                project_type = config.get("project_type", project_type)
                project_name = config.get("name", project_name)
                lang = config.get("language", lang)
                ai_agent = config.get("ai_agent", ai_agent)
        except Exception:
            pass

    print(f"\n⚡ bro-skills v{__version__} - Installing Skills")
    print(f"{'─' * 50}")
    print(f"  📁 Target:  {target}")
    print(f"  🛠️ Skills:  {', '.join(selected_skills)}")
    print(f"{'─' * 50}\n")

    # Scan the codebase to configure scanner metadata
    scanner = ProjectScanner(target)
    scan_profile = scanner.scan()

    # Generate only selected skills
    generator = ProjectGenerator(
        target_dir=target,
        project_name=project_name,
        project_type=project_type,
        scan_profile=scan_profile,
        lang=lang,
        ai_agent=ai_agent,
        selected_skills=selected_skills,
        vault_path=getattr(args, 'vault', None) or os.environ.get("ANTIGRAVITY_SKILLS_VAULT"),
    )
    generator.install_skills()
    print()


def _audit_existing_agent(agent_dir):
    """Scan and compare existing structures."""
    report = {"is_legacy": False, "items": []}

    # 1. Check for new folders (ASF 3.3 Standard)
    standard_dirs = ["identity", "knowledge_base", "memory", "scripts/bash"]
    for d in standard_dirs:
        path = os.path.join(agent_dir, d)
        if not os.path.exists(path):
            report["is_legacy"] = True
            report["items"].append({"name": d, "status": "MISSING", "action": "New initialization"})
        else:
            report["items"].append({"name": d, "status": "OK", "action": "Keep it"})

    # 2. Check for odd/redundant files that do not belong to the new standard
    for item in os.listdir(agent_dir):
        if item in [".", "..", "skills", "workflows", "templates", "scripts", "identity", "knowledge_base", "memory", "README.md"]:
            continue
        report["is_legacy"] = True
        report["items"].append({"name": item, "status": "NON-STANDARD", "action": "Backup & Move"})

    # 3. Skills/Workflows always need core updates
    report["is_legacy"] = True
    report["items"].append({"name": "skills/", "status": "NEED UPDATE", "action": "Core upgrade"})
    report["items"].append({"name": "workflows/", "status": "NEED UPDATE", "action": "Core upgrade"})

    return report


def cmd_list_skills(args):
    """List all skills."""
    print(f"\n🧠 bro-skills - Skills Registry ({len(SKILLS_REGISTRY)} skills)")
    print(f"{'─' * 85}")
    print(f"  {'Skill':<25} {'Type':<12} {'Description'}")
    print(f"  {'─' * 23}   {'─' * 10}   {'─' * 45}")

    for skill in SKILLS_REGISTRY:
        ptype = skill.get("project_types", "all")
        print(f"  @{skill['name']:<23} {ptype:<12} {skill['description']}")

    print(f"\n💡 Use: @speckit.<name> in Antigravity to call skills")
    print(f"   Type: all=all projects, web=Web projects, web_public=Web B2C\n")


def cmd_list_workflows(args):
    """List all workflows."""
    print(f"\n🔄 bro-skills - Workflows Registry ({len(WORKFLOWS_REGISTRY)} workflows)")
    print(f"{'─' * 70}")
    print(f"  {'Command':<35} {'Description'}")
    print(f"  {'─' * 33}   {'─' * 33}")

    for wf in WORKFLOWS_REGISTRY:
        print(f"  /{wf['command']:<33} {wf['description']}")

    print(f"\n💡 Use: /<command> in Antigravity to run workflow\n")


def cmd_validate(args):
    """Validate the project's .agent/ structure."""
    target = os.path.abspath(args.target or os.getcwd())
    agent_dir = os.path.join(target, ".agent")

    print(f"\n🔍 Validating .agent/ at: {target}")
    print(f"{'─' * 50}\n")

    if not os.path.exists(agent_dir):
        print("❌ Cannot find .agent/ folder")
        print("💡 Run: bro-skills init to initialize\n")
        return

    results = validate_agent_structure(agent_dir)

    all_passed = True
    for check in results:
        status = "✅" if check["passed"] else "❌"
        print(f"  {status} {check['name']}")
        if not check["passed"]:
            all_passed = False
            for detail in check.get("details", []):
                print(f"     ⚠️  {detail}")

    print()
    if all_passed:
        print("✅ All checks are PASSED!\n")
    else:
        print("❌ Some tests FAILED. See details above.\n")


def cmd_version(args):
    """Show version."""
    print(f"bro-skills v{__version__}")


def _get_latest_github_version():
    """Retrieve the latest version of bro-skills from GitHub raw package.json."""
    import urllib.request
    import json
    
    url = "https://raw.githubusercontent.com/wedabro/bro-skills/main/package.json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'bro-skills-cli'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get("version")
    except Exception:
        return None


def cmd_update(args):
    """Upgrade bro-skills to the latest version."""
    import subprocess
    import shutil

    install_method = os.environ.get("BRO_SKILLS_INSTALL_METHOD", "pip")

    print("\n⚡ bro-skills - Checking for updates...")
    latest_version = _get_latest_github_version()
    
    if latest_version:
        if __version__ == latest_version:
            print(f"✅ You are already on the latest version (v{__version__}). No update needed.\n")
            return
        else:
            print(f"🔄 New version available: v{__version__} ➔ v{latest_version}")
    else:
        print("⚠️ Could not check for the latest version. Proceeding to update anyway...")

    print(f"Installation method: {install_method.upper()}")

    if install_method == "npm":
        cmd = ["npm", "install", "-g", "github:wedabro/bro-skills"]
    else:
        pip_cmd = "pip"
        if not shutil.which("pip") and shutil.which("pip3"):
            pip_cmd = "pip3"
        cmd = [sys.executable, "-m", pip_cmd, "install", "--upgrade", "git+https://github.com/wedabro/bro-skills.git"]

    print(f"Running command: {' '.join(cmd)}")
    try:
        is_windows = sys.platform.startswith('win')
        result = subprocess.run(cmd, check=True, text=True, shell=is_windows)
        if result.returncode == 0:
            print("\n✅ Updated successfully! Please run 'bro-skills version' to check.")
        else:
            print(f"\n❌ Update failed with error code: {result.returncode}")
    except Exception as e:
        print(f"\n❌ Error executing update command: {e}")
        if sys.platform.startswith('win'):
            print("\n💡 Tip: On Windows, updating directly from the running CLI might fail with 'Access is denied' (WinError 5) because the executable is currently in use.")
            print("Please close any active bro-skills processes and run the upgrade command manually in your terminal:")
        else:
            print(f"💡 You can run the following command to update manually:")
            
        if install_method == "npm":
            print("   npm install -g github:wedabro/bro-skills")
        else:
            print("   pip install --upgrade git+https://github.com/wedabro/bro-skills.git")


def main():
    if sys.platform.startswith('win'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(
        prog="bro-skills",
        description="⚡ bro-skills - Spec-Driven Development CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""For example:
    bro-skills init # Init at current directory
    bro-skills init --target /path/to/project # Init at the specified directory
    bro-skills init --name "My Project" # Init with project name
    bro-skills init --type web_public # Init for B2C Web (SEO/GEO enabled)
    bro-skills init --force # Init and override without asking
    bro-skills list-skills # View skills list
    bro-skills list-workflows # View list of workflows
    bro-skills validate # Validate the .agent/ structure
    bro-skills version # View version
    bro-skills update # Update to the latest version

Project type:
  web_public — Blog, E-commerce, Landing Page (SEO + GEO + Content)
  web_saas — Dashboard, Admin, API Service (SEO for Landing/Blog)
  mobile_app — iOS/Android (No SEO needed)
  desktop_cli — Electron, WPF, CLI Tool (No SEO needed)
  fullstack — Frontend Public + Backend API (SEO + GEO + DevOps)
  game — Game Dev (Unity/Unreal/Godot/Phaser) — gamedev + uiux
  simple_script — Small script/automation (soft rules, not forcing Docker)
  custom_infra — Private infrastructure (soft rules, no standard port enforcement)

NEW project process:
    bro-skills init → /01-speckit.constitution → /02-speckit.specify → /04-speckit.plan → /07-speckit.implement

AVAILABLE project process:
    bro-skills init → /01-speckit.constitution → /util-speckit.migrate → /02-speckit.specify → /07-speckit.implement"""
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # init
    init_parser = subparsers.add_parser("init", help="Initialize the .agent/ structure for the project")
    init_parser.add_argument("--target", "-t", help="Destination directory (default: current directory)")
    init_parser.add_argument("--name", "-n", help="Project name (default: folder name)")
    init_parser.add_argument(
        "--type",
        choices=PROJECT_TYPES.keys(),
        help="Project type: web_public, web_saas, mobile_app, desktop_cli, fullstack, simple_script, custom_infra",
    )
    init_parser.add_argument("--force", "-f", action="store_true", help="Overwrite .agent/ and force interactive setup prompts from scratch")
    init_parser.add_argument("--lang", "-l", help="Agent response language (e.g., en, vi, dynamic)")
    init_parser.add_argument("--ai", help="Specify target AI agent (e.g., claude, cursor, windsurf, antigravity, copilot, kiro, codex, roocode, qoder, gemini, trae, opencode, continue, all)")
    init_parser.add_argument("--skills", "-s", help="Comma-separated list of additional/specific skills to install (e.g. 3d,wordpress)")
    init_parser.add_argument("--vault", help="Path to external skill vault directory (e.g. F:\\code\\github\\antigravity-skills)")

    # install
    install_parser = subparsers.add_parser("install", help="Install specific skills into an existing .agent/ structure")
    install_parser.add_argument("skills", help="Comma-separated list of skills to install (e.g. 3d,wordpress)")
    install_parser.add_argument("--target", "-t", help="Destination directory (default: current directory)")
    install_parser.add_argument("--vault", help="Path to external skill vault directory (e.g. F:\\code\\github\\antigravity-skills)")

    # list-skills
    subparsers.add_parser("list-skills", help="List all skills")

    # list-workflows
    subparsers.add_parser("list-workflows", help="List all workflows")

    # validate
    validate_parser = subparsers.add_parser("validate", help="Validate the .agent/ structure")
    validate_parser.add_argument("--target", "-t", help="Destination directory (default: current directory)")

    # version
    subparsers.add_parser("version", help="Show version")

    # update
    subparsers.add_parser("update", help="Upgrade bro-skills to the latest version")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    commands = {
        "init": cmd_init,
        "install": cmd_install,
        "list-skills": cmd_list_skills,
        "list-workflows": cmd_list_workflows,
        "validate": cmd_validate,
        "version": cmd_version,
        "update": cmd_update,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
