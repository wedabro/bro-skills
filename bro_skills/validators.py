"""
Validators - Validate generated .agent/ structure.
"""

import os
import json
from .registry import (
    SKILLS_REGISTRY, WORKFLOWS_REGISTRY,
    get_skills_for_project_type, get_workflows_for_project_type,
)


def _load_project_config(agent_dir):
    """Read project.json to determine project_type + attributes (if any)."""
    cfg_path = os.path.join(agent_dir, "project.json")
    if not os.path.isfile(cfg_path):
        return None
    try:
        with open(cfg_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError, OSError):
        return None


def validate_agent_structure(agent_dir: str) -> list:
    """
    Validate .agent/ directory structure.
    Returns list of check results: [{name, passed, details}]

    Validates correct set of skills/workflows according to project_type + attributes in
    project.json. If project.json doesn't exist → fallback to validate the entire registry.
    """
    results = []

    # Check 1: .agent/ directory exists
    results.append({
        "name": "Directory .agent/ exists",
        "passed": os.path.isdir(agent_dir),
        "details": [] if os.path.isdir(agent_dir) else ["Directory .agent/ not found"],
    })

    if not os.path.isdir(agent_dir):
        return results

    # Determine the expected skill set/workflow according to project config
    cfg = _load_project_config(agent_dir)
    if cfg and cfg.get("project_type"):
        ptype = cfg["project_type"]
        attrs = cfg.get("attributes") or None
        expected_skills = get_skills_for_project_type(ptype, attrs)
        expected_workflows = get_workflows_for_project_type(ptype)
    else:
        expected_skills = SKILLS_REGISTRY
        expected_workflows = WORKFLOWS_REGISTRY

    # Check 2: Core directories
    core_dirs = ["skills", "workflows", "templates", "scripts", "memory"]
    missing_dirs = []
    for d in core_dirs:
        if not os.path.isdir(os.path.join(agent_dir, d)):
            missing_dirs.append(d)

    results.append({
        "name": f"Core directories ({len(core_dirs)} dirs)",
        "passed": len(missing_dirs) == 0,
        "details": [f"Missing: {d}" for d in missing_dirs],
    })

    # Check 3: Skills directories & SKILL.md
    missing_skills = []
    incomplete_skills = []
    for skill in expected_skills:
        skill_dir = os.path.join(agent_dir, "skills", skill["name"])
        skill_file = os.path.join(skill_dir, "SKILL.md")

        if not os.path.isdir(skill_dir):
            missing_skills.append(skill["name"])
        elif not os.path.isfile(skill_file):
            incomplete_skills.append(skill["name"])

    results.append({
        "name": f"Skills ({len(expected_skills)} skills)",
        "passed": len(missing_skills) == 0 and len(incomplete_skills) == 0,
        "details": (
            [f"Missing folder: {s}" for s in missing_skills] +
            [f"Missing SKILL.md: {s}" for s in incomplete_skills]
        ),
    })

    # Check 4: Workflow files
    missing_workflows = []
    for wf in expected_workflows:
        wf_file = os.path.join(agent_dir, "workflows", f"{wf['command']}.md")
        if not os.path.isfile(wf_file):
            missing_workflows.append(wf["command"])

    results.append({
        "name": f"Workflows ({len(expected_workflows)} workflows)",
        "passed": len(missing_workflows) == 0,
        "details": [f"Missing: {w}.md" for w in missing_workflows],
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
        "details": [f"Missing: {t}" for t in missing_templates],
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
        "details": [f"Missing: {s}" for s in missing_scripts],
    })

    # Check 7: Constitution file
    constitution_file = os.path.join(agent_dir, "memory", "constitution.md")
    results.append({
        "name": "Constitution (memory/constitution.md)",
        "passed": os.path.isfile(constitution_file),
        "details": [] if os.path.isfile(constitution_file) else ["Missing constitution.md"],
    })

    # Check 8: README.md
    readme_file = os.path.join(agent_dir, "README.md")
    results.append({
        "name": "README.md",
        "passed": os.path.isfile(readme_file),
        "details": [] if os.path.isfile(readme_file) else ["Missing README.md"],
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
        "details": [f"Too short: {s}" for s in empty_skills],
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
        "details": [f"Missing frontmatter: {f}" for f in invalid_frontmatter],
    })

    return results
