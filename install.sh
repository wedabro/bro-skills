#!/usr/bin/env sh
# bro-skills installer for Linux/macOS
# Usage: curl -fsSL https://raw.githubusercontent.com/wedabro/bro-skills/main/install.sh | bash

set -e

repo="wedabro/bro-skills"
install_dir="${BRO_SKILLS_INSTALL_DIR:-${HOME}/.local/bin}"
destination="${install_dir}/bro-skills"
src_dir="${HOME}/.local/share/bro-skills"

mkdir -p "$install_dir"
mkdir -p "$src_dir"

PY_BIN=""
if command -v python3 >/dev/null 2>&1; then
    PY_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PY_BIN="python"
fi

if [ -z "$PY_BIN" ]; then
    echo "❌ Error: Python 3 is required to install bro-skills. Please install python3 (e.g. sudo apt install python3) and run again." >&2
    exit 1
fi

echo "⚡ Installing latest bro-skills from GitHub main branch..."

# 1. Try pip install first if pip is available
if "$PY_BIN" -m pip --version >/dev/null 2>&1; then
    if "$PY_BIN" -m pip install --no-cache-dir --force-reinstall --upgrade "git+https://github.com/${repo}.git@main"; then
        echo "✅ bro-skills installed successfully via pip!"
        "$PY_BIN" -m bro_skills version || true
        exit 0
    fi
fi

# 2. Fallback: Download & extract source zip using Python stdlib (no pip, no unzip, no git required!)
"$PY_BIN" -c "
import urllib.request, zipfile, io, os, shutil, sys, time

ts = int(time.time())
url = f'https://github.com/${repo}/archive/refs/heads/main.zip?t={ts}'
headers = {'User-Agent': 'bro-skills-installer', 'Cache-Control': 'no-cache, no-store'}

print('Downloading latest source archive...')
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    data = resp.read()

tmp_extract = os.path.expanduser('~/.local/share/bro-skills-tmp')
if os.path.exists(tmp_extract):
    shutil.rmtree(tmp_extract)

print('Extracting package contents...')
with zipfile.ZipFile(io.BytesIO(data)) as zf:
    zf.extractall(tmp_extract)

src_folder = os.path.join(tmp_extract, 'bro-skills-main')
dest_folder = os.path.expanduser('~/.local/share/bro-skills')

if os.path.exists(dest_folder):
    shutil.rmtree(dest_folder)

shutil.copytree(src_folder, dest_folder)
shutil.rmtree(tmp_extract, ignore_errors=True)
print('Source files installed at:', dest_folder)
"

cat << wrapper > "$destination"
#!/usr/bin/env sh
exec "$PY_BIN" "$src_dir/ssd.py" "\$@"
wrapper

chmod +x "$destination"

echo "✅ bro-skills installed successfully at $destination!"
"$destination" version || true
