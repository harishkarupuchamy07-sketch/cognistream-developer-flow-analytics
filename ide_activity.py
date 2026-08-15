import json
from pathlib import Path
DATA_FILE = Path(__file__).resolve().parent / "events.json"


def extract_ide_events():
    """Extract IDE activity events from the raw event data."""
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        events = json.load(file)

    ide_events = [
        event for event in events
        if event["source"] == "VSCode"
    ]

    return ide_events


if __name__ == "__main__":
    events = extract_ide_events()

    print("IDE events extracted:")
    for event in events:
        print(event)
