#!/usr/bin/env sh
# bro-skills installer for Linux/macOS
# Usage: curl -fsSL https://raw.githubusercontent.com/wedabro/bro-skills/main/install.sh | bash

set -eu

repo="wedabro/bro-skills"
asset="bro-skills-linux-x86_64"
install_dir="${BRO_SKILLS_INSTALL_DIR:-${HOME}/.local/bin}"
destination="${install_dir}/bro-skills"
base_url="https://github.com/${repo}/releases/latest/download"
temp_dir="$(mktemp -d)"

cleanup() {
    rm -rf -- "$temp_dir"
}
trap cleanup EXIT HUP INT TERM

# 1. Prefer Python / Pip installation if available to get the latest main release
PY_CMD=""
if command -v python3 >/dev/null 2>&1 && python3 -m pip --version >/dev/null 2>&1; then
    PY_CMD="python3"
elif command -v python >/dev/null 2>&1 && python -m pip --version >/dev/null 2>&1; then
    PY_CMD="python"
fi

if [ -n "$PY_CMD" ]; then
    echo "⚡ Installing latest bro-skills via Python ($PY_CMD)..."
    ts="$(date +%s)"
    if command -v git >/dev/null 2>&1; then
        if "$PY_CMD" -m pip install --no-cache-dir --force-reinstall --upgrade "git+https://github.com/${repo}.git@main"; then
            echo "✅ bro-skills installed successfully!"
            bro-skills version || true
            exit 0
        fi
    fi

    echo "🔄 Installing via GitHub archive..."
    if "$PY_CMD" -m pip install --no-cache-dir --force-reinstall --upgrade "https://github.com/${repo}/archive/refs/heads/main.zip?t=${ts}"; then
        echo "✅ bro-skills installed successfully!"
        bro-skills version || true
        exit 0
    fi
fi

# 2. Fallback to standalone binary download
if [ "$(uname -s)" != "Linux" ]; then
    echo "bro-skills standalone currently supports Linux and Windows only." >&2
    exit 1
fi

case "$(uname -m)" in
    x86_64|amd64) ;;
    *)
        echo "bro-skills currently provides a standalone Linux binary for x64 only (detected: $(uname -m))." >&2
        exit 1
        ;;
esac

download() {
    url="$1"
    output="$2"
    if command -v curl >/dev/null 2>&1; then
        curl -fsSL "$url" -o "$output"
    elif command -v wget >/dev/null 2>&1; then
        wget -qO "$output" "$url"
    else
        echo "curl or wget is required to download bro-skills." >&2
        exit 1
    fi
}

echo "Installing bro-skills standalone binary..."
download "${base_url}/${asset}" "${temp_dir}/${asset}"
download "${base_url}/${asset}.sha256" "${temp_dir}/${asset}.sha256"

expected="$(awk '{print $1}' "${temp_dir}/${asset}.sha256")"
if command -v sha256sum >/dev/null 2>&1; then
    actual="$(sha256sum "${temp_dir}/${asset}" | awk '{print $1}')"
elif command -v shasum >/dev/null 2>&1; then
    actual="$(shasum -a 256 "${temp_dir}/${asset}" | awk '{print $1}')"
else
    echo "sha256sum or shasum is required to verify the download." >&2
    exit 1
fi

if [ "$actual" != "$expected" ]; then
    echo "SHA-256 verification failed. Expected $expected but downloaded $actual." >&2
    exit 1
fi

mkdir -p "$install_dir"
chmod 755 "${temp_dir}/${asset}"
mv "${temp_dir}/${asset}" "$destination"

echo "bro-skills installed successfully at $destination"
if ! "$destination" version; then
    rm -f -- "$destination"
    echo "The downloaded bro-skills binary cannot run on this Linux system; installation was rolled back." >&2
    exit 1
fi

case ":${PATH}:" in
    *":${install_dir}:"*) ;;
    *)
        echo "Add this line to your shell profile, then open a new terminal:"
        echo "  export PATH=\"${install_dir}:\$PATH\""
        ;;
esac

