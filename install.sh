#!/usr/bin/env bash
# bro-skills Installer for Linux / macOS / WSL / Git Bash
# Usage: curl -fsSL https://raw.githubusercontent.com/wedabro/bro-skills/main/install.sh | bash

set -e

echo "⚡ Installing bro-skills..."

# 1. Detect Python 3
if command -v python3 &>/dev/null; then
    PYTHON_BIN="python3"
elif command -v python &>/dev/null; then
    PYTHON_BIN="python"
else
    echo "❌ Python 3 is required but not found in PATH."
    echo "Please install Python 3.9+ first: https://www.python.org/downloads/"
    exit 1
fi

# 2. Check Python Version (>= 3.9)
$PYTHON_BIN -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)" || {
    echo "❌ Python 3.9 or higher is required."
    exit 1
}

echo "✔ Found $($PYTHON_BIN --version)"

# 3. Installation Strategy
if command -v pipx &>/dev/null; then
    echo "📦 Installing via pipx..."
    pipx install --force git+https://github.com/wedabro/bro-skills.git
elif command -v uv &>/dev/null; then
    echo "📦 Installing via uv..."
    uv tool install --force git+https://github.com/wedabro/bro-skills.git
else
    echo "📦 Installing via pip..."
    $PYTHON_BIN -m pip install --upgrade git+https://github.com/wedabro/bro-skills.git
fi

# 4. Verify Installation
if command -v bro-skills &>/dev/null; then
    echo ""
    echo "🎉 bro-skills installed successfully!"
    bro-skills version
else
    echo ""
    echo "⚠️ bro-skills was installed, but 'bro-skills' command is not in your current PATH."
    echo "Please ensure Python user bin directory (e.g., ~/.local/bin) is added to your PATH environment variable."
fi
