#!/usr/bin/env python3
"""
⚡ bro-skills Release Pipeline Script
Updates version numbers across project files, runs verification tests in Docker,
creates conventional commits & git tags, and pushes to origin.

Usage:
    python .agent/scripts/bump_version.py <new_version> [--push] [--skip-tests]

Examples:
    python .agent/scripts/bump_version.py 1.8.1
    python .agent/scripts/bump_version.py 1.8.1 --push
    python .agent/scripts/bump_version.py 1.8.1 --push --skip-tests
"""

import sys
import re
import os
import subprocess


def parse_version(v_str):
    """Parse version string into a comparable tuple of ints."""
    if not v_str:
        return (0, 0, 0)
    cleaned = v_str.lstrip("v").strip()
    parts = []
    for part in cleaned.split("."):
        digits = "".join(c for c in part if c.isdigit())
        parts.append(int(digits) if digits else 0)
    return tuple(parts)


def get_current_version():
    """Read current version from bro_skills/__init__.py."""
    init_path = os.path.join("bro_skills", "__init__.py")
    if os.path.exists(init_path):
        with open(init_path, "r", encoding="utf-8") as f:
            match = re.search(r'__version__\s*=\s*"([^"]+)"', f.read())
            if match:
                return match.group(1)
    return "0.0.0"


def run_tests():
    """Run pytest suite inside Docker container to ensure 100% test pass."""
    print("🧪 Running pre-release verification tests in Docker container...")
    try:
        res = subprocess.run(["docker", "compose", "run", "--rm", "test"], check=True, text=True)
        if res.returncode == 0:
            print("✅ All unit tests PASSED successfully!\n")
            return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"⚠️ Docker test runner error: {e}")
        print("   Attempting fallback to local pytest...")
        try:
            res = subprocess.run([sys.executable, "-m", "pytest", "-q"], check=True, text=True)
            if res.returncode == 0:
                print("✅ Local pytest suite PASSED successfully!\n")
                return True
        except Exception as local_err:
            print(f"❌ Test suite FAILED: {local_err}")
            return False
    return False


def get_recent_commits():
    """Get commit messages since the last git tag."""
    try:
        last_tag_proc = subprocess.run(["git", "describe", "--tags", "--abbrev=0"], capture_output=True, text=True)
        last_tag = last_tag_proc.stdout.strip() if last_tag_proc.returncode == 0 else ""
        revision_range = f"{last_tag}..HEAD" if last_tag else "HEAD~10..HEAD"
        log_proc = subprocess.run(["git", "log", revision_range, "--oneline"], capture_output=True, text=True)
        if log_proc.returncode == 0 and log_proc.stdout.strip():
            return log_proc.stdout.strip().split("\n")
    except Exception:
        pass
    return []


def bump_version(new_version, auto_push=False, skip_tests=False):
    current_ver = get_current_version()
    print(f"\n=======================================================")
    print(f"⚡ bro-skills Release Pipeline: v{current_ver} ➔ v{new_version}")
    print(f"=======================================================\n")

    # 1. Version validation
    if parse_version(new_version) <= parse_version(current_ver):
        print(f"⚠️ Warning: Target version v{new_version} is not greater than current version v{current_ver}.")

    # 2. Pre-release Test Suite
    if not skip_tests:
        if not run_tests():
            print("❌ ABORTING release pipeline due to test failures!")
            sys.exit(1)
    else:
        print("⏩ Skipping pre-release test suite (--skip-tests active).\n")

    # 3. Update version in files
    print("📝 Updating version strings in project configuration files:")
    
    # package.json
    pkg_path = "package.json"
    if os.path.exists(pkg_path):
        with open(pkg_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = re.sub(r'"version":\s*"[^"]+"', f'"version": "{new_version}"', content)
        with open(pkg_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("  ✓ package.json")

    # pyproject.toml
    pyproj_path = "pyproject.toml"
    if os.path.exists(pyproj_path):
        with open(pyproj_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = re.sub(r'version\s*=\s*"[^"]+"', f'version = "{new_version}"', content)
        with open(pyproj_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("  ✓ pyproject.toml")

    # bro_skills/__init__.py
    init_path = os.path.join("bro_skills", "__init__.py")
    if os.path.exists(init_path):
        with open(init_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = re.sub(r'__version__\s*=\s*"[^"]+"', f'__version__ = "{new_version}"', content)
        with open(init_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("  ✓ bro_skills/__init__.py")

    # bro_skills/generator.py
    gen_path = os.path.join("bro_skills", "generator.py")
    if os.path.exists(gen_path):
        with open(gen_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = re.sub(r'"bro_skills_version":\s*"[^"]+"', f'"bro_skills_version": "{new_version}"', content)
        with open(gen_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("  ✓ bro_skills/generator.py")

    print("\n🎉 All configuration files updated to version " + new_version)

    # 4. Show Recent Commits Summary
    commits = get_recent_commits()
    if commits:
        print("\n📜 Commits included in this release:")
        for c in commits[:8]:
            print(f"  • {c}")
        if len(commits) > 8:
            print(f"  ... and {len(commits) - 8} more commits")

    # 5. Git Commit, Tag & Push
    if auto_push:
        print("\n🚀 Executing Git Release Workflow (commit, tag, push)...")
        try:
            files_to_add = ["package.json", "pyproject.toml", "bro_skills/__init__.py", "bro_skills/generator.py"]
            subprocess.run(["git", "add"] + files_to_add, check=True)
            subprocess.run(["git", "commit", "-m", f"chore(release): bump version to {new_version}"], check=True)
            subprocess.run(["git", "tag", f"v{new_version}"], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            subprocess.run(["git", "push", "origin", f"v{new_version}"], check=True)

            # Try publishing official GitHub Release Object via gh CLI if present
            gh_published = False
            try:
                gh_proc = subprocess.run(
                    ["gh", "release", "create", f"v{new_version}", "--title", f"v{new_version}", "--generate-notes"],
                    capture_output=True, text=True
                )
                if gh_proc.returncode == 0:
                    gh_published = True
                    print(f"📦 Published official GitHub Release object: v{new_version}")
            except Exception:
                pass

            print(f"\n✨ RELEASE SUCCESSFUL: v{new_version} published to GitHub!")
            if gh_published:
                print(f"🔗 Release URL: https://github.com/wedabro/bro-skills/releases/tag/v{new_version}")
            else:
                print(f"🔗 Direct 1-Click Release Link: https://github.com/wedabro/bro-skills/releases/new?tag=v{new_version}&title=v{new_version}")
        except subprocess.CalledProcessError as err:
            print(f"❌ Git operation failed: {err}")
            sys.exit(1)
    else:
        print("\n💡 Manual Release Commands:")
        print("  git add package.json pyproject.toml bro_skills/__init__.py bro_skills/generator.py")
        print(f'  git commit -m "chore(release): bump version to {new_version}"')
        print(f"  git tag v{new_version}")
        print(f"  git push origin main")
        print(f"  git push origin v{new_version}")
        print(f"  gh release create v{new_version} --title \"v{new_version}\" --generate-notes")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Error: Missing required target version.")
        print("\nUsage:")
        print("  python .agent/scripts/bump_version.py <new_version> [--push] [--skip-tests]")
        sys.exit(1)

    version_arg = sys.argv[1]
    auto_push_flag = "--push" in sys.argv or "--git" in sys.argv
    skip_tests_flag = "--skip-tests" in sys.argv

    if not re.match(r'^\d+\.\d+\.\d+$', version_arg):
        print(f"❌ Error: Invalid semver format '{version_arg}'. Expected x.y.z (e.g. 1.8.1)")
        sys.exit(1)

    bump_version(version_arg, auto_push=auto_push_flag, skip_tests=skip_tests_flag)


