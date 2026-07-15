import subprocess
import sys
import re
from importlib.metadata import version
from pathlib import Path

import bro_skills
from bro_skills.scanner import ProjectScanner
from bro_skills.validators import validate_agent_structure


REPO_ROOT = Path(__file__).resolve().parents[1]


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
    result = subprocess.run(
        ["bro-skills", "version"],
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
    
    project_json_path = tmp_path / ".agent" / "project.json"
    assert project_json_path.exists()
    
    with open(project_json_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    assert config["agent_language"] == "vi"
    assert config["ai_agent"] == "all"
    
    rules_path = tmp_path / ".agent" / "rules" / "bro-skills.md"
    assert rules_path.exists()
    
    rules_content = rules_path.read_text(encoding="utf-8")
    assert "- Trả lời bằng tiếng Việt." in rules_content

    results = validate_agent_structure(str(tmp_path / ".agent"))
    assert all(result["passed"] for result in results), results

    skill_path = tmp_path / ".agent" / "skills" / "speckit.identity" / "SKILL.md"
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
    
    agent_dir = tmp_path / ".agent"
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
    for skill_dir in (REPO_ROOT / ".agent" / "skills").iterdir():
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
