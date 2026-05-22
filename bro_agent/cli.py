#!/usr/bin/env python3
"""
⚡ bro-agent - Spec-Driven Development CLI
Entry point cho console script `bro-agent`.

Cài đặt global:
    pip install bro-agent
    bro-agent init --name "My Project"

Hoặc chạy trực tiếp:
    python -m bro_agent init --name "My Project"
"""

import argparse
import sys
import os

from bro_agent import __version__
from bro_agent.generator import ProjectGenerator
from bro_agent.scanner import ProjectScanner
from bro_agent.validators import validate_agent_structure
from bro_agent.registry import (
    SKILLS_REGISTRY, WORKFLOWS_REGISTRY, PROJECT_TYPES,
    get_skills_for_project_type, get_workflows_for_project_type,
)


def _ask_project_type():
    """Hỏi người dùng chọn loại dự án."""
    print("🏗️  Loại dự án:")
    types_list = list(PROJECT_TYPES.items())
    for i, (key, info) in enumerate(types_list, 1):
        print(f"  [{i}] {info['label']} — {info['description']}")

    while True:
        try:
            choice = input(f"\n  Chọn (1-{len(types_list)}): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(types_list):
                selected_key = types_list[idx][0]
                selected_info = types_list[idx][1]
                return selected_key, selected_info
        except (ValueError, IndexError):
            pass
        print(f"  ⚠️  Vui lòng chọn số từ 1 đến {len(types_list)}")


def cmd_init(args):
    """Khởi tạo cấu trúc .agent/ cho project."""
    target = os.path.abspath(args.target or os.getcwd())
    name = args.name or os.path.basename(target)
    force = getattr(args, 'force', False)
    project_type = getattr(args, 'type', None)
    agent_dir = os.path.join(target, ".agent")

    print(f"\n⚡ bro-agent v{__version__} - Spec-Driven Development")
    print(f"{'─' * 50}")
    print(f"  📁 Target:  {target}")
    print(f"  📛 Project: {name}")
    print(f"{'─' * 50}\n")

    # MIGRATION AUDIT LOGIC
    if os.path.exists(agent_dir) and not force:
        print("🔍 Đang quét cấu trúc .agent/ hiện có...")
        audit_report = _audit_existing_agent(agent_dir)

        if audit_report["is_legacy"]:
            print("\n⚠️  PHÁT HIỆN CẤU TRÚC CŨ (LEGACY AGENT)\n")
            print(f"  {'File/Folder':<25} {'Trạng thái':<15} {'Hướng xử lý'}")
            print(f"  {'─' * 23}   {'─' * 13}   {'─' * 18}")

            for item in audit_report["items"]:
                print(f"  {item['name']:<25} {item['status']:<15} {item['action']}")

            print("\n💡 Đề xuất tối ưu:")
            print("  - Nâng cấp core skills & workflows lên bản v1.0.0 (chuẩn ASF 3.3)")
            print("  - Thiết lập tầng Identity & Knowledge Base để 'gắn não' AI")
            print("  - Di chuyển hiến pháp cũ vào memory/constitution.md")

            response = input("\n🚀 Nâng cấp & Tối ưu hóa lên ASF 3.3 ngay? (y/N): ").strip().lower()
            if response != 'y':
                print("❌ Đã hủy.")
                return
        else:
            print("✅ Cấu trúc hiện tại đã đúng chuẩn ASF 3.3.")
            response = input("♻️  Bạn vẫn muốn cài đặt lại (Re-init)? (y/N): ").strip().lower()
            if response != 'y':
                print("❌ Đã hủy.")
                return

    # PROJECT TYPE SELECTION
    if not project_type:
        print()
        project_type, type_info = _ask_project_type()
        print(f"\n  ✅ Đã chọn: {type_info['label']}")
    else:
        type_info = PROJECT_TYPES.get(project_type, PROJECT_TYPES["fullstack"])
        print(f"  🏗️ Project Type: {type_info['label']}")

    # Lọc skills theo loại dự án
    filtered_skills = get_skills_for_project_type(project_type)
    filtered_workflows = get_workflows_for_project_type(project_type)

    # Hiển thị skills được bật/tắt
    all_skill_names = {s["name"] for s in SKILLS_REGISTRY}
    active_skill_names = {s["name"] for s in filtered_skills}
    skipped_skill_names = all_skill_names - active_skill_names

    if skipped_skill_names:
        print(f"\n  🟢 Bật:  {len(active_skill_names)} skills")
        print(f"  🔴 Tắt:  {', '.join(sorted(skipped_skill_names))} (không phù hợp loại dự án)")
    else:
        print(f"\n  🟢 Bật:  {len(active_skill_names)} skills (tất cả)")

    print()

    # SCAN EXISTING CODEBASE
    print("🔬 Đang quét codebase...")
    scanner = ProjectScanner(target)
    scan_profile = scanner.scan()

    if scan_profile["has_existing_code"]:
        print(scanner.generate_report())
        print("  ✅ Sẽ auto-populate Knowledge Base từ dữ liệu thật!\n")
    else:
        print("  📭 Dự án trống — sử dụng templates mặc định.\n")

    # Generate
    generator = ProjectGenerator(
        target_dir=target,
        project_name=name,
        project_type=project_type,
        scan_profile=scan_profile,
    )
    generator.generate()

    print(f"\n✅ Khởi tạo/Nâng cấp thành công!")
    print(f"  📂 .agent/ đã được tối ưu tại: {agent_dir}")
    print(f"  🏗️ Type:      {type_info['label']}")
    print(f"  🎯 Skills:    {len(filtered_skills)} skills (ASF 3.3 Standard)")
    print(f"  🔄 Workflows: {len(filtered_workflows)} workflows")

    # Hiển thị tips theo project type
    print(f"\n💡 Bước tiếp theo:")
    print(f"  1. Kiểm tra '.agent/identity/master-identity.md' để AI nhận diện dự án")
    print(f"  2. Chạy /01-speckit.constitution để cập nhật Tech Stack & Docker Ports")

    if project_type in ("web_public", "fullstack"):
        print(f"  3. Chạy @speckit.seo để audit Technical SEO")
        print(f"  4. Chạy @speckit.geo để tối ưu cho AI Search (ChatGPT, Gemini)")
        print(f"  5. Kiểm tra '.agent/knowledge_base/seo_standards.md' cho SEO checklist")
    elif project_type == "web_saas":
        print(f"  3. Chạy @speckit.seo cho Landing Page & Blog")
    else:
        print(f"  3. Chạy @speckit.devops để tạo Docker environment chuẩn Security")

    print()


def _audit_existing_agent(agent_dir):
    """Quét và so sánh cấu trúc hiện có."""
    report = {"is_legacy": False, "items": []}

    # 1. Kiểm tra các thư mục mới (Chuẩn ASF 3.3)
    standard_dirs = ["identity", "knowledge_base", "memory", "scripts/bash"]
    for d in standard_dirs:
        path = os.path.join(agent_dir, d)
        if not os.path.exists(path):
            report["is_legacy"] = True
            report["items"].append({"name": d, "status": "THIẾU", "action": "Khởi tạo mới"})
        else:
            report["items"].append({"name": d, "status": "OK", "action": "Giữ lại"})

    # 2. Kiểm tra files lẻ/thừa không thuộc chuẩn mới
    for item in os.listdir(agent_dir):
        if item in [".", "..", "skills", "workflows", "templates", "scripts", "identity", "knowledge_base", "memory", "README.md"]:
            continue
        report["is_legacy"] = True
        report["items"].append({"name": item, "status": "NON-STANDARD", "action": "Backup & Di chuyển"})

    # 3. Skills/Workflows luôn cần update core
    report["is_legacy"] = True
    report["items"].append({"name": "skills/", "status": "CẦN UPDATE", "action": "Nâng cấp Core"})
    report["items"].append({"name": "workflows/", "status": "CẦN UPDATE", "action": "Nâng cấp Core"})

    return report


def cmd_list_skills(args):
    """Liệt kê tất cả skills."""
    print(f"\n🧠 bro-agent - Skills Registry ({len(SKILLS_REGISTRY)} skills)")
    print(f"{'─' * 85}")
    print(f"  {'Skill':<25} {'Type':<12} {'Description'}")
    print(f"  {'─' * 23}   {'─' * 10}   {'─' * 45}")

    for skill in SKILLS_REGISTRY:
        ptype = skill.get("project_types", "all")
        print(f"  @{skill['name']:<23} {ptype:<12} {skill['description']}")

    print(f"\n💡 Sử dụng: @speckit.<name> trong Antigravity để gọi skill")
    print(f"   Type: all=mọi dự án, web=Web projects, web_public=Web B2C\n")


def cmd_list_workflows(args):
    """Liệt kê tất cả workflows."""
    print(f"\n🔄 bro-agent - Workflows Registry ({len(WORKFLOWS_REGISTRY)} workflows)")
    print(f"{'─' * 70}")
    print(f"  {'Command':<35} {'Description'}")
    print(f"  {'─' * 33}   {'─' * 33}")

    for wf in WORKFLOWS_REGISTRY:
        print(f"  /{wf['command']:<33} {wf['description']}")

    print(f"\n💡 Sử dụng: /<command> trong Antigravity để chạy workflow\n")


def cmd_validate(args):
    """Validate cấu trúc .agent/ của project."""
    target = os.path.abspath(args.target or os.getcwd())
    agent_dir = os.path.join(target, ".agent")

    print(f"\n🔍 Validating .agent/ tại: {target}")
    print(f"{'─' * 50}\n")

    if not os.path.exists(agent_dir):
        print("❌ Không tìm thấy thư mục .agent/")
        print("💡 Chạy: bro-agent init để khởi tạo\n")
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
        print("✅ Tất cả kiểm tra đều PASSED!\n")
    else:
        print("❌ Một số kiểm tra FAILED. Xem chi tiết ở trên.\n")


def cmd_version(args):
    """Hiển thị version."""
    print(f"bro-agent v{__version__}")


def main():
    parser = argparse.ArgumentParser(
        prog="bro-agent",
        description="⚡ bro-agent - Spec-Driven Development CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ:
    bro-agent init                              # Init tại thư mục hiện tại
    bro-agent init --target /path/to/project    # Init tại thư mục chỉ định
    bro-agent init --name "My Project"          # Init với tên project
    bro-agent init --type web_public            # Init cho Web B2C (bật SEO/GEO)
    bro-agent init --force                      # Init và ghi đè không hỏi
    bro-agent list-skills                       # Xem danh sách skills
    bro-agent list-workflows                    # Xem danh sách workflows
    bro-agent validate                          # Validate cấu trúc .agent/
    bro-agent version                           # Xem phiên bản

Loại dự án:
  web_public  — Blog, E-commerce, Landing Page (SEO + GEO + Content)
  web_saas    — Dashboard, Admin, API Service (SEO cho Landing/Blog)
  mobile_app  — iOS/Android (Không cần SEO)
  desktop_cli — Electron, WPF, CLI Tool (Không cần SEO)
  fullstack   — Frontend Public + Backend API (SEO + GEO + DevOps)

Quy trình dự án MỚI:
    bro-agent init → /01-speckit.constitution → /02-speckit.specify → /04-speckit.plan → /07-speckit.implement

Quy trình dự án CÓ SẴN:
    bro-agent init → /01-speckit.constitution → /util-speckit.migrate → /02-speckit.specify → /07-speckit.implement
        """
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Lệnh cần thực thi")

    # init
    init_parser = subparsers.add_parser("init", help="Khởi tạo cấu trúc .agent/ cho project")
    init_parser.add_argument("--target", "-t", help="Thư mục đích (mặc định: thư mục hiện tại)")
    init_parser.add_argument("--name", "-n", help="Tên project (mặc định: tên thư mục)")
    init_parser.add_argument("--type", help="Loại dự án: web_public, web_saas, mobile_app, desktop_cli, fullstack")
    init_parser.add_argument("--force", "-f", action="store_true", help="Ghi đè .agent/ nếu đã tồn tại")

    # list-skills
    subparsers.add_parser("list-skills", help="Liệt kê tất cả skills")

    # list-workflows
    subparsers.add_parser("list-workflows", help="Liệt kê tất cả workflows")

    # validate
    validate_parser = subparsers.add_parser("validate", help="Validate cấu trúc .agent/")
    validate_parser.add_argument("--target", "-t", help="Thư mục đích (mặc định: thư mục hiện tại)")

    # version
    subparsers.add_parser("version", help="Hiển thị phiên bản")

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
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
