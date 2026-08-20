import subprocess
import sys
import re
from importlib.metadata import version
from pathlib import Path

import bro_skills
from bro_skills.scanner import ProjectScanner
from bro_skills.validators import validate_agent_structure
from bro_skills.registry import (
    REPOSITORY_EXTENSION_SKILLS,
    SKILLS_REGISTRY,
    WORKFLOWS_REGISTRY,
    get_skills_for_project_type,
    resolve_builder_skills,
)
from bro_skills.skill_templates import SKILL_TEMPLATE_MAP
from bro_skills.templates import doc_ui_ux_standards_template
from bro_skills.workflow_templates import WORKFLOW_TEMPLATE_MAP


REPO_ROOT = Path(__file__).resolve().parents[1]


def _normalized_portable_skill(content):
    content = content.lstrip("\ufeff\r\n").replace("\r\n", "\n")
    before, header, body = content.split("---", 2)
    assert not before
    portable_header = "\n".join(
        line
        for line in header.splitlines()
        if not re.match(r"^(role|argument-hint):", line)
    )
    return re.sub(r"\s+", " ", f"{portable_header}\n{body}").strip()


def test_package_version_matches_metadata():
    assert bro_skills.__version__ == version("bro-skills")


def test_module_version_command_runs():
    result = subprocess.run(
        [sys.executable, "-m", "bro_skills", "version"],
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.stdout.strip() == f"bro-skills v{bro_skills.__version__}"


def test_console_script_version_command_runs():
    import sys
    import shutil
    cmd = shutil.which("bro-skills")
    args = [cmd, "version"] if cmd else [sys.executable, "-m", "bro_skills", "version"]
    result = subprocess.run(
        args,
        check=True,
        capture_output=True,
        text=True,
        shell=sys.platform.startswith("win"),
    )

    assert result.stdout.strip() == f"bro-skills v{bro_skills.__version__}"


def test_scanner_detects_python_project(tmp_path):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        "\n".join(
            [
                "[project]",
                'name = "demo-agent"',
                'version = "0.1.0"',
                'description = "Demo package"',
            ]
        ),
        encoding="utf-8",
    )

    profile = ProjectScanner(str(tmp_path)).scan()

    assert profile["has_existing_code"] is True
    assert profile["language"] == "Python"
    assert profile["project_name"] == "demo-agent"
    assert profile["project_version"] == "0.1.0"


def test_generator_scaffolds_with_language(tmp_path):
    import json
    from bro_skills.generator import ProjectGenerator
    
    generator = ProjectGenerator(
        target_dir=str(tmp_path),
        project_name="test-project",
        project_type="simple_script",
        lang="vi"
    )
    generator.generate()
    
    project_json_path = tmp_path / ".agents" / "project.json"
    assert project_json_path.exists()
    
    with open(project_json_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    assert config["agent_language"] == "vi"
    assert config["ai_agent"] == "all"
    
    rules_path = tmp_path / ".agents" / "rules" / "bro-skills.md"
    assert rules_path.exists()
    
    rules_content = rules_path.read_text(encoding="utf-8")
    assert "- Trả lời bằng tiếng Việt." in rules_content

    results = validate_agent_structure(str(tmp_path / ".agents"))
    assert all(result["passed"] for result in results), results

    skill_path = tmp_path / ".agents" / "skills" / "speckit.identity" / "SKILL.md"
    skill_content = skill_path.read_text(encoding="utf-8")
    assert skill_content.startswith("---\n")
    assert "\nrole:" not in skill_content.split("---", 2)[1]


def test_uninstall_removes_agent_structure(tmp_path):
    from bro_skills.generator import ProjectGenerator
    from bro_skills.cli import cmd_uninstall
    
    # 1. Generate scaffold
    generator = ProjectGenerator(
        target_dir=str(tmp_path),
        project_name="test-project",
        project_type="simple_script",
        lang="vi",
        ai_agent="all"
    )
    generator.generate()
    
    agent_dir = tmp_path / ".agents"
    assert agent_dir.exists()
    
    # Create some dummy rules to simulate what generator does
    cursor_rule = tmp_path / ".cursor" / "rules" / "bro-skills.mdc"
    cursor_rule.parent.mkdir(parents=True, exist_ok=True)
    cursor_rule.touch()
    assert cursor_rule.exists()
    
    # 2. Run uninstall
    class Args:
        target = str(tmp_path)
        force = True  # bypass prompt
        
    cmd_uninstall(Args())
    
    # 3. Verify files are removed
    assert not agent_dir.exists()
    assert not cursor_rule.exists()
    # Verify empty directories are cleaned up (like .cursor)
    assert not (tmp_path / ".cursor").exists()


def test_checked_in_skills_have_lean_valid_entrypoints():
    for skill_dir in (REPO_ROOT / ".agents" / "skills").iterdir():
        if not skill_dir.is_dir():
            continue

        skill_file = skill_dir / "SKILL.md"
        assert skill_file.is_file(), f"Missing {skill_file}"

        content = skill_file.read_text(encoding="utf-8")
        assert content.startswith("---\n"), f"Invalid frontmatter in {skill_file}"
        name_match = re.search(r"(?m)^name:\s*([^\r\n]+)", content)
        assert name_match and name_match.group(1).strip() == skill_dir.name
        assert len(content.splitlines()) <= 500, f"Move details from {skill_file} to references/"

        for target in re.findall(r"\[[^]]+\]\(([^)]+\.md)\)", content):
            assert (skill_dir / target).is_file(), f"Broken reference in {skill_file}: {target}"


def test_skill_registry_matches_embedded_templates_and_documented_extensions():
    registered = {skill["name"] for skill in SKILLS_REGISTRY}
    checked_in = {
        path.name
        for path in (REPO_ROOT / ".agents" / "skills").iterdir()
        if path.is_dir()
    }

    assert registered == set(SKILL_TEMPLATE_MAP)
    assert not checked_in - registered - set(REPOSITORY_EXTENSION_SKILLS)
    assert set(REPOSITORY_EXTENSION_SKILLS) <= checked_in


def test_checked_in_core_skills_match_embedded_templates_semantically():
    checked_in_root = REPO_ROOT / ".agents" / "skills"
    for name, template in SKILL_TEMPLATE_MAP.items():
        checked_in = checked_in_root / name / "SKILL.md"
        if not checked_in.exists():
            continue

        assert _normalized_portable_skill(
            checked_in.read_text(encoding="utf-8")
        ) == _normalized_portable_skill(template()), name


def test_frontend_policy_enforces_systemic_reuse_and_shared_tokens():
    frontend_sources = (
        (REPO_ROOT / ".agents/skills/speckit.frontend/SKILL.md").read_text(
            encoding="utf-8"
        ),
        SKILL_TEMPLATE_MAP["speckit.frontend"](),
    )
    for content in frontend_sources:
        assert "### 0. Mandatory Preflight" in content
        assert "shared application shell" in content
        assert "70% or more" in content
        assert "250–300 lines" in content
        assert "### 6. Verification and Completion Gate" in content
        assert "Cancel stale requests" in content
        assert "prefers-reduced-motion" in content
        assert "keyboard operation" in content

    checked_in_ui = (
        REPO_ROOT / ".agents/knowledge_base/ui_ux_standards.md"
    ).read_text(encoding="utf-8")
    generated_ui = doc_ui_ux_standards_template()
    assert re.sub(r"\s+", " ", checked_in_ui).strip() == re.sub(
        r"\s+", " ", generated_ui
    ).strip()

    for content in (checked_in_ui, generated_ui):
        assert "## 🧭 Systemic Layout & Ownership" in content
        assert "Single Change Point" in content
        assert "`gap-4` as the default gap" in content
        assert "## 📱 Responsive System" in content


def test_backend_policy_enforces_contract_safety_and_operational_reliability():
    backend_sources = (
        (REPO_ROOT / ".agents/skills/speckit.backend/SKILL.md").read_text(
            encoding="utf-8"
        ),
        SKILL_TEMPLATE_MAP["speckit.backend"](),
    )
    for content in backend_sources:
        assert "### 0. Preflight and Risk" in content
        assert "### 1. Contract-First API" in content
        assert "idempotency-key scope" in content
        assert "tenant isolation" in content
        assert "expand → backfill → switch → contract" in content
        assert "bounded retries with backoff and" in content
        assert "SLO-relevant" in content
        assert "contract tests for public interfaces" in content
        assert "### 7. Comprehensive 4-Layer Backend Optimization Standard" in content
        assert "Database Replication" in content
        assert "Asynchronous Execution & Message Queues" in content
        assert "Microservices & Load Balancing" in content
        assert "Auto-scaling Policies" in content


def test_core_engineering_specialists_are_registered_and_policy_complete():
    expected = {
        "speckit.identity-access": (
            "authorization code with\n  PKCE",
            "cross-tenant denial",
            "SCIM",
        ),
        "speckit.architecture": (
            "### 0. Context Discovery",
            "### 2. Decision Records",
            "superseding\n  ADR",
        ),
        "speckit.ddd": (
            "bounded contexts",
            "aggregate invariant",
            "outbox",
        ),
        "speckit.database": (
            "RPO",
            "untested backup",
            "restore/failover",
        ),
    }
    for name, clauses in expected.items():
        checked_in = (REPO_ROOT / ".agents/skills" / name / "SKILL.md").read_text(
            encoding="utf-8"
        )
        generated = SKILL_TEMPLATE_MAP[name]()
        for content in (checked_in, generated):
            for clause in clauses:
                assert clause in content, f"{name}: {clause}"


def test_workflow_registry_matches_templates_and_checked_in_files():
    registered = {workflow["command"] for workflow in WORKFLOWS_REGISTRY}
    checked_in = {
        path.stem for path in (REPO_ROOT / ".agents" / "workflows").glob("*.md")
    }

    assert registered == set(WORKFLOW_TEMPLATE_MAP)
    assert registered == checked_in


def test_checked_in_workflows_match_embedded_templates_semantically():
    checked_in_root = REPO_ROOT / ".agents" / "workflows"
    for name, template in WORKFLOW_TEMPLATE_MAP.items():
        checked_in = checked_in_root / f"{name}.md"
        assert re.sub(
            r"\s+", " ", checked_in.read_text(encoding="utf-8")
        ).strip() == re.sub(r"\s+", " ", template()).strip(), name


def test_workflow_skill_references_are_registered():
    skill_names = {skill["name"] for skill in SKILLS_REGISTRY}
    for workflow in WORKFLOWS_REGISTRY:
        unknown = set(workflow["skills"]) - skill_names
        assert not unknown, f"{workflow['command']} references unknown skills: {unknown}"


def test_documented_microservices_architecture_resolves_builders():
    resolved = resolve_builder_skills(
        "fullstack",
        {"architecture": "microservices"},
    )

    assert {"speckit.backend", "speckit.database", "speckit.devops"} <= set(resolved)


def test_non_docker_project_does_not_install_devops_skill():
    selected = {
        skill["name"] for skill in get_skills_for_project_type("simple_script")
    }

    assert "speckit.devops" not in selected
