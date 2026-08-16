#!/usr/bin/env python3
"""
⚡ bro-skills Release Notification Script
Sends release announcements to Discord and Zalo bots when a new version tag is published.

Usage:
    python .agent/scripts/notify_release.py <version_tag> [status]
"""

import sys
import os
import json
import urllib.request
import urllib.error
from datetime import datetime


def send_discord_notification(version: str, status: str = "success") -> bool:
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL", "").strip()
    if not webhook_url:
        print("ℹ️ Discord notification skipped: DISCORD_WEBHOOK_URL not configured.")
        return False

    repo = os.environ.get("GITHUB_REPOSITORY", "wedabro/bro-skills")
    release_url = f"https://github.com/{repo}/releases/tag/{version}"
    color = 0x2ECC71 if status.lower() == "success" else 0xE74C3C  # Green or Red

    payload = {
        "username": "wedabro Release Bot",
        "avatar_url": "https://github.com/wedabro.png",
        "embeds": [
            {
                "title": f"🚀 New Release Published: {version}",
                "url": release_url,
                "description": f"A new version of **{repo}** has been released to GitHub!",
                "color": color,
                "fields": [
                    {"name": "📦 Project", "value": f"`{repo}`", "inline": True},
                    {"name": "🏷️ Version", "value": f"`{version}`", "inline": True},
                    {"name": "⚙️ Status", "value": f"**{status.upper()}**", "inline": True},
                    {
                        "name": "🔗 Links",
                        "value": f"[View GitHub Release]({release_url}) • [Repository](https://github.com/{repo})",
                        "inline": False,
                    },
                ],
                "footer": {"text": "wedabro CI/CD Release Pipeline"},
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        ],
    }

    try:
        req = urllib.request.Request(
            webhook_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "User-Agent": "wedabro-release-bot",
            },
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status in (200, 204):
                print(f"✅ Discord notification sent successfully for {version}!")
                return True
            else:
                print(f"⚠️ Discord responded with HTTP status {resp.status}")
                return False
    except Exception as e:
        print(f"❌ Failed to send Discord notification: {e}")
        return False


def send_zalo_notification(version: str, status: str = "success") -> bool:
    zalo_webhook_url = os.environ.get("ZALO_WEBHOOK_URL", "").strip()
    zalo_token = os.environ.get("ZALO_BOT_TOKEN", "").strip()
    zalo_recipient_id = os.environ.get("ZALO_RECIPIENT_ID", "").strip() or os.environ.get("ZALO_CHAT_ID", "").strip()
    zalo_endpoint = os.environ.get("ZALO_API_ENDPOINT", "https://openapi.zalo.me/v3.0/oa/message/cs").strip()

    if not zalo_webhook_url and not zalo_token:
        print("ℹ️ Zalo notification skipped: Neither ZALO_WEBHOOK_URL nor ZALO_BOT_TOKEN is configured.")
        return False

    repo = os.environ.get("GITHUB_REPOSITORY", "wedabro/bro-skills")
    release_url = f"https://github.com/{repo}/releases/tag/{version}"
    current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    message_text = (
        f"🚀 [wedabro / {repo}] PHÁT HÀNH PHIÊN BẢN MỚI!\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🏷️ Phiên bản: {version}\n"
        f"📦 Dự án: {repo}\n"
        f"⚙️ Trạng thái: {status.upper()}\n"
        f"⏰ Thời gian: {current_time}\n"
        f"🔗 Chi tiết Release: {release_url}\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )

    success = True

    # 1. Trường hợp dùng Zalo Webhook URL
    if zalo_webhook_url:
        try:
            webhook_payload = {
                "text": message_text,
                "version": version,
                "project": repo,
                "release_url": release_url,
            }
            req = urllib.request.Request(
                zalo_webhook_url,
                data=json.dumps(webhook_payload).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "wedabro-release-bot",
                },
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                print(f"✅ Zalo Webhook notification sent successfully (HTTP {resp.status})!")
        except Exception as e:
            print(f"❌ Failed to send Zalo Webhook notification: {e}")
            success = False

    # 2. Trường hợp dùng Zalo Bot Token / OA API
    if zalo_token:
        try:
            headers = {
                "Content-Type": "application/json",
                "access_token": zalo_token,
                "User-Agent": "wedabro-release-bot",
            }
            # Nếu có cấu hình Recipient ID (Zalo User/Group ID) theo format OpenAPI Zalo
            if zalo_recipient_id:
                oa_payload = {
                    "recipient": {"user_id": zalo_recipient_id},
                    "message": {"text": message_text},
                }
            else:
                oa_payload = {
                    "message": {"text": message_text},
                    "version": version,
                    "project": repo,
                    "release_url": release_url,
                }

            req = urllib.request.Request(
                zalo_endpoint,
                data=json.dumps(oa_payload).encode("utf-8"),
                headers=headers,
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                res_body = resp.read().decode("utf-8")
                print(f"✅ Zalo Bot API notification response: {res_body}")
        except Exception as e:
            print(f"❌ Failed to send Zalo Bot Token notification: {e}")
            success = False

    return success


def main():
    version = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GITHUB_REF_NAME", "vUnknown")
    status = sys.argv[2] if len(sys.argv) > 2 else "success"

    print(f"📢 Triggering release notifications for version: {version} (Status: {status})")

    discord_ok = send_discord_notification(version, status)
    zalo_ok = send_zalo_notification(version, status)

    print(f"🏁 Notifications completed. (Discord: {discord_ok}, Zalo: {zalo_ok})")


if __name__ == "__main__":
    main()
