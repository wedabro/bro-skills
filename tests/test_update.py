import hashlib
from types import SimpleNamespace

import pytest

from bro_skills import cli


def test_verify_sha256_accepts_matching_download(tmp_path):
    download = tmp_path / "bro-skills"
    download.write_bytes(b"standalone-binary")
    checksum = tmp_path / "bro-skills.sha256"
    expected = hashlib.sha256(download.read_bytes()).hexdigest()
    checksum.write_text(f"{expected}  bro-skills\n", encoding="utf-8")

    cli._verify_sha256(download, checksum)


def test_verify_sha256_rejects_tampered_download(tmp_path):
    download = tmp_path / "bro-skills"
    download.write_bytes(b"tampered")
    checksum = tmp_path / "bro-skills.sha256"
    checksum.write_text(f"{'0' * 64}  bro-skills\n", encoding="utf-8")

    with pytest.raises(RuntimeError, match="SHA-256 verification failed"):
        cli._verify_sha256(download, checksum)


@pytest.mark.parametrize(
    ("platform_name", "expected"),
    [
        ("win32", "bro-skills-windows-x86_64.exe"),
        ("linux", "bro-skills-linux-x86_64"),
    ],
)
def test_standalone_asset_name(monkeypatch, platform_name, expected):
    monkeypatch.setattr(cli.sys, "platform", platform_name)
    monkeypatch.setattr("platform.machine", lambda: "x86_64")

    assert cli._standalone_asset_name() == expected


def test_update_dispatches_frozen_install_to_standalone_updater(monkeypatch):
    called = []
    monkeypatch.setattr(cli.sys, "frozen", True, raising=False)
    monkeypatch.setattr(cli, "_get_latest_github_version", lambda: "99.0.0")
    monkeypatch.setattr(cli, "_update_standalone", called.append)

    cli.cmd_update(SimpleNamespace())

    assert called == ["99.0.0"]


def test_linux_standalone_update_verifies_and_replaces_executable(monkeypatch, tmp_path):
    target = tmp_path / "bro-skills"
    target.write_bytes(b"old-binary")
    new_binary = b"new-standalone-binary"
    expected = hashlib.sha256(new_binary).hexdigest()

    def fake_download(url, destination):
        if url.endswith(".sha256"):
            destination.write_text(f"{expected}  bro-skills-linux-x86_64\n", encoding="utf-8")
        else:
            destination.write_bytes(new_binary)

    monkeypatch.setattr(cli.sys, "platform", "linux")
    monkeypatch.setattr(cli.sys, "executable", str(target))
    monkeypatch.setattr(cli, "_standalone_asset_name", lambda: "bro-skills-linux-x86_64")
    monkeypatch.setattr(cli, "_download_file", fake_download)

    cli._update_standalone("99.0.0")

    assert target.read_bytes() == new_binary


def test_update_keeps_pip_path_for_non_frozen_install(monkeypatch):
    commands = []
    monkeypatch.delattr(cli.sys, "frozen", raising=False)
    monkeypatch.setattr(cli, "_get_latest_github_version", lambda: "99.0.0")
    monkeypatch.setattr("subprocess.run", lambda command, **kwargs: commands.append(command) or SimpleNamespace(returncode=0))

    cli.cmd_update(SimpleNamespace())

    assert commands == [[cli.sys.executable, "-m", "pip", "install", "--upgrade", "git+https://github.com/wedabro/bro-skills.git"]]
