"""
base_metrics.py
----------------
Week 2 - Base Metrics: query ClickHouse for the raw metrics the Week 2
frontend UI cards need to display (total commits, hours in IDE, messages,
ticket updates) per developer.

This is the query layer that a lightweight API (built in Week 4) would
wrap and hand to the React/Tremor.js dashboard.
"""

import json
from pathlib import Path
import chdb

DB_PATH = Path(__file__).resolve().parent / "clickhouse_data"
METRICS_EXPORT = Path(__file__).resolve().parent / "frontend" / "public" / "metrics.json"

QUERY = """
SELECT
    developer_id,
    countIf(source = 'GitHub' AND event_type = 'commit')          AS total_commits,
    countIf(source = 'Slack'  AND event_type = 'message')         AS slack_messages,
    countIf(source = 'Jira'   AND event_type = 'ticket_update')   AS jira_updates,
    countIf(source = 'VSCode' AND event_type = 'coding_start')    AS coding_sessions,
    round(
        countIf(source = 'VSCode') * 5 / 60.0,
    2)                                                             AS approx_hours_in_ide
FROM cognistream.events
GROUP BY developer_id
ORDER BY developer_id
"""

TEAM_QUERY = """
SELECT
    count()                                                          AS total_events,
    countIf(source = 'GitHub' AND event_type = 'commit')             AS total_commits,
    countIf(source = 'Slack'  AND event_type = 'message')            AS total_slack_messages,
    countIf(source = 'Jira'   AND event_type = 'ticket_update')      AS total_jira_updates,
    uniqExact(developer_id)                                          AS active_developers
FROM cognistream.events
"""


def export_metrics_json():
    """Export per-dev + team metrics as JSON for the React/Tremor UI cards
    (Week 2 frontend). In Week 4 this gets replaced by a live FastAPI call;
    for now the dashboard reads this static file, same shape either way."""
    session = chdb.session.Session(str(DB_PATH))

    per_dev = json.loads(str(session.query(QUERY, "JSON")))["data"]
    team = json.loads(str(session.query(TEAM_QUERY, "JSON")))["data"][0]

    METRICS_EXPORT.parent.mkdir(parents=True, exist_ok=True)
    with open(METRICS_EXPORT, "w") as f:
        json.dump({"team": team, "developers": per_dev}, f, indent=2)

    print(f"Exported metrics for UI cards -> {METRICS_EXPORT}")


def show_metrics():
    session = chdb.session.Session(str(DB_PATH))

    print("=== Per-developer base metrics ===")
    print(session.query(QUERY, "PrettyCompact"))

    print("=== Team-wide totals ===")
    print(session.query(TEAM_QUERY, "PrettyCompact"))

    export_metrics_json()


if __name__ == "__main__":
    show_metrics()
