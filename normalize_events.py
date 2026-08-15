import json
from pathlib import Path
from datetime import datetime


INPUT_FILE = Path(__file__).resolve().parent / "events.json"
OUTPUT_FILE = Path(__file__).resolve().parent / "data" / "processed" / "events_normalized.json"
DEFAULT_DATE = "2026-08-12"


def normalize_timestamp(timestamp):
    timestamp = str(timestamp).strip()

    # Already a full ISO timestamp
    if "T" in timestamp:
        return timestamp

    # Time-only value such as 9, 9:45, 10:30, 11:00
    if ":" not in timestamp:
        timestamp = f"{timestamp}:00"

    dt = datetime.strptime(
        f"{DEFAULT_DATE} {timestamp}",
        "%Y-%m-%d %H:%M"
    )

    return dt.isoformat() + "Z"


def normalize_event(event):
    return {
        "developer_id": event["developer_id"].strip(),
        "timestamp": normalize_timestamp(event["timestamp"]),
        "source": event["source"].strip(),
        "event_type": event["event_type"].strip().lower().replace(" ", "_"),
    }


def normalize_events():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        events = json.load(file)

    normalized_events = [
        normalize_event(event)
        for event in events
    ]

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(normalized_events, file, indent=2)

    print(f"Normalized {len(normalized_events)} events.")
    print(f"Output saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    normalize_events()