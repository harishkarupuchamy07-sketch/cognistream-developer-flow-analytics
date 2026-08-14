from ingestion.github_api import extract_github_events
from ingestion.slack_api import extract_slack_events
from ingestion.ide_activity import extract_ide_events


def test_github_events():
    events = extract_github_events()

    assert len(events) > 0
    assert all(event["source"] == "GitHub" for event in events)


def test_slack_events():
    events = extract_slack_events()

    assert len(events) > 0
    assert all(event["source"] == "Slack" for event in events)


def test_ide_events():
    events = extract_ide_events()

    assert len(events) > 0
    assert all(event["source"] == "VSCode" for event in events)