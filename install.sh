#!/usr/bin/env sh
# bro-skills installer for Linux/macOS
# Usage: curl -fsSL https://raw.githubusercontent.com/wedabro/bro-skills/main/install.sh | bash

set -eu

repo="wedabro/bro-skills"
install_dir="${BRO_SKILLS_INSTALL_DIR:-${HOME}/.local/bin}"
destination="${install_dir}/bro-skills"
src_dir="${HOME}/.local/share/bro-skills"
temp_dir="$(mktemp -d)"

cleanup() {
    rm -rf -- "$temp_dir"
}
trap cleanup EXIT HUP INT TERM

mkdir -p "$install_dir"

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

# Find Python 3 binary
PY_BIN=""
if command -v python3 >/dev/null 2>&1; then
    PY_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PY_BIN="python"
fi

# 1. Try Python + Pip first
if [ -n "$PY_BIN" ]; then
    if "$PY_BIN" -m pip --version >/dev/null 2>&1; then
        echo "⚡ Installing latest bro-skills via $PY_BIN pip..."
        ts="$(date +%s)"
        if command -v git >/dev/null 2>&1; then
            if "$PY_BIN" -m pip install --no-cache-dir --force-reinstall --upgrade "git+https://github.com/${repo}.git@main"; then
                echo "✅ bro-skills installed successfully!"
                bro-skills version || true
                exit 0
            fi
        fi

        if "$PY_BIN" -m pip install --no-cache-dir --force-reinstall --upgrade "https://github.com/${repo}/archive/refs/heads/main.zip?t=${ts}"; then
            echo "✅ bro-skills installed successfully!"
            bro-skills version || true
            exit 0
        fi
    fi

    # 2. Python is installed without pip: Download source zip & create standalone Python wrapper
    echo "⚡ Installing latest bro-skills via $PY_BIN source runner..."
    ts="$(date +%s)"
    zip_path="${temp_dir}/main.zip"
    download "https://github.com/${repo}/archive/refs/heads/main.zip?t=${ts}" "$zip_path"
    
    mkdir -p "$src_dir"
    if command -v unzip >/dev/null 2>&1; then
        unzip -q -o "$zip_path" -d "$temp_dir"
        rm -rf "$src_dir"
        mkdir -p "$src_dir"
        cp -r "${temp_dir}/bro-skills-main/"* "$src_dir/"
    elif "$PY_BIN" -c "import zipfile" >/dev/null 2>&1; then
        "$PY_BIN" -c "import zipfile, shutil; zipfile.ZipFile('$zip_path').extractall('$temp_dir')"
        rm -rf "$src_dir"
        mkdir -p "$src_dir"
        cp -r "${temp_dir}/bro-skills-main/"* "$src_dir/"
    fi

    if [ -f "${src_dir}/ssd.py" ]; then
        cat << wrapper > "$destination"
#!/usr/bin/env sh
exec "$PY_BIN" "${src_dir}/ssd.py" "\$@"
wrapper
        chmod +x "$destination"
        echo "✅ bro-skills installed successfully at $destination!"
        "$destination" version || true
        exit 0
    fi
fi

# 3. Fallback: Standalone binary download from GitHub Releases
echo "Installing bro-skills standalone binary from GitHub Releases..."
asset="bro-skills-linux-x86_64"
base_url="https://github.com/${repo}/releases/latest/download"

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

chmod 755 "${temp_dir}/${asset}"
mv "${temp_dir}/${asset}" "$destination"

echo "bro-skills standalone binary installed successfully at $destination"
"$destination" version || true


