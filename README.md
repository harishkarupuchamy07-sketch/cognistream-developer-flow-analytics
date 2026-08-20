# khushi-217-cognistream-developer-flow-analytics
CogniStream is a developer flow-state and cognitive load analytics platform that collects event data from GitHub, Jira, Slack, and IDEs, processes it with Python and Polars, stores it in ClickHouse, and provides insights through a React and Tremor.js dashboard.

## Week 1 – API Ingestion

### Completed Work

- Created the CogniStream GitHub repository and project structure.
- Created mock developer event data for GitHub, Slack, and IDE sources.
- Developed Python extraction scripts for ingesting source events.
- Created an Apache Airflow DAG to orchestrate the ingestion workflow.
- Configured the DAG for daily automated execution.
- Tested the ingestion pipeline through Airflow.
- Verified event normalization and data validation.
- Successfully validated the ingestion tasks through Airflow execution logs.

### Ingestion Workflow

GitHub / Slack / IDE / Jira
        ↓
Python Extraction Scripts
        ↓
Airflow DAG
        ↓
Unified Ingestion
        ↓
Event Normalization
        ↓
Data Validation

### Validation

- Airflow DAG execution and task logs were verified.
- Extraction tasks were executed through the ingestion DAG.
- Slack extraction completed with return code `0`.
- Normalization processed the available developer events.
- Project Git working tree was verified clean.
- Final commit was verified on both `origin/main` and `collab/main`.

## Week 2 – Data Modeling & Base Metrics

### Completed Work

- Expanded the Week 1 mock dataset (`generate_mock_events.py`) into a full working week: 506 events across 5 developers / 5 days, using the same event schema (`developer_id`, `timestamp`, `source`, `event_type`).
- Deployed ClickHouse (`clickhouse_setup.py`) via `chdb`, an embedded build of the real ClickHouse engine — same SQL/MergeTree engine as a standalone `clickhouse-server`, no container required for local dev. Data persists under `clickhouse_data/`.
- Created the `cognistream.events` MergeTree table, ordered by `(developer_id, event_ts)` for efficient per-developer time-series queries.
- Used **Polars** (`load_to_clickhouse.py`) to clean `data/processed/events_normalized.json`: parsed timestamps, stripped whitespace, lower-cased event types, dropped duplicates/nulls, and staged the result as Parquet.
- Loaded the cleaned Parquet into ClickHouse via `INSERT ... SELECT FROM file(...)`.
- Queried ClickHouse for base metrics (`base_metrics.py`) — total commits, Slack messages, Jira updates, coding sessions, and approximate hours in IDE, per developer and team-wide — and exported them to `frontend/public/metrics.json`.
- Scaffolded the **React + Tremor.js** dashboard (`frontend/`) and built the initial UI cards (`frontend/src/App.jsx`) showing those base metrics, reading from `metrics.json` (will switch to a live FastAPI call in Week 4).
- Fixed a path bug in `validate_data.py` that pointed one directory too high.

### Result (Mid-Project Review checkpoint)

```
Loaded 506 rows into cognistream.events

Per-developer base metrics:
DEV001 -> 6 commits, 9 Slack msgs, 5 Jira updates, 21 coding sessions, 7.17h in IDE
DEV002 -> 6 commits, 12 Slack msgs, 3 Jira updates, 22 coding sessions, 7.08h in IDE
DEV003 -> 4 commits, 9 Slack msgs, 0 Jira updates, 16 coding sessions, 5.50h in IDE
DEV004 -> 5 commits, 7 Slack msgs, 5 Jira updates, 23 coding sessions, 7.58h in IDE
DEV005 -> 6 commits, 10 Slack msgs, 2 Jira updates, 22 coding sessions, 7.42h in IDE

Team totals -> 506 events, 27 commits, 47 Slack messages, 15 Jira updates, 5 active devs
```

The frontend dashboard renders these numbers as Tremor stat cards + a per-developer table (`npm run dev` inside `frontend/`).

### How to reproduce

```bash
pip install -r requirements.txt --break-system-packages

python3 generate_mock_events.py     # refresh mock data (optional, already generated)
python3 event_ingestion.py
python3 normalize_events.py
python3 validate_data.py

python3 clickhouse_setup.py         # deploy ClickHouse + create schema
python3 load_to_clickhouse.py       # Polars clean -> load into ClickHouse
python3 base_metrics.py             # query metrics + export metrics.json

cd frontend
npm install --legacy-peer-deps
npm run dev                         # view the Base Metrics dashboard
```
