"""
clickhouse_setup.py
--------------------
Week 2 - Data Modeling: "Deploy ClickHouse" and create the event table.

We use chdb (https://github.com/chdb-io/chdb) - an embedded build of the
real ClickHouse SQL engine, run in-process. This is genuine ClickHouse SQL
(MergeTree engine, columnar storage, ClickHouse types) without needing a
standalone server/container - ideal for local dev before you point the
same DDL at a real `clickhouse-server` in docker-compose.yml for
production.

Persisted to disk at ./clickhouse_data so the warehouse survives between
script runs (like a real deployed instance).
"""

from pathlib import Path
import chdb

DB_PATH = Path(__file__).resolve().parent / "clickhouse_data"
DB_PATH.mkdir(exist_ok=True)

SESSION = chdb.session.Session(str(DB_PATH))

CREATE_DB = "CREATE DATABASE IF NOT EXISTS cognistream"

CREATE_EVENTS_TABLE = """
CREATE TABLE IF NOT EXISTS cognistream.events
(
    developer_id String,
    event_ts     DateTime,
    event_date   Date MATERIALIZED toDate(event_ts),
    source       LowCardinality(String),
    event_type   LowCardinality(String)
)
ENGINE = MergeTree
ORDER BY (developer_id, event_ts)
"""


def deploy():
    SESSION.query(CREATE_DB)
    SESSION.query(CREATE_EVENTS_TABLE)
    print("ClickHouse deployed (embedded via chdb).")
    print(f"Data directory: {DB_PATH}")
    print("Database 'cognistream' and table 'cognistream.events' are ready.")

    result = SESSION.query("SHOW TABLES FROM cognistream", "PrettyCompact")
    print(result)


if __name__ == "__main__":
    deploy()
