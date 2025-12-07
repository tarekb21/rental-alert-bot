"""Entry point for the alert bot."""
import logging
import yaml
from pathlib import Path

from .fetcher import MockFetcher
from .storage import Storage
from .notifier import ConsoleNotifier, TelegramNotifier
from apscheduler.schedulers.background import BackgroundScheduler
import time

logger = logging.getLogger(__name__)


def load_config(path: str = "config.yaml"):
    p = Path(path)
    if not p.exists():
        p = Path(__file__).parents[1] / "config.example.yaml"
    with p.open() as f:
        return yaml.safe_load(f)


def run_once(config: dict):
    fetcher = MockFetcher(config.get('filters', {}))
    storage = Storage()
    notify_cfg = config.get('notify', {})
    if notify_cfg.get('method') == 'telegram':
        notifier = TelegramNotifier(notify_cfg.get('telegram_token'), notify_cfg.get('telegram_chat_id'))
    else:
        notifier = ConsoleNotifier()

    listings = fetcher.fetch()
    changes = storage.upsert_listings(listings)
    for change in changes:
        notifier.notify(change)


def main():
    logging.basicConfig(level=logging.INFO)
    config = load_config()
    interval = config.get('fetch_interval_minutes', 60)
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: run_once(config), 'interval', minutes=interval)
    scheduler.start()
    logging.info("Scheduler started, running every %s minutes", interval)
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


if __name__ == '__main__':
    main()
