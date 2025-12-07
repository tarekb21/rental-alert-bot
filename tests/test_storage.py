import tempfile
import shutil
from rental_alert_bot.storage import Storage


def test_upsert_new_and_update(tmp_path):
    db = tmp_path / "test.db"
    s = Storage(db)
    listings = [
        {"id": "T1", "price": 100, "available_from": "2025-12-20"},
    ]
    changes = s.upsert_listings(listings)
    assert len(changes) == 1
    assert changes[0]['change_type'] == 'new'

    # Update price
    listings[0]['price'] = 80
    changes = s.upsert_listings(listings)
    assert len(changes) == 1
    assert changes[0]['change_type'] == 'updated'
    s.close()
