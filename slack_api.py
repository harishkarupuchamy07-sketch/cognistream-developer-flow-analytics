import json
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent / "events.json"


def extract_slack_events():
    """Extract Slack events from the raw event data."""
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        events = json.load(file)

    slack_events = [
        event for event in events
        if event["source"] == "Slack"
    ]

    return slack_events


if __name__ == "__main__":
    events = extract_slack_events()

    print("Slack events extracted:")
    for event in events:
        print(event)