import subprocess
import sys
from importlib.metadata import version

import bro_skills
from bro_skills.scanner import ProjectScanner
from bro_skills.validators import validate_agent_structure


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
