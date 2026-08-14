# 🧠 Project Lessons Learned & Self-Correction Log

This file tracks root causes, symptoms, and prevention rules learned from past bugs, edge cases, and user corrections. 
All AI Agents working on this project **MUST** consult this log before starting new tasks and update it whenever a new lesson is learned.

---

## 📌 Rule: Continuous Learning Directive
1. **Self-Correction**: Whenever a bug, workflow error, edge case, or user correction occurs, document the lesson below.
2. **Anti-Regression**: Before executing changes, check this log to ensure past errors are not repeated.

---

## 📓 Log of Lessons Learned

### [LESSON-001] Windows NTFS Junction Symlinks in Docker Volume Mounts
- **Date**: 2026-08-13
- **Category**: DevOps / Docker / Windows Compatibility
- **Symptom**: `mkdir /app/.agents/skills` inside Docker container returned `ENOTDIR`.
- **Root Cause**: `f:\wedabro\bro-skills\.agents\skills` is a Windows NTFS Junction pointing to `F:\wedabro\bro-skills\.agent\skills`. Inside a Linux Docker container mounted via `-v "f:\wedabro\bro-skills:/app"`, Linux sees the Junction as a broken reparse point.
- **Prevention Rule**: Do not rely on Windows NTFS Junction links inside Linux Docker containers. Either operate directly on the real target directory (`.agent/skills`) or replace broken Junction links with native Linux symlinks inside the container.

---

### [LESSON-002] GitHub Releases API vs Git Tags Version Check Mismatch
- **Date**: 2026-08-13
- **Category**: CLI / API / Version Management
- **Symptom**: Running `bro-skills update` printed `New version available: v1.8.0 ➔ v1.7.6` (false downgrade message).
- **Root Cause**: 
  1. `git push origin v1.8.0` creates a Git Tag on GitHub, but `/repos/{owner}/{repo}/releases/latest` API only returns official Releases manually drafted on GitHub.
  2. The update CLI stopped at `/releases/latest` (returning `1.7.6`) without checking Git Tags or raw `package.json` on `main`.
  3. Version check logic evaluated `if current_version != latest_version` instead of `if latest_version > current_version`.
- **Prevention Rule**: 
  - Always aggregate version candidates from Releases API, Tags API, and raw `package.json` on `main`.
  - Always parse semver tuples and compare `latest_version > current_version` to prevent reporting false downgrades.

---

### [LESSON-003] Mandatory Automatic Trigger of `/00-speckit.all` Workflow
- **Date**: 2026-08-13
- **Category**: Agent Protocol / SDLC Workflow
- **Symptom**: Agent waited for user to remind it to trigger `/00-speckit.all` instead of invoking it automatically.
- **Root Cause**: Rule in `AGENTS.md` and `constitution.md` did not explicitly mandate automatic execution on the very first response turn without prompt reminders.
- **Prevention Rule**: When a user requests any feature or implementation, the Agent MUST automatically trigger `/.agent/workflows/00-speckit.all.md` (`/00-speckit.all`) immediately on turn 1 without waiting for user prompt reminders.

---

### [LESSON-004] Pre-Flight Test Suite Execution Before Release
- **Date**: 2026-08-13
- **Category**: Release Engineering / Automation
- **Symptom**: Manual version bumping across 4 files could accidentally publish broken code if tests weren't run beforehand.
- **Root Cause**: Release script only updated version strings without forcing pre-flight unit test execution.
- **Prevention Rule**: Always integrate automated pytest suite runner (`docker compose run --rm test`) directly into `.agent/scripts/bump_version.py` so releases are automatically aborted if unit tests fail.

---

### [LESSON-005] Version Bumping & Release Tagging Strict Policy
- **Date**: 2026-08-13
- **Category**: Governance / Version Control
- **Symptom**: Agent automatically bumped version or asked to bump version after completing atomic features.
- **Root Cause**: Lack of explicit rule prohibiting automatic version bumps after completing routine tasks.
- **Prevention Rule**: The Agent MUST NEVER automatically bump version numbers or create/push release tags (`vX.Y.Z`) on its own. Version bumping and release tagging MUST ONLY be performed when the User explicitly requests/commands to raise the version!

---

### [LESSON-006] Anti-Caching In Pip, NPM & GitHub CDN During Updates
- **Date**: 2026-08-13
- **Category**: CLI / Update Pipeline / Caching
- **Symptom**: Running CLI update commands did not update `bro-skills` to the latest version on user's machine.
- **Root Cause**: 
  1. `pip install --upgrade git+...` re-used cached wheels from `pip` cache (`~/.cache/pip`).
  2. `raw.githubusercontent.com` served cached `package.json` for up to 5 minutes via Fastly CDN.
- **Prevention Rule**: 
  - Always pass `--no-cache-dir --force-reinstall --no-deps` to `pip` update commands.
  - Always append `?t=<timestamp>` query parameters and `Cache-Control: no-cache` headers to raw GitHub URL requests.

---

### [LESSON-007] Installer Scripts Must Prefer Python/Pip To Guarantee Latest Version
- **Date**: 2026-08-13
- **Category**: Installer / Release Distribution
- **Symptom**: Running `curl ... | bash` (`install.sh`) or `irm ... | iex` (`install.ps1`) downloaded v1.7.6 binary instead of v1.8.2.
- **Root Cause**: `install.sh` and `install.ps1` downloaded standalone compiled PyInstaller binaries from `releases/latest/download`, which pointed to old GitHub Releases assets rather than the latest git commit on `main`.
- **Prevention Rule**: Installer scripts MUST check for `python3`/`pip` first and install the latest `main` code directly via `pip install --no-cache-dir --upgrade git+https://github.com/wedabro/bro-skills.git@main`, falling back to standalone binaries only if Python is absent.

---

### [LESSON-008] Python Stdlib Zip Extractor For Zero-Dependency Installations
- **Date**: 2026-08-13
- **Category**: Installer / Cross-Platform Compatibility
- **Symptom**: `install.sh` failed on Linux servers where `python3-pip` and `unzip` were not installed, jumping to old standalone binary download.
- **Root Cause**: Relying on external shell tools (`pip`, `unzip`, `cp -r`) inside `install.sh` caused silent shell aborts on minimal Linux distros (Ubuntu/Debian server).
- **Prevention Rule**: Use Python stdlib (`urllib.request`, `zipfile`, `io`, `os`, `shutil`) to download and extract `main.zip` directly in Python, requiring zero external packages or tools.

---

### [LESSON-009] ANSI Escape Sequence & Terminal Arrow Key Parsing Fix
- **Date**: 2026-08-13
- **Category**: CLI / Interactive Prompt / Key Handling
- **Symptom**: Pressing Down Arrow in `bro-skills init` multiselect menu automatically triggered `❌ Canceled / Đã hủy`.
- **Root Cause**: Windows Terminal & VT100 / ANSI terminals send escape sequence `\x1b[B` or `\x1bOB`. In `select_menu()`, reading `\x1b` immediately returned `"cancel"` because it did not check `msvcrt.kbhit()` or SS3 application mode (`\x1bOB`) / VT100 (`\x1b[B`).
- **Prevention Rule**: Key reading loops MUST check if `\x1b` is followed by `[B`, `[A`, `OB`, `OA` arrow sequences before assuming the standalone ESC key was pressed, and use extended timeouts (>200ms) for POSIX select.

---

### [LESSON-010] GitHub Release Object Creation vs Git Tag Pushing
- **Date**: 2026-08-13
- **Category**: Release Engineering / GitHub Releases
- **Symptom**: GitHub Releases page (`https://github.com/wedabro/bro-skills/releases`) was stuck showing `v1.7.6` as the Latest Release despite tags `v1.8.0`..`v1.8.3` being pushed.
- **Root Cause**: `git push origin vX.Y.Z` creates a Git Tag on GitHub, but does not publish a GitHub Release UI object. The GitHub Releases page & API `/releases/latest` only update when `gh release create vX.Y.Z` or Web UI Release form is published.
- **Prevention Rule**: Release scripts MUST run `gh release create vX.Y.Z --title "vX.Y.Z" --generate-notes` or generate a 1-click web release creation URL (`https://github.com/owner/repo/releases/new?tag=vX.Y.Z&title=vX.Y.Z`) so the official GitHub Releases page stays synced with Git tags.

---

### [LESSON-011] GitHub Actions CI Dependencies & Test Command Invocation
- **Date**: 2026-08-13
- **Category**: CI/CD / GitHub Actions
- **Symptom**: GitHub Actions CI test matrix failed across Python 3.9 - 3.13.
- **Root Cause**:
  1. Python 3.12+ GitHub Actions runners lack pre-installed `setuptools` and `wheel`, causing `pip install -e .` build failures.
  2. Running `pytest -q` directly failed when the `bro-skills` binary PATH was not exported or when `pytest` was invoked as a bare CLI tool.
- **Prevention Rule**: In GitHub Actions workflow files, always run `python -m pip install --upgrade pip setuptools wheel`, `python -m pip install -e ".[test]"`, and invoke test suites via `python -m pytest -q`.

---

### [LESSON-012] Hybrid Numeric & Keypress Menu Navigation For Laggy SSH VPS Connections
- **Date**: 2026-08-13
- **Category**: CLI / UX / Interactive Menu
- **Symptom**: User requested numeric shortcuts on SSH VPS because arrow keys were unreliable over high-latency SSH connections.
- **Root Cause**: High SSH latency / packet fragmentation can delay arrow key ANSI escape sequences, making arrow-only menus frustrating.
- **Prevention Rule**: Display explicit index numbers `[1]`, `[2]`, `[3]` in interactive menus, allow typing digits `1`-`9` directly to toggle/select items, support Vim/WASD keys (`j`/`k`/`s`/`w`), and allow non-interactive CLI flags (`bro-skills init -a codex,cursor,antigravity`).

---

### [LESSON-013] Removal of Hardcoded Docker Port Ranges (8900-8999)
- **Date**: 2026-08-14
- **Category**: CLI / Port Allocation Policy
- **Symptom**: User requested deleting automatic Docker port scanning and fixed 8900-8999 range enforcement during `bro-skills init`.
- **Root Cause**: Hardcoding a fixed port range (8900-8999) or auto-assigning ports during init interfered with custom per-project port schemes managed by users.
- **Prevention Rule**: Do not auto-scan or auto-assign port ranges during project initialization. All application ports should be flexibly configured via `.env` per project without enforcing fixed port range constraints.

---

### [LESSON-014] TOML Parser Version Compatibility (Python 3.9/3.10 vs 3.11+)
- **Date**: 2026-08-14
- **Category**: Python Compatibility / Pytest CI
- **Symptom**: `test_scan_pyproject_authors_table_precedence` failed on Python 3.9 and 3.10 CI runners (`assert 'John Author' == 'real-project-name'`).
- **Root Cause**: `tomllib` standard library is only available in Python 3.11+. On Python 3.9 and 3.10, `import tomllib` threw `ModuleNotFoundError`, falling back to unanchored regex `name\s*=\s*...` which matched `name = "John Author"` inside `authors = [{ name = "John Author" }]` before the top-level `name = "real-project-name"`.
- **Prevention Rule**: When parsing TOML files, try `tomllib`, then fallback `tomli`/`toml` packages, then a section-aware line parser for `[project]` / `[tool.poetry]`, and use line-start anchored multiline regex (`^\s*name\s*=...`) as final fallback.










