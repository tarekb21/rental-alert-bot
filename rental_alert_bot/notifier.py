"""Notification backends."""
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class ConsoleNotifier:
    def notify(self, change: Dict):
        ct = change.get('change_type')
        lid = change.get('listing_id')
        print(f"[ALERT] {ct.upper()} - {lid}: {change.get('new')}")


class TelegramNotifier:
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id

    def notify(self, change: Dict):
        # Real implementation: POST to Telegram Bot API
        try:
            import requests
        except Exception:
            logger.warning("requests not available; cannot send Telegram message")
            return
        msg = f"ALERT {change.get('change_type').upper()} - {change.get('listing_id')}: {change.get('new') }"
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": msg}
        try:
            r = requests.post(url, json=payload, timeout=5)
            r.raise_for_status()
            logger.info("Telegram message sent for %s", change.get('listing_id'))
        except Exception as e:
            logger.exception("Failed to send Telegram message: %s", e)
