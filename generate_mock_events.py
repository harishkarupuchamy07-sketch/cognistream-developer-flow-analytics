"""
generate_mock_events.py
------------------------
Week 1 only gave us 5 sample events (1 dev, 1 day) - not enough to compute
anything meaningful for Week 2 (Flow-State logic, ClickHouse aggregates).

This script generates a realistic week's worth of mock developer activity
across multiple devs / sources, using the SAME schema Week 1 already
established: developer_id, timestamp, source, event_type.

Sources / event types mirror what github_api.py / slack_api.py /
ide_activity.py / jira_api.py already filter on:
    VSCode -> coding_start, coding, coding_end
    Slack  -> message
    GitHub -> commit
    Jira   -> ticket_update
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

OUTPUT_FILE = Path(__file__).resolve().parent / "events.json"

DEVELOPERS = [f"DEV{i:03d}" for i in range(1, 6)]  # DEV001..DEV005
DAYS = 5  # one working week
START_DATE = datetime(2026, 8, 10, 9, 0, 0)  # Monday 9:00 AM


def build_day_for_dev(dev_id, day_offset):
    """Simulate one developer's day: coding blocks interrupted by Slack/Jira,
    with occasional GitHub commits."""
    events = []
    day_start = START_DATE + timedelta(days=day_offset)
    t = day_start

    # A day is made of several "coding sessions" separated by interruptions
    num_sessions = random.randint(3, 6)

    for _ in range(num_sessions):
        # start a coding block
        events.append({
            "developer_id": dev_id,
            "timestamp": t.isoformat(),
            "source": "VSCode",
            "event_type": "coding_start",
        })

        block_minutes = random.choice([15, 25, 40, 55, 90, 110])  # some long flow blocks
        cursor = t
        # emit a couple of "coding" heartbeat events through the block
        for _ in range(random.randint(1, 3)):
            cursor += timedelta(minutes=block_minutes / 3)
            events.append({
                "developer_id": dev_id,
                "timestamp": cursor.isoformat(),
                "source": "VSCode",
                "event_type": "coding",
            })

        t = t + timedelta(minutes=block_minutes)
        events.append({
            "developer_id": dev_id,
            "timestamp": t.isoformat(),
            "source": "VSCode",
            "event_type": "coding_end",
        })

        # interruption: Slack message, GitHub commit, or Jira update
        interruption = random.choices(
            ["Slack", "GitHub", "Jira", None],
            weights=[0.45, 0.25, 0.15, 0.15],
        )[0]

        gap_minutes = random.randint(2, 20)  # break between blocks
        t += timedelta(minutes=gap_minutes)

        if interruption == "Slack":
            events.append({
                "developer_id": dev_id,
                "timestamp": t.isoformat(),
                "source": "Slack",
                "event_type": "message",
            })
        elif interruption == "GitHub":
            events.append({
                "developer_id": dev_id,
                "timestamp": t.isoformat(),
                "source": "GitHub",
                "event_type": "commit",
            })
        elif interruption == "Jira":
            events.append({
                "developer_id": dev_id,
                "timestamp": t.isoformat(),
                "source": "Jira",
                "event_type": "ticket_update",
            })

    return events


def generate_events():
    all_events = []
    for day_offset in range(DAYS):
        for dev in DEVELOPERS:
            all_events.extend(build_day_for_dev(dev, day_offset))

    # sort chronologically (still grouped realistically by dev within a day)
    all_events.sort(key=lambda e: (e["timestamp"], e["developer_id"]))
    return all_events


if __name__ == "__main__":
    events = generate_events()
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2)

    print(f"Generated {len(events)} mock events across {len(DEVELOPERS)} developers "
          f"over {DAYS} days.")
    print(f"Saved to: {OUTPUT_FILE}")
