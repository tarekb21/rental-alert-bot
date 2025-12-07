"""Demo script: run the bot scheduler a few times (fast interval) for testing.

Usage: python demo_scheduler.py
"""
import time
from apscheduler.schedulers.background import BackgroundScheduler
from rental_alert_bot.main import run_once, load_config


def main():
    config = load_config()
    scheduler = BackgroundScheduler()
    # run every 2 seconds for demo
    scheduler.add_job(lambda: run_once(config), 'interval', seconds=2)
    scheduler.start()
    print('Scheduler started for demo (runs 3 times)')
    try:
        time.sleep(7)
    finally:
        scheduler.shutdown()
        print('Demo scheduler stopped')


if __name__ == '__main__':
    main()
