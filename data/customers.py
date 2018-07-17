"""
Customer data.
"""
import random
from datetime import datetime, timedelta
from data import CARS


def customers(count):
    """
    Generate customers, trying to keep within business hours.
    """
    today = datetime.today()
    next_time = datetime(today.year, today.month, today.day, 8)
    for _ in range(count):
        arrival_gap = timedelta(
            hours=random.randint(0, 1),
            minutes=random.randint(0, 59)
        )
        next_time = next_time + arrival_gap
        yield {
            "arrival_time": next_time,
            "interest": random.randint(0, len(CARS)),
            "sale_closed": random.random() > 0.7
        }
        if next_time.hour > 17:
            next_time = next_time.replace(day=next_time.day + 1, hour=8)
