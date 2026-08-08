#!/usr/bin/env python3
"""
yos_notif.py — Y-OS Universal Notification Module

Implémente le Y-OS Module Standard pour les notifications.
Route les messages vers Telegram (@yos_notif_bot).

Usage:
  from yos_notif import send_notif, NotifLevel

  send_notif("Tâche terminée", level=NotifLevel.SUCCESS)
"""

import json
import urllib.request
import urllib.parse
from enum import Enum

# Config
TELEGRAM_BOT_TOKEN = "8285003019:AAHoda1E674czRSYONLra94Ka4YX0nRgClo0nRgClo"
TELEGRAM_CHAT_ID = "223132272"

class NotifLevel(Enum):
    INFO = "ℹ️"
    SUCCESS = "✅"
    WARNING = "⚠️"
    ERROR = "❌"
    LOCK = "🔒"

def send_notif(message: str, level: NotifLevel = NotifLevel.INFO, silent: bool = False, title: str = None) -> bool:
    """
    Envoie une notification via Telegram.
    
    Args:
        message: Le contenu du message (HTML autorisé)
        level: Le niveau de notification (détermine l'icône)
        silent: Si True, la notification arrive sans son
        title: Titre optionnel en gras
    """
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        
        # Formatage standard Y-OS
        formatted_text = f"{level.value} "
        if title:
            formatted_text += f"<b>Y-OS — {title}</b>\n\n"
        else:
            formatted_text += "<b>Y-OS</b>\n\n"
            
        formatted_text += message

        data = urllib.parse.urlencode({
            "chat_id": TELEGRAM_CHAT_ID,
            "text": formatted_text,
            "parse_mode": "HTML",
            "disable_notification": str(silent).lower(),
        }).encode()

        req = urllib.request.Request(url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=5) as resp:
            result = json.loads(resp.read())
            return result.get("ok", False)
    except Exception as e:
        print(f"[YOS NOTIF] Erreur d'envoi Telegram: {e}")
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        msg = sys.argv[1]
        level_str = sys.argv[2].upper() if len(sys.argv) > 2 else "INFO"
        level = getattr(NotifLevel, level_str, NotifLevel.INFO)
        success = send_notif(msg, level=level)
        print("Envoyé" if success else "Échec")
    else:
        print("Usage: python3 yos_notif.py 'message' [INFO|SUCCESS|WARNING|ERROR|LOCK]")
