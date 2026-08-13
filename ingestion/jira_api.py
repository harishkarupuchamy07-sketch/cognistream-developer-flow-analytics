import json
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "raw" / "events.json"


def extract_jira_events():
    """Extract Jira events from the raw event data."""
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        events = json.load(file)

    jira_events = [
        event for event in events
        if event["source"] == "Jira"
    ]

    return jira_events


if __name__ == "__main__":
    events = extract_jira_events()

    print("Jira events extracted:")
    for event in events:
        print(event)