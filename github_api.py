import json
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent / "events.json"


def extract_github_events():
    """Extract GitHub events from the raw event data."""
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        events = json.load(file)

    github_events = [
        event for event in events
        if event["source"] == "GitHub"
    ]

    return github_events


if __name__ == "__main__":
    events = extract_github_events()

    print("GitHub events extracted:")
    for event in events:
        print(event)