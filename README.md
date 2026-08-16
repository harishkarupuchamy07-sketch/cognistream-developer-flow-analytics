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
