from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator


PROJECT_DIR = "/mnt/c/Users/91701/Desktop/khushi-217-cognistream-developer-flow-analytics"

with DAG(
    dag_id="cognistream_daily_ingestion",
    start_date=datetime(2026, 8, 13),
    schedule="0 9 * * *",
    catchup=False,
    tags=["cognistream", "ingestion"],
) as dag:

    github_extraction = BashOperator(
        task_id="github_extraction",
        bash_command=f"cd {PROJECT_DIR} && python3 github_api.py",
    )

    slack_extraction = BashOperator(

        task_id="slack_extraction",
        bash_command=f"cd {PROJECT_DIR} && python3 slack_api.py",
)

    ide_extraction = BashOperator(
        task_id="ide_extraction",
        bash_command=f"cd {PROJECT_DIR} && python3 ide_activity.py",
    )

    jira_extraction = BashOperator(
        task_id="jira_extraction",
        bash_command=f"cd {PROJECT_DIR} && python3 jira_api.py",
    )

    unified_ingestion = BashOperator(
        task_id="unified_ingestion",
        bash_command=f"cd {PROJECT_DIR} && python3 event_ingestion.py",
    )

    normalize_events = BashOperator(
        task_id="normalize_events",
        bash_command=f"cd {PROJECT_DIR} && python3 normalize_events.py",
    )

    validate_data = BashOperator(
        task_id="validate_data",
        bash_command=f"cd {PROJECT_DIR} && python3 validate_data.py",
    )

    github_extraction >> unified_ingestion
    slack_extraction >> unified_ingestion
    ide_extraction >> unified_ingestion
    jira_extraction >> unified_ingestion

    unified_ingestion >> normalize_events
    normalize_events >> validate_data