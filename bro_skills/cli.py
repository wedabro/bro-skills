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


def _is_real_windows_console():
    if not sys.platform.startswith('win'):
        return True
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        h = kernel32.GetStdHandle(-10) # STD_INPUT_HANDLE
        mode = ctypes.c_uint32()
        return kernel32.GetConsoleMode(h, ctypes.byref(mode)) != 0
    except Exception:
        return True


def select_menu(options, title="", lang="en", multi=False):
    """
    options: list of tuples (value, label_en, label_vi)
    title: Title of the menu
    """
    import sys
    import shutil
    
    selected_idx = 0
    selected_indices = set()
    is_windows = sys.platform.startswith('win')
    
    # Track the last printed visual lines count to move cursor back down
    last_total_lines = [0]
    
    def print_menu():
        cols = shutil.get_terminal_size().columns
        
        # Calculate visual lines with wrapping
        visual_lines = 0
        for i, opt in enumerate(options):
            label = opt[2] if lang == "vi" else opt[1]
            if multi and opt[0] not in ("back", "cancel"):
                prefix = "[✓] " if i in selected_indices else "[ ] "
            else:
                prefix = ""
            text_len = len(prefix) + len(label) + 4
            visual_lines += max(1, (text_len + cols - 1) // cols)
            
        title_lines = max(1, (len(title) + cols - 1) // cols)
        total_lines = visual_lines + title_lines
        last_total_lines[0] = total_lines
        
        # Clear lines as we print
        sys.stdout.write(f"\r\033[K{title}\n")
        for i, opt in enumerate(options):
            label = opt[2] if lang == "vi" else opt[1]
            num_str = f"[{i + 1:2d}] " if opt[0] not in ("back", "cancel") else "     "
            if multi and opt[0] not in ("back", "cancel"):
                prefix = f"{num_str}[✓] " if i in selected_indices else f"{num_str}[ ] "
            else:
                prefix = num_str
            
            display_text = f"{prefix}{label}"
            if i == selected_idx:
                sys.stdout.write(f"\033[K\033[96m  ➔ {display_text}\033[0m\n")
            else:
                sys.stdout.write(f"\033[K    {display_text}\n")
        sys.stdout.write(f"\033[{total_lines}A")
        sys.stdout.flush()

    if not sys.stdout.isatty():
        return options[0][0]

    # Fallback to standard numeric input if stdin is not a real tty/console
    # (e.g. running in Git Bash/mintty on Windows without winpty)
    if not sys.stdin.isatty() or not _is_real_windows_console():
        print(f"\n{title}")
        for i, opt in enumerate(options):
            label = opt[2] if lang == "vi" else opt[1]
            print(f"  [{i + 1}] {label}")
        
        while True:
            try:
                if lang == "vi":
                    prompt = f"Nhập lựa chọn (chọn nhiều cách nhau bởi dấu phẩy, vd: 1,2) hoặc 'q' để hủy: " if multi else f"Nhập lựa chọn của bạn (1-{len(options)}) hoặc 'q' để hủy: "
                else:
                    prompt = f"Enter choice (multiple choices separated by comma, e.g. 1,2) or 'q' to cancel: " if multi else f"Enter your choice (1-{len(options)}) or 'q' to cancel: "
                val = input(prompt).strip()
                if val.lower() in ('q', 'cancel'):
                    return "cancel"
                
                if multi:
                    parts = [p.strip() for p in val.replace(" ", ",").split(",") if p.strip()]
                    selected_vals = []
                    is_back_or_cancel = False
                    for part in parts:
                        if part.lower() in ('q', 'cancel'):
                            return "cancel"
                        idx = int(part) - 1
                        if 0 <= idx < len(options):
                            opt_val = options[idx][0]
                            if opt_val in ("back", "cancel"):
                                is_back_or_cancel = opt_val
                            else:
                                selected_vals.append(opt_val)
                    if is_back_or_cancel and not selected_vals:
                        return is_back_or_cancel
                    if selected_vals:
                        return ",".join(selected_vals)
                else:
                    idx = int(val) - 1
                    if 0 <= idx < len(options):
                        return options[idx][0]
            except (ValueError, IndexError):
                pass
            except (KeyboardInterrupt, EOFError):
                return "cancel"
            
            if lang == "vi":
                print("❌ Lựa chọn không hợp lệ, vui lòng chọn lại.")
            else:
                print("❌ Invalid choice, please try again.")

    cols = shutil.get_terminal_size().columns
    initial_visual_lines = 0
    for i, opt in enumerate(options):
        label = opt[2] if lang == "vi" else opt[1]
        num_str = f"[{i + 1:2d}] " if opt[0] not in ("back", "cancel") else "     "
        if multi and opt[0] not in ("back", "cancel"):
            prefix = f"{num_str}[✓] " if i in selected_indices else f"{num_str}[ ] "
        else:
            prefix = num_str
        text_len = len(prefix) + len(label) + 4
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
                elif ch == b' ':
                    if multi and options[selected_idx][0] not in ("back", "cancel"):
                        if selected_idx in selected_indices:
                            selected_indices.remove(selected_idx)
                        else:
                            selected_indices.add(selected_idx)
                elif ch in (b'j', b'J', b's', b'S'):
                    selected_idx = (selected_idx + 1) % len(options)
                elif ch in (b'k', b'K', b'w', b'W'):
                    selected_idx = (selected_idx - 1) % len(options)
                elif ch and ch.isdigit():
                    num_val = int(ch.decode('ascii', errors='ignore'))
                    if 1 <= num_val <= len(options):
                        idx = num_val - 1
                        selected_idx = idx
                        if multi and options[idx][0] not in ("back", "cancel"):
                            if idx in selected_indices:
                                selected_indices.remove(idx)
                            else:
                                selected_indices.add(idx)
                        elif not multi:
                            break
                elif ch == b'\x1b':
                    if msvcrt.kbhit():
                        ch2 = msvcrt.getch()
                        if ch2 in (b'[', b'O'):
                            if msvcrt.kbhit():
                                ch3 = msvcrt.getch()
                                if ch3 in (b'A', b'H'):
                                    selected_idx = (selected_idx - 1) % len(options)
                                elif ch3 in (b'B', b'P'):
                                    selected_idx = (selected_idx + 1) % len(options)
                        elif ch2 in (b'A', b'H'):
                            selected_idx = (selected_idx - 1) % len(options)
                        elif ch2 in (b'B', b'P'):
                            selected_idx = (selected_idx + 1) % len(options)
                elif ch in (b'q', b'Q'):
                    return "cancel"
                elif ch in (b'\xe0', b'\x00'):
                    ch2 = msvcrt.getch()
                    if ch2 in (b'H', b'A'):
                        selected_idx = (selected_idx - 1) % len(options)
                    elif ch2 in (b'P', b'B'):
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
                    elif char1 == ' ':
                        if multi and options[selected_idx][0] not in ("back", "cancel"):
                            if selected_idx in selected_indices:
                                selected_indices.remove(selected_idx)
                            else:
                                selected_indices.add(selected_idx)
                    elif char1 in ('j', 'J', 's', 'S'):
                        selected_idx = (selected_idx + 1) % len(options)
                    elif char1 in ('k', 'K', 'w', 'W'):
                        selected_idx = (selected_idx - 1) % len(options)
                    elif char1.isdigit():
                        num_val = int(char1)
                        if 1 <= num_val <= len(options):
                            idx = num_val - 1
                            selected_idx = idx
                            if multi and options[idx][0] not in ("back", "cancel"):
                                if idx in selected_indices:
                                    selected_indices.remove(idx)
                                else:
                                    selected_indices.add(idx)
                            elif not multi:
                                break
                    elif char1 in ('q', 'Q'):
                        return "cancel"
                    elif char1 == '\x1b':
                        rlist, _, _ = select.select([sys.stdin], [], [], 0.35)
                        if rlist:
                            char2 = sys.stdin.read(1)
                            if char2 in ('[', 'O'):
                                rlist3, _, _ = select.select([sys.stdin], [], [], 0.35)
                                if rlist3:
                                    char3 = sys.stdin.read(1)
                                    if char3 in ('A', 'H'):
                                        selected_idx = (selected_idx - 1) % len(options)
                                    elif char3 in ('B', 'P'):
                                        selected_idx = (selected_idx + 1) % len(options)
                                    elif char3.isdigit():
                                        while True:
                                            rlist_ex, _, _ = select.select([sys.stdin], [], [], 0.1)
                                            if not rlist_ex:
                                                break
                                            ex = sys.stdin.read(1)
                                            if ex in ('A', 'H'):
                                                selected_idx = (selected_idx - 1) % len(options)
                                                break
                                            elif ex in ('B', 'P'):
                                                selected_idx = (selected_idx + 1) % len(options)
                                                break
                                            elif ex == '~':
                                                break
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    finally:
        # Move cursor down by the last printed total lines so we don't overwrite the final output
        sys.stdout.write(f"\033[{last_total_lines[0]}B\033[?25h\n")
        sys.stdout.flush()
        
    if multi:
        if options[selected_idx][0] in ("back", "cancel"):
            return options[selected_idx][0]
        if not selected_indices:
            curr_val = options[selected_idx][0]
            return curr_val
        selected_vals = [options[idx][0] for idx in sorted(selected_indices)]
        return ",".join(selected_vals)
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
        "wordpress": ("Website WordPress (Theme/Plugin)", "Phát triển Theme & Plugin WordPress — PHP, Gutenberg blocks, Interactivity API"),
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
    title = "🤖 Chọn cấu hình trợ lý AI (Space để tích/bỏ tích, Enter để xác nhận):" if lang == "vi" else "🤖 Select target AI agents (Space to select/deselect, Enter to confirm):"
    return select_menu(agents, title, lang, multi=True)


def cmd_init(args):
    """Initialize the .agent/ structure for the project."""
    target = os.path.abspath(args.target or os.getcwd())
    name = args.name or os.path.basename(target)
    force = getattr(args, 'force', False)
    project_type = getattr(args, 'type', None)
    agent_dir = os.path.join(target, ".agent")

    print(f"\n⚡ bro-skills v{__version__} — Antigravity Spec Framework 4.0 Elite")
    print(f"{'─' * 55}")
    print(f"  📁 Target:  {target}")
    print(f"  📛 Project: {name}")
    print(f"{'─' * 55}\n")

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
            print(f" - Upgrade core skills & workflows to version {__version__} (ASF 4.0 Elite standard)")
            print(" - Set up Identity & Knowledge Base layer to orient AI")
            print(" - Move old constitution to memory/constitution.md")

            response = input("\n🚀 Upgrade & Optimize to ASF 4.0 Elite now? (y/N): ").strip().lower()
            if response != 'y':
                print("❌ Canceled.")
                return
        else:
            print("✅ The current structure meets ASF 4.0 Elite standards.")
            response = input("♻️ Do you still want to reinstall (Re-init)? (y/N): ").strip().lower()
            if response != 'y':
                print("❌ Canceled.")
                return

    # LANGUAGE, AGENT, AND PROJECT TYPE SELECTION FLOW
    lang = getattr(args, 'lang', None) or existing_config.get("agent_language") or existing_config.get("language")
    project_type = getattr(args, 'type', None) or existing_config.get("project_type")
    ai_agent = getattr(args, 'ai', None)
    type_info = None

    # Check if we can auto-apply existing configurations without interactive prompt
    is_upgrade = os.path.exists(agent_dir) and not force
    if is_upgrade and lang and project_type:
        type_info = PROJECT_TYPES.get(project_type, PROJECT_TYPES["fullstack"])
        old_agent = existing_config.get("ai_agent") or existing_config.get("ai")
        
        print(f"ℹ️  Reusing existing configurations:")
        print(f"   - Language:  {lang}")
        print(f"   - Type:      {type_info['label']}")
        if old_agent:
            print(f"   - Previous AI Agent: {old_agent}")
        
        if getattr(args, 'ai', None):
            ai_agent = args.ai
            print(f"   - AI Agent:  {ai_agent}\n")
        else:
            if old_agent:
                if lang == "vi":
                    prompt_msg = f"\n❓ Bạn có muốn cấu hình cho IDE khác không? (y/N): "
                else:
                    prompt_msg = f"\n❓ Do you want to configure rules for a different IDE? (y/N): "
                
                change_ide = input(prompt_msg).strip().lower()
                if change_ide == 'y':
                    ai_agent = _ask_agent_selection(lang)
                    if ai_agent == "cancel" or ai_agent == "back":
                        print("❌ Canceled / Đã hủy.")
                        return
                    if lang == "vi":
                        print(f"✅ Cấu hình Agent mới đã chọn: {ai_agent}\n")
                    else:
                        print(f"✅ New selected AI Agent: {ai_agent}\n")
                else:
                    ai_agent = old_agent
                    if lang == "vi":
                        print(f"✅ Tiếp tục sử dụng cấu hình Agent cũ: {ai_agent}\n")
                    else:
                        print(f"✅ Reusing previous AI Agent: {ai_agent}\n")
            else:
                if lang == "vi":
                    print("\n⚠️  Không tìm thấy thông tin IDE trong cấu hình cũ. Vui lòng chọn:")
                else:
                    print("\n⚠️  No previous IDE configuration found. Please select:")
                ai_agent = _ask_agent_selection(lang)
                if ai_agent == "cancel" or ai_agent == "back":
                    print("❌ Canceled / Đã hủy.")
                    return
                if lang == "vi":
                    print(f"✅ Cấu hình Agent đã chọn: {ai_agent}\n")
                else:
                    print(f"✅ Selected AI Agent: {ai_agent}\n")
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
                            "custom_infra": "Hạ tầng tùy chỉnh",
                            "wordpress": "Website WordPress (Theme/Plugin)"
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
                                "custom_infra": "Hạ tầng tùy chỉnh",
                                "wordpress": "Website WordPress (Theme/Plugin)"
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
        force=force,
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
        force=getattr(args, 'force', False),
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


    print()


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


def _parse_version_tuple(v_str):
    """Parse version string into a comparable tuple of ints."""
    if not v_str:
        return (0, 0, 0)
    cleaned = v_str.lstrip("v").strip()
    parts = []
    for part in cleaned.split("."):
        digits = "".join(c for c in part if c.isdigit())
        parts.append(int(digits) if digits else 0)
    return tuple(parts)


def _get_latest_github_version():
    """Retrieve the latest version of bro-skills from GitHub Releases, Tags, or raw package metadata."""
    import urllib.request
    import json
    import time

    candidates = set()
    timestamp = int(time.time())
    headers = {
        'User-Agent': 'bro-skills-cli',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache'
    }

    # 1. Check GitHub Releases API
    try:
        url = f"https://api.github.com/repos/wedabro/bro-skills/releases/latest?t={timestamp}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            tag = data.get("tag_name", "").lstrip("v")
            if tag:
                candidates.add(tag)
    except Exception:
        pass

    # 2. Check GitHub Tags API
    try:
        url = f"https://api.github.com/repos/wedabro/bro-skills/tags?t={timestamp}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            if isinstance(data, list):
                for item in data[:5]:
                    t = item.get("name", "").lstrip("v")
                    if t:
                        candidates.add(t)
    except Exception:
        pass

    # 3. Check raw package.json on main branch
    try:
        url = f"https://raw.githubusercontent.com/wedabro/bro-skills/main/package.json?t={timestamp}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            v = data.get("version", "").lstrip("v")
            if v:
                candidates.add(v)
    except Exception:
        pass

    if not candidates:
        return None

    return max(candidates, key=_parse_version_tuple)




def _standalone_asset_name():
    """Return the release asset for the current supported standalone platform."""
    import platform

    machine = platform.machine().lower()
    if machine not in ("amd64", "x86_64"):
        raise RuntimeError(f"Standalone updates currently support x64 only (detected: {machine}).")
    if sys.platform.startswith("win"):
        return "bro-skills-windows-x86_64.exe"
    if sys.platform.startswith("linux"):
        return "bro-skills-linux-x86_64"
    raise RuntimeError(f"Standalone updates are not available for {sys.platform}.")


def _download_file(url, destination):
    """Download one release asset with a stable CLI user agent."""
    import urllib.request

    request = urllib.request.Request(url, headers={"User-Agent": "bro-skills-cli"})
    with urllib.request.urlopen(request, timeout=60) as response, open(destination, "wb") as output:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            output.write(chunk)


def _verify_sha256(path, checksum_path):
    """Verify a downloaded asset against its release checksum file."""
    import hashlib

    with open(checksum_path, "r", encoding="utf-8") as checksum_file:
        expected = checksum_file.read().strip().split()[0].lower()
    digest = hashlib.sha256()
    with open(path, "rb") as downloaded_file:
        for chunk in iter(lambda: downloaded_file.read(1024 * 1024), b""):
            digest.update(chunk)
    actual = digest.hexdigest()
    if actual != expected:
        raise RuntimeError(f"SHA-256 verification failed. Expected {expected}, downloaded {actual}.")


def _update_standalone(latest_version):
    """Download, verify, and replace a PyInstaller standalone executable."""
    import pathlib
    import shutil
    import subprocess
    import tempfile

    asset = _standalone_asset_name()
    base_url = "https://github.com/wedabro/bro-skills/releases/latest/download"
    temp_dir = pathlib.Path(tempfile.mkdtemp(prefix="bro-skills-update-"))
    staged = temp_dir / asset
    checksum = temp_dir / f"{asset}.sha256"

    try:
        print(f"Downloading {asset}...")
        _download_file(f"{base_url}/{asset}", staged)
        _download_file(f"{base_url}/{asset}.sha256", checksum)
        _verify_sha256(staged, checksum)

        target = pathlib.Path(sys.executable).resolve()
        if sys.platform.startswith("win"):
            updater = temp_dir / "finish-update.ps1"
            updater.write_text(
                "param([int]$ProcessId, [string]$Source, [string]$Target, [string]$TempDir)\n"
                "$ErrorActionPreference = 'SilentlyContinue'\n"
                "Wait-Process -Id $ProcessId -ErrorAction SilentlyContinue\n"
                "Start-Sleep -Seconds 1\n"
                "for ($i = 0; $i -lt 5; $i++) {\n"
                "    Move-Item -LiteralPath $Source -Destination $Target -Force\n"
                "    if ($?) { break }\n"
                "    Start-Sleep -Seconds 1\n"
                "}\n"
                "Remove-Item -LiteralPath $TempDir -Recurse -Force\n",
                encoding="utf-8",
            )
            creation_flags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
            subprocess.Popen(
                [
                    "powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass",
                    "-File", str(updater), str(os.getpid()), str(staged), str(target), str(temp_dir),
                ],
                creationflags=creation_flags,
            )
            print(f"✅ Update v{latest_version} verified and scheduled. Reopen your terminal shortly.")
            return

        pending = target.with_name(f"{target.name}.new")
        shutil.copy2(staged, pending)
        os.chmod(pending, 0o755)
        os.replace(pending, target)
        shutil.rmtree(temp_dir, ignore_errors=True)
        print(f"✅ Updated successfully to v{latest_version}.")
    except Exception:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise


def cmd_update(args):
    """Upgrade bro-skills to the latest version."""
    import subprocess
    import shutil

    force = getattr(args, "force", False)
    install_method = os.environ.get("BRO_SKILLS_INSTALL_METHOD", "pip")

    print("\n⚡ bro-skills - Checking for updates...")
    latest_version = _get_latest_github_version()
    
    if latest_version:
        if _parse_version_tuple(latest_version) <= _parse_version_tuple(__version__) and not force:
            print(f"✅ You are already on the latest version (v{__version__}). No update needed.")
            print("💡 Pass --force (or -f) to force re-installing/upgrading to the latest version.\n")
            return
        elif _parse_version_tuple(latest_version) > _parse_version_tuple(__version__):
            print(f"🔄 New version available: v{__version__} ➔ v{latest_version}")
        else:
            print(f"🔄 Re-installing version v{latest_version} (--force)...")
    else:
        print("⚠️ Could not check for the latest version online. Proceeding to update anyway...")

    if getattr(sys, "frozen", False):
        if not latest_version:
            print("❌ Cannot update the standalone executable without release information.")
            return
        try:
            _update_standalone(latest_version)
        except Exception as e:
            print(f"\n❌ Standalone update failed: {e}")
        return

    print(f"Installation method: {install_method.upper()}")
    is_windows = sys.platform.startswith('win')
    import time
    ts = int(time.time())

    # Check if pip module is available in current Python environment
    has_pip = False
    try:
        pip_check = subprocess.run([sys.executable, "-m", "pip", "--version"], capture_output=True, text=True)
        if pip_check.returncode == 0:
            has_pip = True
    except Exception:
        pass

    if install_method == "npm":
        cmd = ["npm", "install", "--no-cache", "-g", f"github:wedabro/bro-skills#main"]
        print(f"Running command: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, check=True, text=True, shell=is_windows)
            if result.returncode == 0:
                print("\n✅ Updated successfully! Please run 'bro-skills version' to check.")
                return
        except Exception as e:
            print(f"\n⚠️ Primary update command failed: {e}")
    elif has_pip:
        cmd = [sys.executable, "-m", "pip", "install", "--no-cache-dir", "--force-reinstall", "--no-deps", f"git+https://github.com/wedabro/bro-skills.git@main?t={ts}"]
        print(f"Running command: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, check=True, text=True, shell=is_windows)
            if result.returncode == 0:
                print("\n✅ Updated successfully! Please run 'bro-skills version' to check.")
                return
        except Exception as e:
            print(f"\n⚠️ Primary pip update command failed: {e}")

        # Fallback 1: Try raw zip archive via pip
        zip_url = f"https://github.com/wedabro/bro-skills/archive/refs/heads/main.zip?t={ts}"
        fallback_zip_cmd = [sys.executable, "-m", "pip", "install", "--no-cache-dir", "--force-reinstall", "--no-deps", zip_url]
        print(f"\n🔄 Retrying with fallback zip download via pip: {' '.join(fallback_zip_cmd)}")
        try:
            res_zip = subprocess.run(fallback_zip_cmd, check=True, text=True, shell=is_windows)
            if res_zip.returncode == 0:
                print("\n✅ Updated successfully via fallback archive! Please run 'bro-skills version' to check.")
                return
        except Exception as e2:
            print(f"⚠️ Fallback zip install failed: {e2}")

        if shutil.which("pipx"):
            pipx_cmd = ["pipx", "upgrade", "bro-skills"]
            try:
                res_pipx = subprocess.run(pipx_cmd, check=True, text=True, shell=is_windows)
                if res_pipx.returncode == 0:
                    print("\n✅ Updated successfully via pipx!")
                    return
            except Exception:
                pass

    # Pure Python stdlib update (works everywhere, no pip, no git, no npm required!)
    try:
        import urllib.request
        import zipfile
        import io

        print("\n🔄 Updating source package via Python stdlib...")
        url = f"https://github.com/wedabro/bro-skills/archive/refs/heads/main.zip?t={ts}"
        headers = {'User-Agent': 'bro-skills-cli', 'Cache-Control': 'no-cache, no-store'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            data = resp.read()

        target_dir = os.path.expanduser("~/.local/share/bro-skills")
        tmp_dir = os.path.expanduser("~/.local/share/bro-skills-tmp")
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir, ignore_errors=True)
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            zf.extractall(tmp_dir)

        extracted_src = os.path.join(tmp_dir, "bro-skills-main")
        if os.path.exists(extracted_src):
            if os.path.exists(target_dir):
                shutil.rmtree(target_dir, ignore_errors=True)
            shutil.copytree(extracted_src, target_dir)
            shutil.rmtree(tmp_dir, ignore_errors=True)
            print("\n✅ Updated successfully via Python source runner! Please run 'bro-skills version' to verify.")
            return
    except Exception as std_err:
        print(f"⚠️ Python stdlib update fallback failed: {std_err}")

    print("\n❌ Update failed. Please check your internet connection.")

def clean_empty_parents(path, root_dir):
    """Clean empty parent directories up to root_dir."""
    current = os.path.dirname(path)
    while current and current != root_dir and len(current) > len(root_dir):
        if os.path.exists(current) and os.path.isdir(current):
            try:
                if not os.listdir(current):
                    os.rmdir(current)
                else:
                    break
            except Exception:
                break
        current = os.path.dirname(current)


def cmd_uninstall(args):
    """Uninstall bro-skills by removing .agent/ and IDE rules from the project."""
    import shutil

    target = os.path.abspath(args.target or os.getcwd())
    force = getattr(args, 'force', False)
    agent_dir = os.path.join(target, ".agent")

    # If the user didn't specify --force, we should double check if .agent exists
    # If not even .agent exists and not force, we exit
    if not os.path.exists(agent_dir) and not force:
        print("❌ Không tìm thấy thư mục `.agent` tại dự án này.")
        return

    print(f"\n⚡ bro-skills - Gỡ cài đặt (Uninstall)")
    print(f"{'─' * 50}")
    print(f"  📁 Target:  {target}")
    print(f"{'─' * 50}\n")

    if not force:
        confirm = input("⚠️  Bạn có chắc chắn muốn gỡ bỏ hoàn toàn bro-skills khỏi dự án này không? (y/N): ").strip().lower()
        if confirm != 'y':
            print("❌ Đã hủy yêu cầu gỡ cài đặt.")
            return

    print("\n🧹 Bắt đầu gỡ bỏ các tệp và thư mục liên quan...")

    paths_to_delete = [
        ".agent",
        "AGENTS.md",
        "CLAUDE.md",
        ".clinerules",
        ".roomember",
        ".traerules",
        ".cursor/rules/bro-skills.mdc",
        ".windsurf/rules/bro-skills.md",
        ".github/copilot-instructions.md",
        ".aiassistant/rules/bro-skills.md",
        ".kiro/steering/tech.md",
        ".kiro/settings/mcp.json",
        ".kiro/skills",
        ".qoder/rules/bro-skills.md",
        ".opencode/rules/bro-skills.md",
        ".gemini/rules/bro-skills.md",
        ".continue/config.json",
        ".agents/AGENTS.md",
        ".agents/skills",
    ]

    deleted_count = 0
    for rel_path in paths_to_delete:
        abs_path = os.path.join(target, rel_path)
        if os.path.exists(abs_path) or os.path.islink(abs_path):
            success = False
            try:
                if os.path.islink(abs_path) or os.path.isfile(abs_path):
                    os.unlink(abs_path)
                    success = True
                elif os.path.isdir(abs_path):
                    if os.name == "nt":
                        try:
                            os.rmdir(abs_path)
                            success = True
                        except OSError:
                            shutil.rmtree(abs_path, ignore_errors=True)
                            success = True
                    else:
                        shutil.rmtree(abs_path, ignore_errors=True)
                        success = True
            except Exception as e:
                print(f"  ⚠️ Lỗi khi xóa {rel_path}: {e}")
            
            if success:
                print(f"  🗑️ Đã xóa: {rel_path}")
                deleted_count += 1
                clean_empty_parents(abs_path, target)

    print(f"\n✅ Hoàn tất gỡ bỏ! Đã dọn dẹp {deleted_count} tệp/thư mục.")


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
    bro-skills init → /01-speckit.constitution → /util-speckit.migrate → /02-speckit.specify → /07-speckit.implement"""
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")


def clean_empty_parents(path, root_dir):
    """Clean empty parent directories up to root_dir."""
    current = os.path.dirname(path)
    while current and current != root_dir and len(current) > len(root_dir):
        if os.path.exists(current) and os.path.isdir(current):
            try:
                if not os.listdir(current):
                    os.rmdir(current)
                else:
                    break
            except Exception:
                break
        current = os.path.dirname(current)


def cmd_uninstall(args):
    """Uninstall bro-skills by removing .agent/ and IDE rules from the project."""
    import shutil

    target = os.path.abspath(args.target or os.getcwd())
    force = getattr(args, 'force', False)
    agent_dir = os.path.join(target, ".agent")

    # If the user didn't specify --force, we should double check if .agent exists
    # If not even .agent exists and not force, we exit
    if not os.path.exists(agent_dir) and not force:
        print("❌ Không tìm thấy thư mục `.agent` tại dự án này.")
        return

    print(f"\n⚡ bro-skills - Gỡ cài đặt (Uninstall)")
    print(f"{'─' * 50}")
    print(f"  📁 Target:  {target}")
    print(f"{'─' * 50}\n")

    if not force:
        confirm = input("⚠️  Bạn có chắc chắn muốn gỡ bỏ hoàn toàn bro-skills khỏi dự án này không? (y/N): ").strip().lower()
        if confirm != 'y':
            print("❌ Đã hủy yêu cầu gỡ cài đặt.")
            return

    print("\n🧹 Bắt đầu gỡ bỏ các tệp và thư mục liên quan...")

    paths_to_delete = [
        ".agent",
        "AGENTS.md",
        "CLAUDE.md",
        ".clinerules",
        ".roomember",
        ".traerules",
        ".cursor/rules/bro-skills.mdc",
        ".windsurf/rules/bro-skills.md",
        ".github/copilot-instructions.md",
        ".aiassistant/rules/bro-skills.md",
        ".kiro/steering/tech.md",
        ".kiro/settings/mcp.json",
        ".kiro/skills",
        ".qoder/rules/bro-skills.md",
        ".opencode/rules/bro-skills.md",
        ".gemini/rules/bro-skills.md",
        ".continue/config.json",
        ".agents/AGENTS.md",
        ".agents/skills",
    ]

    deleted_count = 0
    for rel_path in paths_to_delete:
        abs_path = os.path.join(target, rel_path)
        if os.path.exists(abs_path) or os.path.islink(abs_path):
            success = False
            try:
                if os.path.islink(abs_path) or os.path.isfile(abs_path):
                    os.unlink(abs_path)
                    success = True
                elif os.path.isdir(abs_path):
                    if os.name == "nt":
                        try:
                            os.rmdir(abs_path)
                            success = True
                        except OSError:
                            shutil.rmtree(abs_path, ignore_errors=True)
                            success = True
                    else:
                        shutil.rmtree(abs_path, ignore_errors=True)
                        success = True
            except Exception as e:
                print(f"  ⚠️ Lỗi khi xóa {rel_path}: {e}")
            
            if success:
                print(f"  🗑️ Đã xóa: {rel_path}")
                deleted_count += 1
                clean_empty_parents(abs_path, target)

    print(f"\n✅ Hoàn tất gỡ bỏ! Đã dọn dẹp {deleted_count} tệp/thư mục.")


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
  wordpress — WordPress Theme & Plugin Development (PHP, Gutenberg blocks, Interactivity API)

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
        help="Project type: web_public, web_saas, mobile_app, desktop_cli, fullstack, simple_script, custom_infra, wordpress",
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
    install_parser.add_argument("--force", "-f", action="store_true", help="Force install and overwrite existing skills")

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
    update_parser = subparsers.add_parser("update", help="Upgrade bro-skills to the latest version")
    update_parser.add_argument("--force", "-f", action="store_true", help="Force re-installing/upgrading to the latest version")

    # uninstall
    uninstall_parser = subparsers.add_parser("uninstall", help="Remove all files and directories created by bro-skills")
    uninstall_parser.add_argument("--target", "-t", help="Destination directory (default: current directory)")
    uninstall_parser.add_argument("--force", "-f", action="store_true", help="Remove without confirmation")

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
        "uninstall": cmd_uninstall,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
