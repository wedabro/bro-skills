import json
from pathlib import Path
import pytest

from bro_skills.scanner import ProjectScanner


def test_scan_package_json_valid(tmp_path: Path):
    pkg_file = tmp_path / "package.json"
    pkg_file.write_text(
        json.dumps({
            "name": "my-app",
            "version": "1.2.3",
            "description": "My test app",
            "dependencies": {
                "next": "^13.0.0",
                "react": "^18.0.0",
            },
            "devDependencies": {
                "typescript": "^5.0.0",
            },
            "scripts": {
                "build": "next build",
            },
        }),
        encoding="utf-8",
    )

    scanner = ProjectScanner(str(tmp_path))
    scanner._scan_package_json()

    assert scanner.profile["project_name"] == "my-app"
    assert scanner.profile["project_version"] == "1.2.3"
    assert scanner.profile["project_description"] == "My test app"
    assert scanner.profile["language"] == "TypeScript"
    assert "Next.js" in scanner.profile["tech_stack"]
    assert "React" in scanner.profile["tech_stack"]
    assert "TypeScript" in scanner.profile["tech_stack"]
    assert scanner.profile["package_manager"] == "npm"


def test_scan_package_json_malformed_json(tmp_path: Path):
    pkg_file = tmp_path / "package.json"
    pkg_file.write_text("{ malformed json ...", encoding="utf-8")

    scanner = ProjectScanner(str(tmp_path))
    scanner._scan_package_json()

    assert scanner.profile["project_name"] == ""
    assert scanner.profile["dependencies"] == {}


def test_scan_package_json_non_dict_root(tmp_path: Path):
    pkg_file = tmp_path / "package.json"
    pkg_file.write_text("[1, 2, 3]", encoding="utf-8")

    scanner = ProjectScanner(str(tmp_path))
    scanner._scan_package_json()

    assert scanner.profile["project_name"] == ""


def test_scan_package_json_non_dict_deps(tmp_path: Path):
    pkg_file = tmp_path / "package.json"
    pkg_file.write_text(
        json.dumps({
            "name": "app",
            "dependencies": "not-a-dict",
            "devDependencies": None,
        }),
        encoding="utf-8",
    )

    scanner = ProjectScanner(str(tmp_path))
    scanner._scan_package_json()

    assert scanner.profile["project_name"] == "app"
    assert scanner.profile["dependencies"] == {}
    assert scanner.profile["dev_dependencies"] == {}


def test_scan_package_json_pnpm_manager(tmp_path: Path):
    pkg_file = tmp_path / "package.json"
    pkg_file.write_text(json.dumps({"name": "pnpm-app"}), encoding="utf-8")
    (tmp_path / "pnpm-lock.yaml").touch()

    scanner = ProjectScanner(str(tmp_path))
    scanner._scan_package_json()

    assert scanner.profile["package_manager"] == "pnpm"
    assert "pnpm Monorepo" in scanner.profile["tech_stack"]


def test_scan_pyproject_valid(tmp_path: Path):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        '\n'.join([
            '[project]',
            'name = "fastapi-service"',
            'version = "0.4.0"',
            'description = "FastAPI Service"',
            'dependencies = ["fastapi"]',
        ]),
        encoding="utf-8",
    )

    scanner = ProjectScanner(str(tmp_path))
    scanner._scan_pyproject()

    assert scanner.profile["language"] == "Python"
    assert scanner.profile["project_name"] == "fastapi-service"
    assert scanner.profile["project_version"] == "0.4.0"
    assert scanner.profile["project_description"] == "FastAPI Service"
    assert "FastAPI" in scanner.profile["tech_stack"]
    assert "Python" in scanner.profile["tech_stack"]


def test_scan_pyproject_missing(tmp_path: Path):
    scanner = ProjectScanner(str(tmp_path))
    scanner._scan_pyproject()

    assert scanner.profile["language"] is None
    assert scanner.profile["project_name"] == ""


def test_scan_docker_valid(tmp_path: Path):
    (tmp_path / "Dockerfile").touch()
    compose = tmp_path / "docker-compose.yml"
    compose.write_text(
        '\n'.join([
            'services:',
            '  web:',
            '    ports:',
            '      - "8900:8000"',
            '  api:',
            '    ports:',
            '      - "8901:3000"',
        ]),
        encoding="utf-8",
    )
    (tmp_path / "docker-compose.prod.yml").touch()

    scanner = ProjectScanner(str(tmp_path))
    scanner._scan_docker()

    assert scanner.profile["docker"]["has_docker"] is True
    assert scanner.profile["docker"]["has_compose"] is True
    assert scanner.profile["docker"]["has_prod_compose"] is True
    assert "web" in scanner.profile["docker"]["services"]
    assert "api" in scanner.profile["docker"]["services"]
    assert "web: 8900:8000" in scanner.profile["docker"]["ports"]
    assert "Docker" in scanner.profile["tech_stack"]


def test_scan_docker_permission_error(monkeypatch, tmp_path: Path):
    compose = tmp_path / "docker-compose.yml"
    compose.touch()

    def fake_open(*args, **kwargs):
        raise PermissionError("Access denied")

    monkeypatch.setattr("builtins.open", fake_open)

    scanner = ProjectScanner(str(tmp_path))
    scanner._scan_docker()

    assert scanner.profile["docker"]["has_compose"] is True
    assert scanner.profile["docker"]["services"] == []


def test_scan_env_valid(tmp_path: Path):
    env_file = tmp_path / ".env.example"
    env_file.write_text(
        '\n'.join([
            '# Environment Variables',
            'PORT=8900',
            'DATABASE_URL=postgresql://localhost:5432/db',
            'SECRET_KEY=',
            '',
            '# Comment line',
        ]),
        encoding="utf-8",
    )

    scanner = ProjectScanner(str(tmp_path))
    scanner._scan_env()

    assert "PORT" in scanner.profile["env_vars"]
    assert "DATABASE_URL" in scanner.profile["env_vars"]
    assert "SECRET_KEY" in scanner.profile["env_vars"]
    assert len(scanner.profile["env_vars"]) == 3


def test_scan_env_permission_error(monkeypatch, tmp_path: Path):
    env_file = tmp_path / ".env.example"
    env_file.touch()

    def fake_open(*args, **kwargs):
        raise PermissionError("Permission denied")

    monkeypatch.setattr("builtins.open", fake_open)

    scanner = ProjectScanner(str(tmp_path))
    scanner._scan_env()

    assert scanner.profile["env_vars"] == []


def test_scan_readme_valid(tmp_path: Path):
    readme = tmp_path / "README.md"
    readme.write_text(
        '\n'.join([
            '# Project Title',
            '',
            'This is line 1 of project description.',
            'This is line 2 of project description.',
            'This is line 3 of project description.',
            '',
            '## Features',
            'Feature details...',
        ]),
        encoding="utf-8",
    )

    scanner = ProjectScanner(str(tmp_path))
    scanner._scan_readme()

    assert scanner.profile["project_description"] == (
        "This is line 1 of project description. "
        "This is line 2 of project description. "
        "This is line 3 of project description."
    )


def test_scan_readme_permission_error(monkeypatch, tmp_path: Path):
    readme = tmp_path / "README.md"
    readme.touch()

    def fake_open(*args, **kwargs):
        raise PermissionError("Read error")

    monkeypatch.setattr("builtins.open", fake_open)

    scanner = ProjectScanner(str(tmp_path))
    scanner._scan_readme()

    assert scanner.profile["project_description"] == ""


def test_scan_handles_nonexistent_directory(tmp_path: Path):
    nonexistent = tmp_path / "does_not_exist"
    scanner = ProjectScanner(str(nonexistent))
    profile = scanner.scan()

    assert isinstance(profile, dict)
    assert profile["has_existing_code"] is False
    assert profile["project_name"] == ""


def test_scan_handles_permission_error_on_listdir(monkeypatch, tmp_path: Path):
    def fake_listdir(*args, **kwargs):
        raise PermissionError("Directory read permission denied")

    monkeypatch.setattr("os.listdir", fake_listdir)

    scanner = ProjectScanner(str(tmp_path))
    profile = scanner.scan()

    assert isinstance(profile, dict)
    assert profile["source_structure"] == []


def test_scan_api_routes_root_and_nested(tmp_path: Path):
    root_api = tmp_path / "app" / "api"
    root_api.mkdir(parents=True)
    (root_api / "route.ts").touch()
    
    users_api = root_api / "users"
    users_api.mkdir()
    (users_api / "route.ts").touch()

    scanner = ProjectScanner(str(tmp_path))
    scanner._scan_api_routes()

    assert "/api" in scanner.profile["api"]["routes"]
    assert "/api/users" in scanner.profile["api"]["routes"]
    assert "/api/." not in scanner.profile["api"]["routes"]


def test_scan_docker_compose_ignores_non_service_sections_and_comments(tmp_path: Path):
    compose = tmp_path / "docker-compose.yml"
    compose.write_text(
        "\n".join([
            "services:",
            "  web:",
            "    ports:",
            "      - '8900:8000'",
            "    #   - '9999:9999'",
            "volumes:",
            "  db_data:",
            "networks:",
            "  app_net:",
        ]),
        encoding="utf-8",
    )

    scanner = ProjectScanner(str(tmp_path))
    scanner._scan_docker()

    assert "web" in scanner.profile["docker"]["services"]
    assert scanner.profile["docker"]["ports"] == ["web: 8900:8000"]
    assert "db_data" not in scanner.profile["docker"]["services"]
    assert "app_net" not in scanner.profile["docker"]["services"]


def test_scan_pages_with_api_docs_folder(tmp_path: Path):
    app_dir = tmp_path / "app"
    api_docs = app_dir / "api-docs"
    api_docs.mkdir(parents=True)
    (api_docs / "page.tsx").touch()
    (app_dir / "page.tsx").touch()

    scanner = ProjectScanner(str(tmp_path))
    scanner._scan_pages()

    assert "/" in scanner.profile["pages"]
    assert "/api-docs" in scanner.profile["pages"]


def test_scan_env_malformed_lines_and_export(tmp_path: Path):
    env_file = tmp_path / ".env.example"
    env_file.write_text(
        "\n".join([
            "# Comment line",
            "INVALID_LINE_WITHOUT_EQUALS",
            "export API_KEY=secret_123",
            "DB_HOST=localhost",
        ]),
        encoding="utf-8",
    )

    scanner = ProjectScanner(str(tmp_path))
    scanner._scan_env()

    assert "API_KEY" in scanner.profile["env_vars"]
    assert "DB_HOST" in scanner.profile["env_vars"]
    assert "INVALID_LINE_WITHOUT_EQUALS" not in scanner.profile["env_vars"]


def test_scan_readme_level2_heading(tmp_path: Path):
    readme = tmp_path / "README.md"
    readme.write_text(
        "\n".join([
            "## My Awesome Service",
            "This is the service description line 1.",
            "This is the service description line 2.",
        ]),
        encoding="utf-8",
    )

    scanner = ProjectScanner(str(tmp_path))
    scanner._scan_readme()

    assert scanner.profile["project_description"] == (
        "This is the service description line 1. "
        "This is the service description line 2."
    )


def test_scan_prisma_schema(tmp_path: Path):
    prisma_dir = tmp_path / "prisma"
    prisma_dir.mkdir()
    schema = prisma_dir / "schema.prisma"
    schema.write_text(
        "\n".join([
            'datasource db { provider = "postgresql" }',
            "model User {",
            "  id String @id",
            "  email String",
            "}",
        ]),
        encoding="utf-8",
    )

    scanner = ProjectScanner(str(tmp_path))
    scanner._scan_prisma()

    assert scanner.profile["database"]["has_prisma"] is True
    assert scanner.profile["database"]["type"] == "PostgreSQL"
    assert len(scanner.profile["database"]["models"]) == 1
    assert scanner.profile["database"]["models"][0]["name"] == "User"


def test_scan_report_and_generators(tmp_path: Path):
    scanner = ProjectScanner(str(tmp_path))
    scanner.profile["project_name"] = "test-proj"
    scanner.profile["project_version"] = "1.0.0"
    scanner.profile["framework"] = "Next.js"
    scanner.profile["tech_stack"] = ["Next.js", "React", "Prisma"]
    scanner.profile["docker"] = {
        "has_docker": True,
        "has_compose": True,
        "has_prod_compose": False,
        "services": ["web"],
        "ports": ["web: 8900:3000"],
    }
    scanner.profile["database"] = {
        "type": "PostgreSQL",
        "has_prisma": True,
        "models": [{"name": "User", "fields": ["id: String"]}],
        "schema_raw": "model User {}",
    }
    scanner.profile["api"]["routes"] = ["/api/users"]
    scanner.profile["pages"] = ["/"]
    scanner.profile["env_vars"] = ["DATABASE_URL"]

    report = scanner.generate_report()
    assert "test-proj" in report
    assert "Next.js" in report

    infra = scanner.generate_infrastructure_content()
    assert "Infrastructure & Docker Standards" in infra

    schema = scanner.generate_data_schema_content()
    assert "Data Schema" in schema

    api_std = scanner.generate_api_standards_content()
    assert "API Standards" in api_std

    biz_logic = scanner.generate_business_logic_content()
    assert "Business Logic" in biz_logic

    identity = scanner.generate_identity_context()
    assert "Framework: Next.js" in identity


def test_scan_catches_all_exceptions_in_scan_methods(monkeypatch, tmp_path: Path):
    scanner = ProjectScanner(str(tmp_path))

    def bugged_method():
        raise RuntimeError("Uncaught error inside detection method")

    monkeypatch.setattr(scanner, "_scan_package_json", bugged_method)
    profile = scanner.scan()

    assert isinstance(profile, dict)


def test_scan_pyproject_single_quotes(tmp_path: Path):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        '\n'.join([
            '[project]',
            "name = 'single-quote-service'",
            "version = '0.5.0'",
            "description = 'Single Quote Service Description'",
            'dependencies = ["flask"]',
        ]),
        encoding="utf-8",
    )

    scanner = ProjectScanner(str(tmp_path))
    scanner._scan_pyproject()
    scanner._detect_framework()

    assert scanner.profile["language"] == "Python"
    assert scanner.profile["project_name"] == "single-quote-service"
    assert scanner.profile["project_version"] == "0.5.0"
    assert scanner.profile["project_description"] == "Single Quote Service Description"
    assert scanner.profile["framework"] == "Flask"
    assert "Flask" in scanner.profile["tech_stack"]


def test_scan_docker_compose_host_ip_and_environment_vars(tmp_path: Path):
    compose = tmp_path / "docker-compose.yml"
    compose.write_text(
        "\n".join([
            "services:",
            "  web:",
            "    ports:",
            "      - '127.0.0.1:8902:80'",
            "    environment:",
            "      - TIME_RANGE=0800:1700",
            "  db:",
            "    image: postgres:15",
            "    environment:",
            "      - TIMEOUT=30:60",
        ]),
        encoding="utf-8",
    )

    scanner = ProjectScanner(str(tmp_path))
    scanner._scan_docker()

    assert "web" in scanner.profile["docker"]["services"]
    assert "db" in scanner.profile["docker"]["services"]
    assert scanner.profile["docker"]["ports"] == ["web: 8902:80"]


def test_scan_pages_route_groups(tmp_path: Path):
    app_dir = tmp_path / "app"
    marketing_about = app_dir / "(marketing)" / "about"
    marketing_about.mkdir(parents=True)
    (marketing_about / "page.tsx").touch()

    marketing_home = app_dir / "(marketing)" / "(home)"
    marketing_home.mkdir(parents=True)
    (marketing_home / "page.tsx").touch()

    scanner = ProjectScanner(str(tmp_path))
    scanner._scan_pages()

    assert "/about" in scanner.profile["pages"]
    assert "/" in scanner.profile["pages"]
    assert "/marketing/about" not in scanner.profile["pages"]


def test_scan_pages_pages_router(tmp_path: Path):
    pages_dir = tmp_path / "pages"
    pages_dir.mkdir(parents=True)
    (pages_dir / "index.tsx").touch()
    (pages_dir / "about.tsx").touch()

    scanner = ProjectScanner(str(tmp_path))
    scanner._scan_pages()

    assert "/" in scanner.profile["pages"]
    assert "/about" in scanner.profile["pages"]


def test_scan_env_dot_env_fallback(tmp_path: Path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join([
            "export API_KEY='secret_key'",
            "DATABASE_URL=postgresql://localhost/db",
        ]),
        encoding="utf-8",
    )

    scanner = ProjectScanner(str(tmp_path))
    scanner._scan_env()

    assert "API_KEY" in scanner.profile["env_vars"]
    assert "DATABASE_URL" in scanner.profile["env_vars"]


def test_scan_readme_lowercase_filename(tmp_path: Path):
    readme = tmp_path / "readme.md"
    readme.write_text(
        "\n".join([
            "# Lowercase Readme",
            "This description comes from a lowercase readme file.",
        ]),
        encoding="utf-8",
    )

    scanner = ProjectScanner(str(tmp_path))
    scanner._scan_readme()

    assert scanner.profile["project_description"] == "This description comes from a lowercase readme file."


