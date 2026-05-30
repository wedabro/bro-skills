"""
Scanner - Quét codebase hiện có để auto-populate .agent/ files.
Đọc hiểu dự án thông qua config files, source code, và cấu trúc thư mục.
"""

import os
import json
import re
import glob


class ProjectScanner:
    """Quét project directory để trích xuất thông tin thật."""

    def __init__(self, target_dir: str):
        self.target_dir = target_dir
        self.profile = {
            "has_existing_code": False,
            "tech_stack": [],
            "framework": None,
            "language": None,
            "package_manager": None,
            "dependencies": {},
            "dev_dependencies": {},
            "scripts": {},
            "docker": {
                "has_docker": False,
                "has_compose": False,
                "has_prod_compose": False,
                "services": [],
                "ports": [],
            },
            "database": {
                "type": None,
                "has_prisma": False,
                "models": [],
                "schema_raw": "",
            },
            "api": {
                "routes": [],
                "has_api_dir": False,
            },
            "pages": [],
            "env_vars": [],
            "project_description": "",
            "project_name": "",
            "project_version": "",
            "source_structure": [],
        }

    def scan(self):
        """Chạy toàn bộ quá trình quét."""
        self._scan_package_json()
        self._scan_pyproject()
        self._scan_docker()
        self._scan_prisma()
        self._scan_env()
        self._scan_api_routes()
        self._scan_pages()
        self._scan_readme()
        self._scan_source_structure()
        self._detect_framework()

        # Đánh dấu có code hay không
        if (self.profile["tech_stack"]
            or self.profile["dependencies"]
            or self.profile["dev_dependencies"]
            or self.profile["docker"]["has_docker"]
            or self.profile["docker"]["has_compose"]):
            self.profile["has_existing_code"] = True

        return self.profile

    # =========================================================================
    # PACKAGE.JSON
    # =========================================================================
    def _scan_package_json(self):
        """Đọc package.json để lấy dependencies, scripts, tên project."""
        pkg_path = os.path.join(self.target_dir, "package.json")
        if not os.path.exists(pkg_path):
            return

        try:
            with open(pkg_path, "r", encoding="utf-8") as f:
                pkg = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return

        self.profile["project_name"] = pkg.get("name", "")
        self.profile["project_version"] = pkg.get("version", "")
        self.profile["project_description"] = pkg.get("description", "")

        deps = pkg.get("dependencies", {})
        dev_deps = pkg.get("devDependencies", {})
        self.profile["dependencies"] = deps
        self.profile["dev_dependencies"] = dev_deps

        # Detect tech stack from deps
        all_deps = {**deps, **dev_deps}
        tech_map = {
            "next": "Next.js",
            "react": "React",
            "vue": "Vue.js",
            "express": "Express.js",
            "nestjs": "NestJS",
            "@nestjs/core": "NestJS",
            "prisma": "Prisma",
            "@prisma/client": "Prisma",
            "typescript": "TypeScript",
            "tailwindcss": "TailwindCSS",
            "@tailwindcss/postcss": "TailwindCSS",
            "postgres": "PostgreSQL",
            "pg": "PostgreSQL",
            "mysql2": "MySQL",
            "mongodb": "MongoDB",
            "mongoose": "MongoDB",
            "redis": "Redis",
            "ioredis": "Redis",
            "tsx": "TypeScript",
            "prisma-client-js": "Prisma",
        }
        for dep_name, tech_label in tech_map.items():
            if dep_name in all_deps and tech_label not in self.profile["tech_stack"]:
                self.profile["tech_stack"].append(tech_label)

        self.profile["scripts"] = pkg.get("scripts", {})
        self.profile["language"] = "JavaScript"
        if "typescript" in all_deps or "ts-node" in all_deps or "tsx" in all_deps:
            self.profile["language"] = "TypeScript"

        # Package manager detection
        if os.path.exists(os.path.join(self.target_dir, "pnpm-workspace.yaml")) or os.path.exists(os.path.join(self.target_dir, "pnpm-lock.yaml")):
            self.profile["package_manager"] = "pnpm"
            if "pnpm" not in self.profile["tech_stack"]:
                self.profile["tech_stack"].append("pnpm Monorepo")
        elif os.path.exists(os.path.join(self.target_dir, "yarn.lock")):
            self.profile["package_manager"] = "yarn"
        else:
            self.profile["package_manager"] = "npm"

    # =========================================================================
    # PYPROJECT.TOML
    # =========================================================================
    def _scan_pyproject(self):
        """Đọc pyproject.toml cho Python projects."""
        pyproject_path = os.path.join(self.target_dir, "pyproject.toml")
        if not os.path.exists(pyproject_path):
            return

        try:
            with open(pyproject_path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            return

        self.profile["language"] = "Python"
        if "Python" not in self.profile["tech_stack"]:
            self.profile["tech_stack"].append("Python")

        # Extract name
        name_match = re.search(r'name\s*=\s*"([^"]+)"', content)
        if name_match and not self.profile["project_name"]:
            self.profile["project_name"] = name_match.group(1)

        # Extract version
        ver_match = re.search(r'version\s*=\s*"([^"]+)"', content)
        if ver_match:
            self.profile["project_version"] = ver_match.group(1)

        # Extract description
        desc_match = re.search(r'description\s*=\s*"([^"]+)"', content)
        if desc_match and not self.profile["project_description"]:
            self.profile["project_description"] = desc_match.group(1)

        # Detect frameworks
        if "django" in content.lower():
            self.profile["tech_stack"].append("Django")
        if "fastapi" in content.lower():
            self.profile["tech_stack"].append("FastAPI")
        if "flask" in content.lower():
            self.profile["tech_stack"].append("Flask")

    # =========================================================================
    # DOCKER
    # =========================================================================
    def _scan_docker(self):
        """Quét Docker files để lấy services, ports."""
        # Dockerfile
        dockerfiles = glob.glob(os.path.join(self.target_dir, "**/Dockerfile"), recursive=True)
        if dockerfiles:
            self.profile["docker"]["has_docker"] = True
            if "Docker" not in self.profile["tech_stack"]:
                self.profile["tech_stack"].append("Docker")

        # docker-compose.yml
        for compose_name in ["docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml"]:
            compose_path = os.path.join(self.target_dir, compose_name)
            if os.path.exists(compose_path):
                self.profile["docker"]["has_compose"] = True
                self._parse_compose(compose_path)
                break

        # docker-compose.prod.yml
        for prod_name in ["docker-compose.prod.yml", "docker-compose.prod.yaml", "docker-compose.production.yml"]:
            prod_path = os.path.join(self.target_dir, prod_name)
            if os.path.exists(prod_path):
                self.profile["docker"]["has_prod_compose"] = True
                break

    def _parse_compose(self, filepath):
        """Parse docker-compose để lấy services và ports (simple parser)."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            return

        # Extract services (simple regex)
        in_services = False
        current_service = None
        indent_level = 0

        for line in content.split("\n"):
            stripped = line.strip()
            if stripped.startswith("services:"):
                in_services = True
                continue

            if in_services:
                # Service name (2-space indent, ends with :)
                if re.match(r"^  \w", line) and stripped.endswith(":") and not stripped.startswith("-"):
                    current_service = stripped.rstrip(":")
                    if current_service not in self.profile["docker"]["services"]:
                        self.profile["docker"]["services"].append(current_service)

                # Port mapping
                port_match = re.search(r'["\']?(\d+):(\d+)["\']?', stripped)
                if port_match and current_service:
                    port_entry = f"{current_service}: {port_match.group(1)}:{port_match.group(2)}"
                    if port_entry not in self.profile["docker"]["ports"]:
                        self.profile["docker"]["ports"].append(port_entry)

    # =========================================================================
    # PRISMA
    # =========================================================================
    def _scan_prisma(self):
        """Quét Prisma schema để lấy models."""
        # Check multiple possible paths
        schema_paths = [
            os.path.join(self.target_dir, "prisma", "schema.prisma"),
            os.path.join(self.target_dir, "packages", "database", "prisma", "schema.prisma"),
            os.path.join(self.target_dir, "apps", "api", "prisma", "schema.prisma"),
        ]

        schema_path = None
        for p in schema_paths:
            if os.path.exists(p):
                schema_path = p
                break

        if not schema_path:
            return

        self.profile["database"]["has_prisma"] = True
        if "Prisma" not in self.profile["tech_stack"]:
            self.profile["tech_stack"].append("Prisma")

        try:
            with open(schema_path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            return

        # Detect database type
        if 'provider = "postgresql"' in content:
            self.profile["database"]["type"] = "PostgreSQL"
            if "PostgreSQL" not in self.profile["tech_stack"]:
                self.profile["tech_stack"].append("PostgreSQL")
        elif 'provider = "mysql"' in content:
            self.profile["database"]["type"] = "MySQL"
        elif 'provider = "sqlite"' in content:
            self.profile["database"]["type"] = "SQLite"

        # Extract model names and their fields (summary)
        models = re.findall(r'model\s+(\w+)\s*\{([^}]+)\}', content, re.DOTALL)
        for model_name, model_body in models:
            fields = []
            for line in model_body.strip().split("\n"):
                line = line.strip()
                if not line or line.startswith("//") or line.startswith("@@"):
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    field_name = parts[0]
                    field_type = parts[1]
                    fields.append(f"{field_name}: {field_type}")

            self.profile["database"]["models"].append({
                "name": model_name,
                "fields": fields[:10],  # Limit to 10 fields per model
            })

        # Store raw schema (truncated)
        self.profile["database"]["schema_raw"] = content[:3000]

    # =========================================================================
    # ENV VARS
    # =========================================================================
    def _scan_env(self):
        """Quét .env.example hoặc .env để lấy tên biến (KHÔNG lấy giá trị)."""
        env_files = [".env.example", ".env.local.example", ".env.development"]
        for env_name in env_files:
            env_path = os.path.join(self.target_dir, env_name)
            if not os.path.exists(env_path):
                continue

            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        key = line.split("=")[0].strip()
                        if key and key not in self.profile["env_vars"]:
                            self.profile["env_vars"].append(key)
            except UnicodeDecodeError:
                pass
            break  # Only read first found

    # =========================================================================
    # API ROUTES
    # =========================================================================
    def _scan_api_routes(self):
        """Quét API routes từ cấu trúc thư mục."""
        # Next.js App Router
        api_dir = os.path.join(self.target_dir, "app", "api")
        if not os.path.exists(api_dir):
            api_dir = os.path.join(self.target_dir, "src", "app", "api")

        if os.path.exists(api_dir):
            self.profile["api"]["has_api_dir"] = True
            for root, dirs, files in os.walk(api_dir):
                for f in files:
                    if f in ("route.ts", "route.js"):
                        rel = os.path.relpath(root, api_dir)
                        route = "/api/" + rel.replace("\\", "/").replace("[", ":").replace("]", "")
                        if route not in self.profile["api"]["routes"]:
                            self.profile["api"]["routes"].append(route)

        # NestJS controllers
        src_dir = os.path.join(self.target_dir, "src")
        if os.path.exists(src_dir):
            for root, dirs, files in os.walk(src_dir):
                for f in files:
                    if f.endswith(".controller.ts") or f.endswith(".controller.js"):
                        controller_name = f.replace(".controller.ts", "").replace(".controller.js", "")
                        route = f"/api/{controller_name}"
                        if route not in self.profile["api"]["routes"]:
                            self.profile["api"]["routes"].append(route)

    # =========================================================================
    # PAGES
    # =========================================================================
    def _scan_pages(self):
        """Quét public pages từ cấu trúc thư mục."""
        # Next.js App Router pages
        app_dir = os.path.join(self.target_dir, "app")
        if not os.path.exists(app_dir):
            app_dir = os.path.join(self.target_dir, "src", "app")

        if os.path.exists(app_dir):
            for root, dirs, files in os.walk(app_dir):
                # Skip api, components, etc
                rel = os.path.relpath(root, app_dir)
                if rel.startswith("api") or rel.startswith("_"):
                    continue
                for f in files:
                    if f in ("page.tsx", "page.jsx", "page.ts", "page.js"):
                        if rel == ".":
                            page_route = "/"
                        else:
                            page_route = "/" + rel.replace("\\", "/").replace("(", "").replace(")", "")
                        if page_route not in self.profile["pages"]:
                            self.profile["pages"].append(page_route)

    # =========================================================================
    # README
    # =========================================================================
    def _scan_readme(self):
        """Đọc README để lấy mô tả dự án."""
        readme_path = os.path.join(self.target_dir, "README.md")
        if not os.path.exists(readme_path):
            return

        try:
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            return

        # Lấy nội dung sau heading đầu tiên (thường là mô tả)
        lines = content.split("\n")
        desc_lines = []
        found_heading = False
        for line in lines:
            if line.startswith("# ") and not found_heading:
                found_heading = True
                continue
            if found_heading:
                if line.startswith("## "):
                    break
                stripped = line.strip()
                if stripped and not stripped.startswith("[") and not stripped.startswith("!"):
                    desc_lines.append(stripped)
                if len(desc_lines) >= 3:
                    break

        if desc_lines and not self.profile["project_description"]:
            self.profile["project_description"] = " ".join(desc_lines)

    # =========================================================================
    # SOURCE STRUCTURE
    # =========================================================================
    def _scan_source_structure(self):
        """Quét cấu trúc thư mục cấp 1-2 để hiểu kiến trúc."""
        ignore_dirs = {
            "node_modules", ".git", ".next", ".agent", "__pycache__",
            "dist", "build", ".cache", ".turbo", "coverage",
            "test-output", "test-output-deep", "test-output-infra",
        }

        if not os.path.isdir(self.target_dir):
            return

        for item in sorted(os.listdir(self.target_dir)):
            if item.startswith(".") and item not in (".env.example",):
                if item == ".agent":
                    self.profile["source_structure"].append(f"📁 {item}/ (Agent config)")
                continue
            if item in ignore_dirs:
                continue

            full_path = os.path.join(self.target_dir, item)
            if os.path.isdir(full_path):
                # Count children
                try:
                    children = [c for c in os.listdir(full_path) if not c.startswith(".") and c not in ignore_dirs]
                    self.profile["source_structure"].append(f"📁 {item}/ ({len(children)} items)")
                except PermissionError:
                    self.profile["source_structure"].append(f"📁 {item}/")
            else:
                self.profile["source_structure"].append(f"📄 {item}")

    # =========================================================================
    # FRAMEWORK DETECTION
    # =========================================================================
    def _detect_framework(self):
        """Xác định framework chính từ tech stack."""
        ts = self.profile["tech_stack"]
        if "Next.js" in ts:
            self.profile["framework"] = "Next.js"
        elif "NestJS" in ts:
            self.profile["framework"] = "NestJS"
        elif "Django" in ts:
            self.profile["framework"] = "Django"
        elif "FastAPI" in ts:
            self.profile["framework"] = "FastAPI"
        elif "Express.js" in ts:
            self.profile["framework"] = "Express.js"
        elif "Vue.js" in ts:
            self.profile["framework"] = "Vue.js"
        elif "React" in ts:
            self.profile["framework"] = "React"

    # =========================================================================
    # REPORT GENERATION
    # =========================================================================
    def generate_report(self):
        """Tạo báo cáo scan dạng text."""
        p = self.profile
        lines = []
        lines.append("📊 KẾT QUẢ QUÉT DỰ ÁN")
        lines.append("─" * 50)

        if p["project_name"]:
            lines.append(f"  📛 Tên:        {p['project_name']}")
        if p["project_version"]:
            lines.append(f"  🏷️  Version:    {p['project_version']}")
        if p["framework"]:
            lines.append(f"  🏗️ Framework:  {p['framework']}")
        if p["language"]:
            lines.append(f"  💻 Language:   {p['language']}")
        if p["package_manager"]:
            lines.append(f"  📦 Pkg Mgr:    {p['package_manager']}")

        if p["tech_stack"]:
            lines.append(f"  🛠️ Tech Stack: {', '.join(p['tech_stack'])}")

        if p["docker"]["has_compose"]:
            lines.append(f"  🐳 Docker:     {len(p['docker']['services'])} services")
            for port in p["docker"]["ports"]:
                lines.append(f"     ├─ {port}")

        if p["database"]["has_prisma"]:
            lines.append(f"  🗄️ Database:   {p['database']['type']} ({len(p['database']['models'])} models)")
            for m in p["database"]["models"][:5]:
                lines.append(f"     ├─ {m['name']} ({len(m['fields'])} fields)")

        if p["api"]["routes"]:
            lines.append(f"  🌐 API Routes: {len(p['api']['routes'])}")
            for r in p["api"]["routes"][:8]:
                lines.append(f"     ├─ {r}")
            if len(p["api"]["routes"]) > 8:
                lines.append(f"     └─ ...và {len(p['api']['routes']) - 8} routes khác")

        if p["pages"]:
            lines.append(f"  📄 Pages:      {len(p['pages'])}")
            for pg in p["pages"][:8]:
                lines.append(f"     ├─ {pg}")

        if p["env_vars"]:
            lines.append(f"  🔑 ENV Vars:   {len(p['env_vars'])}")

        lines.append("─" * 50)
        return "\n".join(lines)

    # =========================================================================
    # KNOWLEDGE BASE CONTENT GENERATORS
    # =========================================================================
    def generate_infrastructure_content(self):
        """Tạo nội dung infrastructure.md từ dữ liệu thật."""
        p = self.profile
        sections = []
        sections.append("# 🏗️ Infrastructure & Docker Standards\n")
        sections.append(f"> Auto-generated by bro-skills Scanner\n")

        # Tech Stack
        if p["tech_stack"]:
            sections.append("## 🛠️ Tech Stack")
            for tech in p["tech_stack"]:
                sections.append(f"- {tech}")
            sections.append("")

        # Docker
        sections.append("## 📂 Environment Mapping")
        if p["docker"]["has_compose"]:
            sections.append("- **Local**: `docker-compose.yml` (Hot-reload, Dev-tools)")
            if p["docker"]["has_prod_compose"]:
                sections.append("- **Production**: `docker-compose.prod.yml` (Standalone, Hardened)")
            else:
                sections.append("- **Production**: [Chưa có — cần tạo `docker-compose.prod.yml`]")

            if p["docker"]["services"]:
                sections.append(f"\n### Services ({len(p['docker']['services'])})")
                for svc in p["docker"]["services"]:
                    sections.append(f"- `{svc}`")

            if p["docker"]["ports"]:
                sections.append(f"\n### Port Mapping")
                for port in p["docker"]["ports"]:
                    sections.append(f"- {port}")
        else:
            sections.append("- **Docker**: Chưa cấu hình — cần thiết lập Docker environment")
            sections.append("- **Ports**: Tuân thủ dải **8900-8999**")

        # ENV
        if p["env_vars"]:
            sections.append(f"\n## 🔑 Environment Variables ({len(p['env_vars'])})")
            for var in p["env_vars"]:
                sections.append(f"- `{var}`")

        # Security
        sections.append("\n## 🔒 Security Protocol")
        sections.append("- Use `.env.example` for all sensitive variables.")
        sections.append("- Production images use Alpine/Slim versions.")
        sections.append("- Firewall rules: Only expose mapped ports 89XX.")

        return "\n".join(sections)

    def generate_data_schema_content(self):
        """Tạo nội dung data_schema.md từ Prisma schema thật."""
        p = self.profile
        sections = []
        sections.append("# 📊 Data Schema\n")
        sections.append(f"> Auto-generated by bro-skills Scanner\n")

        if p["database"]["has_prisma"]:
            sections.append(f"## Database: {p['database']['type'] or 'Unknown'}")
            sections.append(f"Models: {len(p['database']['models'])}\n")

            for model in p["database"]["models"]:
                sections.append(f"### {model['name']}")
                sections.append("```")
                for field in model["fields"]:
                    sections.append(f"  {field}")
                sections.append("```\n")
        else:
            sections.append("## Database")
            sections.append("Chưa phát hiện Database schema.")
            sections.append("Khi thêm Prisma/SQL, chạy lại `bro-skills init` để cập nhật.\n")

        return "\n".join(sections)

    def generate_api_standards_content(self):
        """Tạo nội dung api_standards.md từ API routes thật."""
        p = self.profile
        sections = []
        sections.append("# 🌐 API Standards\n")
        sections.append(f"> Auto-generated by bro-skills Scanner\n")

        if p["api"]["routes"]:
            sections.append(f"## Discovered Routes ({len(p['api']['routes'])})")
            for route in p["api"]["routes"]:
                sections.append(f"- `{route}`")
            sections.append("")

        sections.append("## Conventions")
        sections.append("- Base URL: `/api/v1/`")
        sections.append("- Authentication: Bearer Token")
        sections.append("- Error format: `{ error: string, status: number }`")
        sections.append("- Pagination: `?page=1&limit=20`")
        sections.append("- Response: JSON with `data`, `meta` fields")

        return "\n".join(sections)

    def generate_business_logic_content(self):
        """Tạo nội dung business_logic.md từ source structure."""
        p = self.profile
        sections = []
        sections.append("# 💼 Business Logic\n")
        sections.append(f"> Auto-generated by bro-skills Scanner\n")

        if p["project_description"]:
            sections.append(f"## Mô tả dự án")
            sections.append(p["project_description"])
            sections.append("")

        if p["source_structure"]:
            sections.append("## Cấu trúc source")
            for item in p["source_structure"]:
                sections.append(f"  {item}")
            sections.append("")

        if p["pages"]:
            sections.append(f"## Public Pages ({len(p['pages'])})")
            for pg in p["pages"]:
                sections.append(f"- `{pg}`")
            sections.append("")

        sections.append("## Core Business Rules")
        sections.append("<!-- Điền logic nghiệp vụ cốt lõi của dự án tại đây -->")
        sections.append("<!-- VD: Quy trình đặt hàng, xử lý thanh toán, quản lý tồn kho... -->")

        return "\n".join(sections)

    def generate_identity_context(self):
        """Tạo context bổ sung cho Identity dựa trên scan."""
        p = self.profile
        parts = []
        if p["framework"]:
            parts.append(f"Framework: {p['framework']}")
        if p["language"]:
            parts.append(f"Language: {p['language']}")
        if p["tech_stack"]:
            parts.append(f"Tech: {', '.join(p['tech_stack'])}")
        if p["database"]["type"]:
            parts.append(f"DB: {p['database']['type']}")
        if p["docker"]["has_compose"]:
            parts.append(f"Docker: {len(p['docker']['services'])} services")

        return " | ".join(parts) if parts else ""

