"""
Validators - Validate cấu trúc .agent/ đã tạo.
"""

import os
from .registry import SKILLS_REGISTRY, WORKFLOWS_REGISTRY


def validate_agent_structure(agent_dir: str) -> list:
    """
    Validate cấu trúc .agent/ directory.
    Returns list of check results: [{name, passed, details}]
    """
    results = []

    # Check 1: .agent/ directory exists
    results.append({
        "name": "Thư mục .agent/ tồn tại",
        "passed": os.path.isdir(agent_dir),
        "details": [] if os.path.isdir(agent_dir) else ["Không tìm thấy thư mục .agent/"],
    })

    if not os.path.isdir(agent_dir):
        return results

    # Check 2: Core directories
    core_dirs = ["skills", "workflows", "templates", "scripts", "memory"]
    missing_dirs = []
    for d in core_dirs:
        if not os.path.isdir(os.path.join(agent_dir, d)):
            missing_dirs.append(d)

    results.append({
        "name": f"Thư mục core ({len(core_dirs)} dirs)",
        "passed": len(missing_dirs) == 0,
        "details": [f"Thiếu: {d}" for d in missing_dirs],
    })

    # Check 3: Skills directories & SKILL.md
    missing_skills = []
    incomplete_skills = []
    for skill in SKILLS_REGISTRY:
        skill_dir = os.path.join(agent_dir, "skills", skill["name"])
        skill_file = os.path.join(skill_dir, "SKILL.md")

        if not os.path.isdir(skill_dir):
            missing_skills.append(skill["name"])
        elif not os.path.isfile(skill_file):
            incomplete_skills.append(skill["name"])

    results.append({
        "name": f"Skills ({len(SKILLS_REGISTRY)} skills)",
        "passed": len(missing_skills) == 0 and len(incomplete_skills) == 0,
        "details": (
            [f"Thiếu thư mục: {s}" for s in missing_skills] +
            [f"Thiếu SKILL.md: {s}" for s in incomplete_skills]
        ),
    })

    # Check 4: Workflow files
    missing_workflows = []
    for wf in WORKFLOWS_REGISTRY:
        wf_file = os.path.join(agent_dir, "workflows", f"{wf['command']}.md")
        if not os.path.isfile(wf_file):
            missing_workflows.append(wf["command"])

    results.append({
        "name": f"Workflows ({len(WORKFLOWS_REGISTRY)} workflows)",
        "passed": len(missing_workflows) == 0,
        "details": [f"Thiếu: {w}.md" for w in missing_workflows],
    })

    # Check 5: Template files
    template_files = [
        "spec-template.md",
        "plan-template.md",
        "tasks-template.md",
        "constitution-template.md",
    ]
    missing_templates = []
    for t in template_files:
        if not os.path.isfile(os.path.join(agent_dir, "templates", t)):
            missing_templates.append(t)

    results.append({
        "name": f"Templates ({len(template_files)} templates)",
        "passed": len(missing_templates) == 0,
        "details": [f"Thiếu: {t}" for t in missing_templates],
    })

    # Check 6: Script files
    script_files = [
        "create-new-feature.sh",
        "setup-plan.sh",
        "check-prerequisites.sh",
        "update-agent-context.sh",
    ]
    missing_scripts = []
    for s in script_files:
        if not os.path.isfile(os.path.join(agent_dir, "scripts", "bash", s)):
            missing_scripts.append(s)

    results.append({
        "name": f"Scripts ({len(script_files)} scripts)",
        "passed": len(missing_scripts) == 0,
        "details": [f"Thiếu: {s}" for s in missing_scripts],
    })

    # Check 7: Constitution file
    constitution_file = os.path.join(agent_dir, "memory", "constitution.md")
    results.append({
        "name": "Constitution (memory/constitution.md)",
        "passed": os.path.isfile(constitution_file),
        "details": [] if os.path.isfile(constitution_file) else ["Thiếu constitution.md"],
    })

    # Check 8: README.md
    readme_file = os.path.join(agent_dir, "README.md")
    results.append({
        "name": "README.md",
        "passed": os.path.isfile(readme_file),
        "details": [] if os.path.isfile(readme_file) else ["Thiếu README.md"],
    })

    # Check 9: SKILL.md content quality (basic check)
    empty_skills = []
    for skill in SKILLS_REGISTRY:
        skill_file = os.path.join(agent_dir, "skills", skill["name"], "SKILL.md")
        if os.path.isfile(skill_file):
            size = os.path.getsize(skill_file)
            if size < 100:
                empty_skills.append(f"{skill['name']} ({size} bytes)")

    results.append({
        "name": "SKILL.md content quality (>100 bytes each)",
        "passed": len(empty_skills) == 0,
        "details": [f"Quá ngắn: {s}" for s in empty_skills],
    })

    # Check 10: Workflow frontmatter
    invalid_frontmatter = []
    wf_dir = os.path.join(agent_dir, "workflows")
    if os.path.isdir(wf_dir):
        for fname in os.listdir(wf_dir):
            if fname.endswith(".md"):
                fpath = os.path.join(wf_dir, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                if not content.startswith("---"):
                    invalid_frontmatter.append(fname)

    results.append({
        "name": "Workflow frontmatter (YAML header)",
        "passed": len(invalid_frontmatter) == 0,
        "details": [f"Thiếu frontmatter: {f}" for f in invalid_frontmatter],
    })

    return results
