import subprocess
import sys
from importlib.metadata import version

import bro_skills
from bro_skills.scanner import ProjectScanner


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
    result = subprocess.run(
        ["bro-skills", "version"],
        check=True,
        capture_output=True,
        text=True,
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
