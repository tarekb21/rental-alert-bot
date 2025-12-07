Holidu Availability & Price Alert Bot

Small demo project that periodically fetches rental listings, detects availability or price changes, and sends notifications.

Quick start

- Create a virtualenv and install dependencies from `requirements.txt`.
- Update `config.example.yaml` and rename to `config.yaml`.
- Run `python -m rental_alert_bot.main` to run once, or schedule with cron / systemd.

What is included

- Mock fetcher that returns sample listings (`rental_alert_bot.fetcher`).
- SQLite storage with change history (`rental_alert_bot.storage`).
- Console and placeholder Telegram notifiers (`rental_alert_bot.notifier`).
- Scheduler using APScheduler; configure `fetch_interval_minutes` in `config.yaml`.

Run locally

1. Copy `config.example.yaml` to `config.yaml` and edit as needed.
2. Run the bot:

```bash
python -m rental_alert_bot.main
```

