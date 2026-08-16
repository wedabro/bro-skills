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


def _get_zalo_bot_chat_id_from_updates(token: str) -> str:
    """Try resolving chat_id from recent bot updates via Zalo Bot Platform getUpdates."""
    try:
        url = f"https://bot-api.zaloplatforms.com/bot{token}/getUpdates"
        req = urllib.request.Request(url, headers={"User-Agent": "wedabro-release-bot"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="ignore"))
            if data.get("ok") and data.get("result"):
                # Search for the latest message with a valid chat id
                for item in reversed(data["result"]):
                    msg = item.get("message") or item.get("channel_post") or {}
                    chat = msg.get("chat") or {}
                    if chat.get("id"):
                        return str(chat["id"])
    except Exception as e:
        print(f"ℹ️ Could not automatically fetch chat_id from getUpdates: {e}")
    return ""


def send_zalo_notification(version: str, status: str = "success") -> bool:
    zalo_webhook_url = os.environ.get("ZALO_WEBHOOK_URL", "").strip()
    zalo_token = os.environ.get("ZALO_BOT_TOKEN", "").strip()
    zalo_chat_id = (
        os.environ.get("ZALO_CHAT_ID", "").strip()
        or os.environ.get("ZALO_RECIPIENT_ID", "").strip()
    )

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

    # 1. Trường hợp dùng Zalo Bot Platform (Token có định dạng id:secret như 451078241683572072:...)
    if zalo_token and ":" in zalo_token:
        print("🤖 Detected Zalo Bot Platform format (id:secret)...")
        if not zalo_chat_id:
            zalo_chat_id = _get_zalo_bot_chat_id_from_updates(zalo_token)
            if zalo_chat_id:
                print(f"💡 Auto-detected Zalo chat_id from recent updates: {zalo_chat_id}")

        if not zalo_chat_id:
            print("⚠️ Zalo Bot Error: Missing ZALO_CHAT_ID. Please send a message to the bot on Zalo or set ZALO_CHAT_ID in GitHub Secrets.")
            return False

        try:
            bot_api_url = f"https://bot-api.zaloplatforms.com/bot{zalo_token}/sendMessage"
            payload = {
                "chat_id": zalo_chat_id,
                "text": message_text,
            }
            req = urllib.request.Request(
                bot_api_url,
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "wedabro-release-bot",
                },
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                res_body = resp.read().decode("utf-8", errors="ignore")
                print(f"✅ Zalo Bot Platform sendMessage response: {res_body}")
                return True
        except urllib.error.HTTPError as he:
            err_body = he.read().decode("utf-8", errors="ignore")
            print(f"❌ Zalo Bot Platform HTTP Error {he.code}: {err_body}")
            return False
        except Exception as e:
            print(f"❌ Failed to send Zalo Bot Platform message: {e}")
            return False

    # 2. Trường hợp dùng Zalo Webhook URL
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
                resp_text = resp.read().decode("utf-8", errors="ignore")
                print(f"✅ Zalo Webhook notification response (HTTP {resp.status}): {resp_text}")
        except urllib.error.HTTPError as he:
            err_body = he.read().decode("utf-8", errors="ignore")
            print(f"❌ Zalo Webhook HTTP Error {he.code}: {err_body}")
            success = False
        except Exception as e:
            print(f"❌ Failed to send Zalo Webhook notification: {e}")
            success = False

    # 3. Trường hợp dùng Zalo OA Access Token (Bearer)
    if zalo_token and ":" not in zalo_token:
        zalo_endpoint = os.environ.get("ZALO_API_ENDPOINT", "https://openapi.zalo.me/v3.0/oa/message/cs").strip()
        try:
            headers = {
                "Content-Type": "application/json",
                "access_token": zalo_token,
                "Authorization": f"Bearer {zalo_token}",
                "User-Agent": "wedabro-release-bot",
            }
            if zalo_chat_id:
                oa_payload = {
                    "recipient": {"user_id": zalo_chat_id},
                    "message": {"text": message_text},
                }
            else:
                oa_payload = {
                    "message": {"text": message_text},
                    "text": message_text,
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
                res_body = resp.read().decode("utf-8", errors="ignore")
                print(f"✅ Zalo OA API notification response: {res_body}")
        except urllib.error.HTTPError as he:
            err_body = he.read().decode("utf-8", errors="ignore")
            print(f"❌ Zalo OA API HTTP Error {he.code}: {err_body}")
            success = False
        except Exception as e:
            print(f"❌ Failed to send Zalo OA API notification: {e}")
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
