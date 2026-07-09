"""
yos-notify — Universal Notification Module for yOS
===================================================
Core module of the yOS ecosystem. Callable from:
  - CLI:    yos-notify "Title" "Message" [options]
  - Python: from yos_notify import notify

Channels:
  - Pushover (default): native iOS / macOS / Android push
  - Telegram (optional): cross-platform via Bot API

Device targeting (Pushover only):
  - all       : all registered devices (default)
  - ios       : iPhone / iPad
  - macos     : Mac
  - android   : Android
  - n100      : N100 / Ubuntu (requires Pushover Desktop app or ntfy fallback)

Usage examples:
  notify("Done", "DWPose completed")
  notify("Alert", "Disk full", channel="both", device="ios")
  notify("Info", "Pipeline started", channel="telegram")
"""

import os
import json
import argparse
import requests
from pathlib import Path
from datetime import datetime

# ─── Config ────────────────────────────────────────────────────────────────────
CONFIG_PATH = Path(os.environ.get("YOS_NOTIFY_CONFIG", Path.home() / ".yos" / "notify.json"))

DEFAULT_CONFIG = {
    "default_channel": "pushover",
    "pushover": {
        "app_token": os.environ.get("PUSHOVER_APP_TOKEN", ""),
        "user_key":  os.environ.get("PUSHOVER_USER_KEY", ""),
        "devices": {
            "all":     "",          # empty string = all devices in Pushover
            "ios":     "",          # device name as registered in Pushover app
            "macos":   "",          # device name as registered in Pushover app
            "android": "",          # device name as registered in Pushover app
            "n100":    "",          # device name as registered in Pushover app
        }
    },
    "telegram": {
        "bot_token": os.environ.get("TELEGRAM_BOT_TOKEN", ""),
        "chat_id":   os.environ.get("TELEGRAM_CHAT_ID", ""),
    }
}

# ─── Config loader ─────────────────────────────────────────────────────────────
def load_config() -> dict:
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            stored = json.load(f)
        # Merge with defaults (env vars override stored values if set)
        cfg = DEFAULT_CONFIG.copy()
        cfg["pushover"].update(stored.get("pushover", {}))
        cfg["telegram"].update(stored.get("telegram", {}))
        cfg["default_channel"] = stored.get("default_channel", cfg["default_channel"])
        # Env vars always win
        if os.environ.get("PUSHOVER_APP_TOKEN"):
            cfg["pushover"]["app_token"] = os.environ["PUSHOVER_APP_TOKEN"]
        if os.environ.get("PUSHOVER_USER_KEY"):
            cfg["pushover"]["user_key"] = os.environ["PUSHOVER_USER_KEY"]
        if os.environ.get("TELEGRAM_BOT_TOKEN"):
            cfg["telegram"]["bot_token"] = os.environ["TELEGRAM_BOT_TOKEN"]
        if os.environ.get("TELEGRAM_CHAT_ID"):
            cfg["telegram"]["chat_id"] = os.environ["TELEGRAM_CHAT_ID"]
        return cfg
    return DEFAULT_CONFIG.copy()


def save_config(cfg: dict):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    # Never save tokens to file if they came from env vars — store placeholders
    safe = {
        "default_channel": cfg["default_channel"],
        "pushover": {
            "app_token": cfg["pushover"]["app_token"],
            "user_key":  cfg["pushover"]["user_key"],
            "devices":   cfg["pushover"]["devices"],
        },
        "telegram": {
            "bot_token": cfg["telegram"]["bot_token"],
            "chat_id":   cfg["telegram"]["chat_id"],
        }
    }
    with open(CONFIG_PATH, "w") as f:
        json.dump(safe, f, indent=2)
    print(f"Config saved to {CONFIG_PATH}")


# ─── Pushover channel ──────────────────────────────────────────────────────────
def send_pushover(title: str, message: str, device: str = "all",
                  priority: int = 0, sound: str = None) -> dict:
    """
    Send via Pushover.
    device: 'all' | 'ios' | 'macos' | 'android' | 'n100' | exact device name
    priority: -2 (silent) | -1 (quiet) | 0 (normal) | 1 (high) | 2 (emergency)
    """
    cfg = load_config()
    po = cfg["pushover"]

    if not po["app_token"] or not po["user_key"]:
        return {"ok": False, "error": "Pushover not configured. Run: yos-notify --setup"}

    # Resolve device name
    device_name = po["devices"].get(device, device)  # fallback to literal string

    payload = {
        "token":   po["app_token"],
        "user":    po["user_key"],
        "title":   title,
        "message": message,
        "priority": priority,
    }
    if device_name:  # empty string = all devices
        payload["device"] = device_name
    if sound:
        payload["sound"] = sound

    try:
        r = requests.post("https://api.pushover.net/1/messages.json",
                          data=payload, timeout=10)
        result = r.json()
        result["ok"] = result.get("status") == 1
        return result
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ─── Telegram channel ──────────────────────────────────────────────────────────
def send_telegram(title: str, message: str, parse_mode: str = "HTML") -> dict:
    """Send via Telegram Bot API."""
    cfg = load_config()
    tg = cfg["telegram"]

    if not tg["bot_token"] or not tg["chat_id"]:
        return {"ok": False, "error": "Telegram not configured. Run: yos-notify --setup"}

    text = f"<b>🔔 {title}</b>\n{message}" if parse_mode == "HTML" else f"*{title}*\n{message}"
    ts   = datetime.now().strftime("%H:%M:%S")
    text += f"\n<i>— yOS · {ts}</i>" if parse_mode == "HTML" else f"\n_— yOS · {ts}_"

    url = f"https://api.telegram.org/bot{tg['bot_token']}/sendMessage"
    try:
        r = requests.post(url, json={
            "chat_id":    tg["chat_id"],
            "text":       text,
            "parse_mode": parse_mode,
        }, timeout=10)
        result = r.json()
        result["ok"] = result.get("ok", False)
        return result
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ─── Unified notify() API ──────────────────────────────────────────────────────
def notify(title: str, message: str,
           channel: str = None,
           device:  str = "all",
           priority: int = 0,
           sound: str = None) -> dict:
    """
    Universal notification entry point.

    Args:
        title    : Notification title
        message  : Notification body
        channel  : 'pushover' | 'telegram' | 'both' | None (uses default from config)
        device   : 'all' | 'ios' | 'macos' | 'android' | 'n100' (Pushover only)
        priority : Pushover priority (-2 to 2)
        sound    : Pushover sound name (optional)

    Returns:
        dict with 'pushover' and/or 'telegram' result dicts
    """
    cfg = load_config()
    if channel is None:
        channel = cfg["default_channel"]

    results = {}

    if channel in ("pushover", "both"):
        results["pushover"] = send_pushover(title, message, device, priority, sound)

    if channel in ("telegram", "both"):
        results["telegram"] = send_telegram(title, message)

    # Log result
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ok = all(v.get("ok") for v in results.values())
    status = "✅" if ok else "❌"
    print(f"[yos-notify] {status} {ts} | channel={channel} device={device} | {title}")
    for ch, res in results.items():
        if not res.get("ok"):
            print(f"  [{ch}] ERROR: {res.get('error', res)}")

    return results


# ─── Setup wizard ──────────────────────────────────────────────────────────────
def setup_wizard():
    print("\n=== yOS-Notify Setup ===\n")
    cfg = load_config()

    print("--- Pushover ---")
    print("  Get your tokens at https://pushover.net")
    cfg["pushover"]["app_token"] = input(f"  App Token [{cfg['pushover']['app_token'] or 'not set'}]: ").strip() or cfg["pushover"]["app_token"]
    cfg["pushover"]["user_key"]  = input(f"  User Key  [{cfg['pushover']['user_key'] or 'not set'}]: ").strip() or cfg["pushover"]["user_key"]

    print("\n  Device names (leave blank = all devices):")
    for dev in ["ios", "macos", "android", "n100"]:
        current = cfg["pushover"]["devices"].get(dev, "")
        val = input(f"    {dev} device name [{current or 'all'}]: ").strip()
        cfg["pushover"]["devices"][dev] = val if val else current

    print("\n--- Telegram ---")
    print("  Bot token from @BotFather, Chat ID from @userinfobot")
    cfg["telegram"]["bot_token"] = input(f"  Bot Token [{cfg['telegram']['bot_token'] or 'not set'}]: ").strip() or cfg["telegram"]["bot_token"]
    cfg["telegram"]["chat_id"]   = input(f"  Chat ID   [{cfg['telegram']['chat_id'] or 'not set'}]: ").strip() or cfg["telegram"]["chat_id"]

    print("\n--- Default channel ---")
    ch = input("  Default channel [pushover/telegram/both] (default: pushover): ").strip()
    cfg["default_channel"] = ch if ch in ("pushover", "telegram", "both") else "pushover"

    save_config(cfg)
    print("\nSetup complete. Run a test: yos-notify 'Test' 'Hello from yOS'")


# ─── CLI ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        prog="yos-notify",
        description="yOS Universal Notification Module"
    )
    parser.add_argument("title",   nargs="?", help="Notification title")
    parser.add_argument("message", nargs="?", help="Notification body")
    parser.add_argument("--channel",  default=None,  choices=["pushover", "telegram", "both"],
                        help="Notification channel (default: from config)")
    parser.add_argument("--device",   default="all",
                        choices=["all", "ios", "macos", "android", "n100"],
                        help="Target device (Pushover only)")
    parser.add_argument("--priority", default=0, type=int,
                        choices=[-2, -1, 0, 1, 2],
                        help="Pushover priority (-2 silent → 2 emergency)")
    parser.add_argument("--sound",    default=None,
                        help="Pushover sound name (e.g. 'magic', 'bike')")
    parser.add_argument("--setup",    action="store_true",
                        help="Run interactive setup wizard")
    parser.add_argument("--test",     action="store_true",
                        help="Send a test notification")

    args = parser.parse_args()

    if args.setup:
        setup_wizard()
        return

    if args.test:
        notify("yOS-Notify Test", "Module is working correctly ✅",
               channel=args.channel, device=args.device)
        return

    if not args.title or not args.message:
        parser.print_help()
        return

    notify(args.title, args.message,
           channel=args.channel,
           device=args.device,
           priority=args.priority,
           sound=args.sound)


if __name__ == "__main__":
    main()
