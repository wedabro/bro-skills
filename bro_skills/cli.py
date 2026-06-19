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


def _ask_project_type():
    """Ask the user to select a project type."""
    print("🏗️ Project type:")
    types_list = list(PROJECT_TYPES.items())
    for i, (key, info) in enumerate(types_list, 1):
        print(f"  [{i}] {info['label']} — {info['description']}")

    while True:
        try:
            choice = input(f"\nSelect (1-{len(types_list)}): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(types_list):
                selected_key = types_list[idx][0]
                selected_info = types_list[idx][1]
                return selected_key, selected_info
        except (ValueError, IndexError):
            pass
        print(f"⚠️ Please choose a number from 1 to {len(types_list)}")


def _ask_agent_language():
    """Ask the user to select the agent response language."""
    print("🌐 Agent Response Language:")
    print("  [1] English (en)")
    print("  [2] Vietnamese (vi)")
    print("  [3] Dynamic (Detect dynamically based on user messages)")
    print("  [4] Other (Custom language)")

    while True:
        choice = input("\nSelect (1-4): ").strip()
        if choice == "1":
            return "en"
        elif choice == "2":
            return "vi"
        elif choice == "3":
            return "dynamic"
        elif choice == "4":
            custom_lang = input("Enter custom language (e.g., French, Japanese): ").strip()
            if custom_lang:
                return custom_lang
        print("⚠️ Please choose a number from 1 to 4")


def _ask_agent_selection():
    """Ask the user to select a target AI agent."""
    agents = [
        ("claude", "Claude Code (CLAUDE.md)"),
        ("cursor", "Cursor (.cursor/rules/bro-skills.mdc)"),
        ("windsurf", "Windsurf (.windsurf/rules/bro-skills.md)"),
        ("antigravity", "Antigravity (.agent/rules/bro-skills.md + AGENTS.md)"),
        ("copilot", "GitHub Copilot (.github/copilot-instructions.md)"),
        ("kiro", "Kiro (.kiro/steering/tech.md + MCP)"),
        ("codex", "Codex (skills.json in customizations root)"),
        ("roocode", "Roo Code (.clinerules + .roomember)"),
        ("qoder", "Qoder (.qoder/rules/bro-skills.md)"),
        ("gemini", "Gemini CLI (.gemini/rules/bro-skills.md)"),
        ("trae", "Trae (.traerules)"),
        ("opencode", "OpenCode (.opencode/rules/bro-skills.md)"),
        ("continue", "Continue (.continue/config.json)"),
        ("all", "All Assistants"),
    ]
    print("\n🤖 Target AI Agent Configuration:")
    for i, (key, desc) in enumerate(agents, 1):
        print(f"  [{i}] {desc}")

    while True:
        try:
            choice = input(f"\nSelect (1-{len(agents)}): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(agents):
                return agents[idx][0]
        except (ValueError, IndexError):
            pass
        print(f"⚠️ Please choose a number from 1 to {len(agents)}")


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

    # LANGUAGE SELECTION
    lang = getattr(args, 'lang', None)
    if not lang:
        print()
        lang = _ask_agent_language()
        print(f"\n✅ Selected language: {lang}")
    else:
        print(f"  🌐 Agent Language: {lang}")

    # AGENT SELECTION
    ai_agent = getattr(args, 'ai', None)
    if not ai_agent:
        print()
        ai_agent = _ask_agent_selection()
        print(f"\n✅ Selected AI Agent: {ai_agent}")
    else:
        print(f"  🤖 AI Agent: {ai_agent}")

    # PROJECT TYPE SELECTION
    if not project_type:
        print()
        project_type, type_info = _ask_project_type()
        print(f"\n✅ Selected: {type_info['label']}")
    else:
        type_info = PROJECT_TYPES.get(project_type, PROJECT_TYPES["fullstack"])
        print(f"  🏗️ Project Type: {type_info['label']}")

    # Filter skills by project type
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


def cmd_update(args):
    """Upgrade bro-skills to the latest version."""
    import subprocess
    import shutil

    install_method = os.environ.get("BRO_SKILLS_INSTALL_METHOD", "pip")

    print("\n⚡ bro-skills - Upgrading to the latest version...")
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
    init_parser.add_argument("--force", "-f", action="store_true", help="Overwrite .agent/ if it already exists")
    init_parser.add_argument("--lang", "-l", help="Agent response language (e.g., en, vi, dynamic)")
    init_parser.add_argument("--ai", help="Specify target AI agent (e.g., claude, cursor, windsurf, antigravity, copilot, kiro, codex, roocode, qoder, gemini, trae, opencode, continue, all)")

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
        "list-skills": cmd_list_skills,
        "list-workflows": cmd_list_workflows,
        "validate": cmd_validate,
        "version": cmd_version,
        "update": cmd_update,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
