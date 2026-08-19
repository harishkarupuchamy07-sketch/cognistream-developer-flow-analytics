"""
load_to_clickhouse.py
----------------------
Week 2 - ELT Pipeline: use Polars to clean the extracted JSON payloads
(events_normalized.json from Week 1) and load them into the ClickHouse
'cognistream.events' table.

Cleaning steps performed with Polars:
    1. Load the normalized JSON into a DataFrame.
    2. Parse timestamp strings -> proper Datetime dtype.
    3. Drop exact duplicate events (dedupe on all columns).
    4. Drop rows with any null in required fields.
    5. Standardize casing on source/event_type (defensive, in case future
       raw payloads aren't pre-cleaned by normalize_events.py).
    6. Sort chronologically per developer.

The cleaned frame is then written to a Parquet staging file and loaded
into ClickHouse via `INSERT INTO ... SELECT * FROM file(...)`, which is
how a real ClickHouse ELT hop from a data lake staging area works.
"""

from pathlib import Path

import chdb
import polars as pl

PROJECT_DIR = Path(__file__).resolve().parent
NORMALIZED_FILE = PROJECT_DIR / "data" / "processed" / "events_normalized.json"
STAGING_PARQUET = PROJECT_DIR / "data" / "processed" / "events_staged.parquet"
DB_PATH = PROJECT_DIR / "clickhouse_data"


def clean_with_polars() -> pl.DataFrame:
    df = pl.read_json(NORMALIZED_FILE)

    df = (
        df.with_columns(
            pl.col("developer_id").str.strip_chars(),
            pl.col("source").str.strip_chars(),
            pl.col("event_type").str.strip_chars().str.to_lowercase(),
            # normalize_events.py already emits ISO timestamps (some with a
            # trailing "Z"); strip that before parsing so Polars can infer.
            pl.col("timestamp").str.replace("Z$", "").alias("timestamp"),
        )
        .with_columns(
            pl.col("timestamp").str.to_datetime(strict=False).alias("event_ts")
        )
        .drop_nulls(subset=["developer_id", "event_ts", "source", "event_type"])
        .unique()
        .sort(["developer_id", "event_ts"])
        .select(["developer_id", "event_ts", "source", "event_type"])
    )

    return df


def load_to_clickhouse(df: pl.DataFrame):
    STAGING_PARQUET.parent.mkdir(parents=True, exist_ok=True)
    df.write_parquet(STAGING_PARQUET)

    session = chdb.session.Session(str(DB_PATH))

    session.query("TRUNCATE TABLE IF EXISTS cognistream.events")
    session.query(f"""
        INSERT INTO cognistream.events (developer_id, event_ts, source, event_type)
        SELECT developer_id, event_ts, source, event_type
        FROM file('{STAGING_PARQUET}', Parquet)
    """)

    count = str(session.query(
        "SELECT count() FROM cognistream.events", "TabSeparated"
    )).strip()
    print(f"Loaded {count} rows into cognistream.events")

    preview = session.query(
        "SELECT * FROM cognistream.events ORDER BY developer_id, event_ts LIMIT 8",
        "PrettyCompact",
    )
    print(preview)


if __name__ == "__main__":
    raw_df = pl.read_json(NORMALIZED_FILE)
    cleaned_df = clean_with_polars()

    print(f"Raw normalized events:   {raw_df.height}")
    print(f"Cleaned events (deduped): {cleaned_df.height}")

    load_to_clickhouse(cleaned_df)
