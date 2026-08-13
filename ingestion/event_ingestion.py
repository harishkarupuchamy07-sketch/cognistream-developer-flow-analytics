from github_api import extract_github_events
from ide_activity import extract_ide_events
from slack_api import extract_slack_events


def ingest_events():
    """Collect events from GitHub, IDE, and Slack sources."""

    github_events = extract_github_events()
    ide_events = extract_ide_events()
    slack_events = extract_slack_events()

    all_events = github_events + ide_events + slack_events

    return all_events


if __name__ == "__main__":
    events = ingest_events()

    print(f"Total events ingested: {len(events)}")

    for event in events:
        print(event)