import json
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "processed" / "events_normalized.json"


REQUIRED_FIELDS = {
    "developer_id",
    "timestamp",
    "source",
    "event_type",
}


def validate_events():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        events = json.load(file)

    if not isinstance(events, list):
        raise ValueError("Events data must be a list.")

    for index, event in enumerate(events):
        if not isinstance(event, dict):
            raise ValueError(f"Event {index} is not a dictionary.")

        missing_fields = REQUIRED_FIELDS - event.keys()

        if missing_fields:
            raise ValueError(
                f"Event {index} is missing fields: {missing_fields}"
            )

        if not event["developer_id"]:
            raise ValueError(f"Event {index} has an empty developer_id.")

        if not event["timestamp"]:
            raise ValueError(f"Event {index} has an empty timestamp.")

        if not event["source"]:
            raise ValueError(f"Event {index} has an empty source.")

        if not event["event_type"]:
            raise ValueError(f"Event {index} has an empty event_type.")

    return True


if __name__ == "__main__":
    validate_events()
    print("Data validation passed successfully.")