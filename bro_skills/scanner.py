"""
Scanner - Scan the existing codebase to auto-populate .agent/ files.
Understand the project through config files, source code, and folder structure.
"""

import os
import json
import re
import glob


class ProjectScanner:
    """Scan project directory to extract real information."""

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
        """Run the entire scan process."""
        for scan_func in [
            self._scan_package_json,
            self._scan_pyproject,
            self._scan_docker,
            self._scan_prisma,
            self._scan_env,
            self._scan_api_routes,
            self._scan_pages,
            self._scan_readme,
            self._scan_source_structure,
            self._detect_framework,
        ]:
            try:
                scan_func()
            except Exception:
                pass

        try:
            # Mark whether code exists
            if (self.profile.get("tech_stack")
                or self.profile.get("dependencies")
                or self.profile.get("dev_dependencies")
                or (isinstance(self.profile.get("docker"), dict) and (self.profile["docker"].get("has_docker") or self.profile["docker"].get("has_compose")))):
                self.profile["has_existing_code"] = True
        except Exception:
            pass

        return self.profile

    # =========================================================================
    # =========================================================================
    # PACKAGE.JSON
    # =========================================================================
    def _scan_package_json(self):
        """Read package.json to get dependencies, scripts, and project name."""
        pkg_path = os.path.join(self.target_dir, "package.json")
        try:
            if not os.path.exists(pkg_path):
                return

            with open(pkg_path, "r", encoding="utf-8") as f:
                pkg = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return

        if not isinstance(pkg, dict):
            return

        name = pkg.get("name")
        if isinstance(name, str):
            self.profile["project_name"] = name
        version = pkg.get("version")
        if isinstance(version, str):
            self.profile["project_version"] = version
        description = pkg.get("description")
        if isinstance(description, str):
            self.profile["project_description"] = description

        deps = pkg.get("dependencies")
        if not isinstance(deps, dict):
            deps = {}
        dev_deps = pkg.get("devDependencies")
        if not isinstance(dev_deps, dict):
            dev_deps = {}
        scripts = pkg.get("scripts")
        if not isinstance(scripts, dict):
            scripts = {}

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

        self.profile["scripts"] = scripts
        self.profile["language"] = "JavaScript"
        if "typescript" in all_deps or "ts-node" in all_deps or "tsx" in all_deps:
            self.profile["language"] = "TypeScript"

        # Package manager detection
        try:
            if os.path.exists(os.path.join(self.target_dir, "pnpm-workspace.yaml")) or os.path.exists(os.path.join(self.target_dir, "pnpm-lock.yaml")):
                self.profile["package_manager"] = "pnpm"
                if "pnpm Monorepo" not in self.profile["tech_stack"]:
                    self.profile["tech_stack"].append("pnpm Monorepo")
            elif os.path.exists(os.path.join(self.target_dir, "yarn.lock")):
                self.profile["package_manager"] = "yarn"
            elif os.path.exists(os.path.join(self.target_dir, "bun.lockb")) or os.path.exists(os.path.join(self.target_dir, "bun.lock")):
                self.profile["package_manager"] = "bun"
                if "Bun" not in self.profile["tech_stack"]:
                    self.profile["tech_stack"].append("Bun")
            else:
                self.profile["package_manager"] = "npm"
        except OSError:
            self.profile["package_manager"] = "npm"

    # =========================================================================
    # PYPROJECT.TOML
    # =========================================================================
    def _scan_pyproject(self):
        """Read pyproject.toml for Python projects."""
        pyproject_path = os.path.join(self.target_dir, "pyproject.toml")
        try:
            if not os.path.exists(pyproject_path):
                return

            with open(pyproject_path, "r", encoding="utf-8") as f:
                content = f.read()
        except (UnicodeDecodeError, OSError):
            return

        self.profile["language"] = "Python"
        if "Python" not in self.profile["tech_stack"]:
            self.profile["tech_stack"].append("Python")

        # Try tomllib standard library parsing first
        try:
            import tomllib
            data = tomllib.loads(content)
            if isinstance(data, dict):
                proj = data.get("project")
                if isinstance(proj, dict):
                    name = proj.get("name")
                    if isinstance(name, str) and name and not self.profile["project_name"]:
                        self.profile["project_name"] = name
                    version = proj.get("version")
                    if isinstance(version, str) and version:
                        self.profile["project_version"] = version
                    description = proj.get("description")
                    if isinstance(description, str) and description and not self.profile["project_description"]:
                        self.profile["project_description"] = description

                poetry = data.get("tool", {}).get("poetry") if isinstance(data.get("tool"), dict) else None
                if isinstance(poetry, dict):
                    name = poetry.get("name")
                    if isinstance(name, str) and name and not self.profile["project_name"]:
                        self.profile["project_name"] = name
                    version = poetry.get("version")
                    if isinstance(version, str) and version and not self.profile["project_version"]:
                        self.profile["project_version"] = version
                    description = poetry.get("description")
                    if isinstance(description, str) and description and not self.profile["project_description"]:
                        self.profile["project_description"] = description
        except Exception:
            pass

        # Regex fallback if metadata not found via tomllib
        if not self.profile["project_name"]:
            name_match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', content)
            if name_match:
                self.profile["project_name"] = name_match.group(1)

        if not self.profile["project_version"]:
            ver_match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
            if ver_match:
                self.profile["project_version"] = ver_match.group(1)

        if not self.profile["project_description"]:
            desc_match = re.search(r'description\s*=\s*["\']([^"\']+)["\']', content)
            if desc_match:
                self.profile["project_description"] = desc_match.group(1)

        # Detect frameworks
        if "django" in content.lower() and "Django" not in self.profile["tech_stack"]:
            self.profile["tech_stack"].append("Django")
        if "fastapi" in content.lower() and "FastAPI" not in self.profile["tech_stack"]:
            self.profile["tech_stack"].append("FastAPI")
        if "flask" in content.lower() and "Flask" not in self.profile["tech_stack"]:
            self.profile["tech_stack"].append("Flask")

    # =========================================================================
    # DOCKER
    # =========================================================================
    def _scan_docker(self):
        """Scan Docker files to get services and ports."""
        # Dockerfile
        try:
            dockerfiles = None
            try:
                dockerfiles = glob.glob("**/Dockerfile", root_dir=self.target_dir, recursive=True)
            except (TypeError, ValueError, OSError):
                pass
            if not dockerfiles:
                escaped_dir = glob.escape(self.target_dir)
                dockerfiles = glob.glob(os.path.join(escaped_dir, "**/Dockerfile"), recursive=True)
            if dockerfiles:
                self.profile["docker"]["has_docker"] = True
                if "Docker" not in self.profile["tech_stack"]:
                    self.profile["tech_stack"].append("Docker")
        except (OSError, RecursionError, ValueError):
            pass

        # docker-compose.yml
        for compose_name in ["docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml"]:
            compose_path = os.path.join(self.target_dir, compose_name)
            try:
                if os.path.exists(compose_path):
                    self.profile["docker"]["has_compose"] = True
                    self._parse_compose(compose_path)
                    break
            except (OSError, ValueError):
                continue

        # docker-compose.prod.yml
        for prod_name in ["docker-compose.prod.yml", "docker-compose.prod.yaml", "docker-compose.production.yml"]:
            prod_path = os.path.join(self.target_dir, prod_name)
            try:
                if os.path.exists(prod_path):
                    self.profile["docker"]["has_prod_compose"] = True
                    break
            except (OSError, ValueError):
                continue

    def _parse_compose(self, filepath):
        """Parse docker-compose to get services and ports (simple parser)."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except (UnicodeDecodeError, OSError):
            return

        in_services = False
        in_ports = False
        current_service = None

        for line in content.split("\n"):
            comment_idx = line.find("#")
            if comment_idx != -1:
                quote_count = line[:comment_idx].count('"') + line[:comment_idx].count("'")
                if quote_count % 2 == 0:
                    clean_line = line[:comment_idx]
                else:
                    clean_line = line
            else:
                clean_line = line

            stripped = clean_line.strip()
            if not stripped:
                continue

            # Top-level key check (no leading spaces/tabs)
            if not clean_line.startswith(" ") and not clean_line.startswith("\t"):
                if stripped.startswith("services:"):
                    in_services = True
                    current_service = None
                    in_ports = False
                else:
                    in_services = False
                    current_service = None
                    in_ports = False
                continue

            if in_services:
                # Service name (2-space indent, ends with :)
                if (re.match(r"^  [a-zA-Z0-9_-]+", clean_line) or re.match(r"^\t[a-zA-Z0-9_-]+", clean_line)) and stripped.endswith(":") and not stripped.startswith("-"):
                    current_service = stripped.rstrip(":")
                    in_ports = False
                    if current_service not in self.profile["docker"]["services"]:
                        self.profile["docker"]["services"].append(current_service)
                    continue

                if current_service:
                    if stripped.startswith("ports:"):
                        in_ports = True
                        subbed_line = re.sub(r'\$\{[^:]+:-([^}]+)\}', r'\1', stripped)
                        for port_match in re.finditer(r'(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:)?(\d+):(\d+)', subbed_line):
                            host_port, container_port = port_match.group(1), port_match.group(2)
                            if 1 <= int(host_port) <= 65535 and 1 <= int(container_port) <= 65535:
                                port_entry = f"{current_service}: {host_port}:{container_port}"
                                if port_entry not in self.profile["docker"]["ports"]:
                                    self.profile["docker"]["ports"].append(port_entry)
                        continue

                    # If key at service-level indent change (e.g., environment:, volumes:)
                    if not clean_line.startswith("      ") and not clean_line.startswith("    -") and not clean_line.startswith("\t\t\t") and not clean_line.startswith("\t\t-"):
                        if not stripped.startswith("-") and not stripped.startswith("ports:"):
                            in_ports = False

                    if in_ports:
                        subbed_line = re.sub(r'\$\{[^:]+:-([^}]+)\}', r'\1', stripped)
                        for port_match in re.finditer(r'(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:)?(\d+):(\d+)', subbed_line):
                            host_port, container_port = port_match.group(1), port_match.group(2)
                            if 1 <= int(host_port) <= 65535 and 1 <= int(container_port) <= 65535:
                                port_entry = f"{current_service}: {host_port}:{container_port}"
                                if port_entry not in self.profile["docker"]["ports"]:
                                    self.profile["docker"]["ports"].append(port_entry)

    # =========================================================================
    # PRISMA
    # =========================================================================
    def _scan_prisma(self):
        """Scan Prisma schema to get models."""
        schema_paths = [
            os.path.join(self.target_dir, "prisma", "schema.prisma"),
            os.path.join(self.target_dir, "packages", "database", "prisma", "schema.prisma"),
            os.path.join(self.target_dir, "apps", "api", "prisma", "schema.prisma"),
        ]

        schema_path = None
        for p in schema_paths:
            try:
                if os.path.exists(p):
                    schema_path = p
                    break
            except OSError:
                continue

        if not schema_path:
            return

        self.profile["database"]["has_prisma"] = True
        if "Prisma" not in self.profile["tech_stack"]:
            self.profile["tech_stack"].append("Prisma")

        try:
            with open(schema_path, "r", encoding="utf-8") as f:
                content = f.read()
        except (UnicodeDecodeError, OSError):
            return

        # Detect database type
        provider_match = re.search(r'provider\s*=\s*["\']([^"\']+)["\']', content, re.IGNORECASE)
        if provider_match:
            p_val = provider_match.group(1).lower()
            db_type = None
            if p_val in ("postgresql", "postgres"):
                db_type = "PostgreSQL"
            elif p_val == "mysql":
                db_type = "MySQL"
            elif p_val == "sqlite":
                db_type = "SQLite"
            elif p_val == "mongodb":
                db_type = "MongoDB"
            elif p_val in ("sqlserver", "sql-server"):
                db_type = "SQL Server"
            elif p_val == "cockroachdb":
                db_type = "CockroachDB"

            if db_type:
                self.profile["database"]["type"] = db_type
                if db_type not in self.profile["tech_stack"]:
                    self.profile["tech_stack"].append(db_type)

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
        """Scan .env.example or .env to get variable names (DO NOT get values)."""
        env_files = [".env.example", ".env.local.example", ".env.development", ".env", ".env.local", ".env.test"]
        for env_name in env_files:
            env_path = os.path.join(self.target_dir, env_name)
            try:
                if not os.path.exists(env_path):
                    continue

                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#") or "=" not in line:
                            continue
                        key = line.split("=")[0].strip()
                        key = re.sub(r"^export\s+", "", key).strip()
                        key = key.strip("'\"")
                        if key and key not in self.profile["env_vars"]:
                            self.profile["env_vars"].append(key)
                break  # Only read first found
            except (UnicodeDecodeError, OSError):
                continue

    # =========================================================================
    # API ROUTES
    # =========================================================================
    def _scan_api_routes(self):
        """Scan API routes from folder structure."""
        try:
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
                            if rel == ".":
                                route = "/api"
                            else:
                                route = "/api/" + rel.replace("\\", "/").replace("[", ":").replace("]", "")
                            if route not in self.profile["api"]["routes"]:
                                self.profile["api"]["routes"].append(route)
        except OSError:
            pass

        try:
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
        except OSError:
            pass

        try:
            # Next.js Pages Router API routes
            pages_api_dir = os.path.join(self.target_dir, "pages", "api")
            if not os.path.exists(pages_api_dir):
                pages_api_dir = os.path.join(self.target_dir, "src", "pages", "api")

            if os.path.exists(pages_api_dir):
                self.profile["api"]["has_api_dir"] = True
                for root, dirs, files in os.walk(pages_api_dir):
                    rel = os.path.relpath(root, pages_api_dir)
                    norm_rel = rel.replace("\\", "/")
                    for f in files:
                        if f.endswith((".ts", ".js")) and not f.startswith("_") and not any(ext in f for ext in (".test.", ".spec.", ".d.ts")):
                            filename_no_ext = os.path.splitext(f)[0]
                            if filename_no_ext == "index":
                                if rel == ".":
                                    route = "/api"
                                else:
                                    route = "/api/" + norm_rel
                            else:
                                if rel == ".":
                                    route = "/api/" + filename_no_ext
                                else:
                                    route = "/api/" + norm_rel + "/" + filename_no_ext
                            route = route.replace("[", ":").replace("]", "")
                            if route not in self.profile["api"]["routes"]:
                                self.profile["api"]["routes"].append(route)
        except OSError:
            pass

    # =========================================================================
    # PAGES
    # =========================================================================
    def _scan_pages(self):
        """Scan public pages from folder structure."""
        try:
            # Next.js App Router pages
            app_dir = os.path.join(self.target_dir, "app")
            if not os.path.exists(app_dir):
                app_dir = os.path.join(self.target_dir, "src", "app")

            if os.path.exists(app_dir):
                for root, dirs, files in os.walk(app_dir):
                    rel = os.path.relpath(root, app_dir)
                    norm_rel = rel.replace("\\", "/")
                    rel_parts = norm_rel.split("/")
                    if "api" in rel_parts or any(p.startswith("_") for p in rel_parts):
                        continue
                    for f in files:
                        if f in ("page.tsx", "page.jsx", "page.ts", "page.js"):
                            if rel == ".":
                                page_route = "/"
                            else:
                                path_segments = [p for p in rel_parts if not (p.startswith("(") and p.endswith(")"))]
                                if not path_segments:
                                    page_route = "/"
                                else:
                                    page_route = "/" + "/".join(path_segments)
                            if page_route not in self.profile["pages"]:
                                self.profile["pages"].append(page_route)
        except OSError:
            pass

        try:
            # Next.js Pages Router pages
            pages_dir = os.path.join(self.target_dir, "pages")
            if not os.path.exists(pages_dir):
                pages_dir = os.path.join(self.target_dir, "src", "pages")

            if os.path.exists(pages_dir):
                for root, dirs, files in os.walk(pages_dir):
                    rel = os.path.relpath(root, pages_dir)
                    norm_rel = rel.replace("\\", "/")
                    rel_parts = norm_rel.split("/")
                    if "api" in rel_parts or any(p.startswith("_") for p in rel_parts):
                        continue
                    for f in files:
                        if f.endswith((".tsx", ".jsx", ".ts", ".js")) and not f.startswith("_") and not any(ext in f for ext in (".test.", ".spec.", ".d.ts")):
                            filename_no_ext = os.path.splitext(f)[0]
                            if filename_no_ext == "index":
                                if rel == ".":
                                    page_route = "/"
                                else:
                                    page_route = "/" + norm_rel
                            else:
                                if rel == ".":
                                    page_route = "/" + filename_no_ext
                                else:
                                    page_route = "/" + norm_rel + "/" + filename_no_ext
                            if page_route not in self.profile["pages"]:
                                self.profile["pages"].append(page_route)
        except OSError:
            pass

    # =========================================================================
    # README
    # =========================================================================
    def _scan_readme(self):
        """Read README to get project description."""
        readme_path = None
        for name in ["README.md", "readme.md", "Readme.md", "README.markdown", "README.txt"]:
            p = os.path.join(self.target_dir, name)
            try:
                if os.path.exists(p):
                    readme_path = p
                    break
            except OSError:
                continue

        if not readme_path:
            return

        try:
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()
        except (UnicodeDecodeError, OSError):
            return

        # Get content after first heading (usually the description)
        lines = content.split("\n")
        desc_lines = []
        found_heading = False
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("#") and not found_heading:
                found_heading = True
                continue
            if found_heading:
                if stripped.startswith("#"):
                    break
                if not stripped.startswith("[") and not stripped.startswith("!") and not stripped.startswith("```"):
                    desc_lines.append(stripped)
                if len(desc_lines) >= 3:
                    break

        if not desc_lines:
            for line in lines:
                stripped = line.strip()
                if not stripped or stripped.startswith("#") or stripped.startswith("[") or stripped.startswith("!") or stripped.startswith("```"):
                    continue
                desc_lines.append(stripped)
                if len(desc_lines) >= 3:
                    break

        if desc_lines and not self.profile["project_description"]:
            self.profile["project_description"] = " ".join(desc_lines)

    # =========================================================================
    # SOURCE STRUCTURE
    # =========================================================================
    def _scan_source_structure(self):
        """Scan folder structure at level 1-2 to understand the architecture."""
        ignore_dirs = {
            "node_modules", ".git", ".next", ".agent", "__pycache__",
            "dist", "build", ".cache", ".turbo", "coverage",
            "test-output", "test-output-deep", "test-output-infra",
        }

        try:
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
                try:
                    if os.path.isdir(full_path):
                        # Count children
                        try:
                            children = [c for c in os.listdir(full_path) if not c.startswith(".") and c not in ignore_dirs]
                            self.profile["source_structure"].append(f"📁 {item}/ ({len(children)} items)")
                        except OSError:
                            self.profile["source_structure"].append(f"📁 {item}/")
                    else:
                        self.profile["source_structure"].append(f"📄 {item}")
                except OSError:
                    continue
        except OSError:
            pass

    # =========================================================================
    # FRAMEWORK DETECTION
    # =========================================================================
    def _detect_framework(self):
        """Detect core framework from tech stack."""
        ts = self.profile["tech_stack"]
        if "Next.js" in ts:
            self.profile["framework"] = "Next.js"
        elif "NestJS" in ts:
            self.profile["framework"] = "NestJS"
        elif "Django" in ts:
            self.profile["framework"] = "Django"
        elif "FastAPI" in ts:
            self.profile["framework"] = "FastAPI"
        elif "Flask" in ts:
            self.profile["framework"] = "Flask"
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
        """Generate scan report in text format."""
        p = self.profile
        lines = []
        lines.append("📊 PROJECT SCAN REPORT")
        lines.append("─" * 50)

        if p["project_name"]:
            lines.append(f"  📛 Name:        {p['project_name']}")
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
                lines.append(f"     └─ ...and {len(p['api']['routes']) - 8} other routes")

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
        """Generate infrastructure.md content from real data."""
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
                sections.append("- **Production**: [Missing — need to create `docker-compose.prod.yml`]")

            if p["docker"]["services"]:
                sections.append(f"\n### Services ({len(p['docker']['services'])})")
                for svc in p["docker"]["services"]:
                    sections.append(f"- `{svc}`")

            if p["docker"]["ports"]:
                sections.append(f"\n### Port Mapping")
                for port in p["docker"]["ports"]:
                    sections.append(f"- {port}")
        else:
            sections.append("- **Docker**: Not configured — need to set up Docker environment")
            sections.append("- **Ports**: Flexibly configure ports via environment variables (.env)")

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
        """Generate data_schema.md content from real Prisma schema."""
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
            sections.append("No Database schema detected.")
            sections.append("Once Prisma/SQL is added, run `bro-skills init` to update.\n")

        return "\n".join(sections)

    def generate_api_standards_content(self):
        """Generate api_standards.md content from real API routes."""
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
        """Generate business_logic.md content from source structure."""
        p = self.profile
        sections = []
        sections.append("# 💼 Business Logic\n")
        sections.append(f"> Auto-generated by bro-skills Scanner\n")

        if p["project_description"]:
            sections.append(f"## Project Description")
            sections.append(p["project_description"])
            sections.append("")

        if p["source_structure"]:
            sections.append("## Source Structure")
            for item in p["source_structure"]:
                sections.append(f"  {item}")
            sections.append("")

        if p["pages"]:
            sections.append(f"## Public Pages ({len(p['pages'])})")
            for pg in p["pages"]:
                sections.append(f"- `{pg}`")
            sections.append("")

        sections.append("## Core Business Rules")
        sections.append("<!-- Fill in the core business logic of the project here -->")
        sections.append("<!-- E.g., Ordering process, payment processing, inventory management... -->")

        return "\n".join(sections)

    def generate_identity_context(self):
        """Generate additional identity context based on scan."""
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
