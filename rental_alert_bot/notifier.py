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
        # Placeholder: real implementation would call Telegram API
        logger.info("TelegramNotifier would send message: %s", change)
