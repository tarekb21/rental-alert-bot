"""Mock fetcher that simulates Holidu listings."""
from dataclasses import dataclass, asdict
from typing import List
import random
import datetime


@dataclass
class Listing:
    id: str
    title: str
    city: str
    price: float
    available_from: str  # ISO date
    guests: int


class MockFetcher:
    def __init__(self, filters: dict = None):
        self.filters = filters or {}

    def fetch(self) -> List[dict]:
        # Generate deterministic-ish sample data
        base_date = datetime.date.today()
        sample = []
        for i in range(1, 6):
            price = 150 + random.choice([-30, -10, 0, 10, 50])
            avail = base_date + datetime.timedelta(days=random.randint(0, 60))
            l = Listing(
                id=f"L{i}",
                title=f"Sample Listing {i}",
                city=self.filters.get('city', 'Lisbon'),
                price=price,
                available_from=avail.isoformat(),
                guests=self.filters.get('guests', 2),
            )
            sample.append(asdict(l))
        return sample
