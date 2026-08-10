#!/usr/bin/env sh
# bro-skills standalone installer for Linux x64
# Usage: curl -fsSL https://raw.githubusercontent.com/wedabro/bro-skills/main/install.sh | sh

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

echo "Installing bro-skills standalone..."
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
"$destination" version

case ":${PATH}:" in
    *":${install_dir}:"*) ;;
    *)
        echo "Add this line to your shell profile, then open a new terminal:"
        echo "  export PATH=\"${install_dir}:\$PATH\""
        ;;
esac
