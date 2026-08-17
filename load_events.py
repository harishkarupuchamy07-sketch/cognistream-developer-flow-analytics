import json
from pathlib import Path

# pyrefly: ignore [missing-import]
import polars as pl
from clickhouse_driver import Client

from clickhouse_config import ClickHouseConfig
from normalize_events import normalize_timestamp


INPUT_FILE = Path(__file__).resolve().parent / "events.json"
TABLE = "cognistream.events"


REQUIRED_FIELDS = {
    "developer_id": pl.String(),
    "timestamp": pl.String(),
    "source": pl.String(),
    "event_type": pl.String(),
}


def clean_events() -> pl.DataFrame:
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        events = json.load(file)

    df = pl.DataFrame(events)

    missing = [field for field in REQUIRED_FIELDS if field not in df.columns]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")

    df = df.with_columns(
        [
            pl.col("developer_id").str.strip_chars().cast(pl.String()),
            pl.col("source").str.strip_chars().cast(pl.String()),
            pl.col("event_type").str.strip_chars().str.to_lowercase().str.replace_all(" ", "_").cast(pl.String()),
        ]
    )

    df = df.with_columns(
        pl.col("timestamp")
        .map_elements(normalize_timestamp, return_dtype=pl.String)
        .str.to_datetime(time_unit="ms")
        .alias("timestamp")
    )

    df = df.filter(
        pl.all_horizontal(
            pl.col("developer_id").is_not_null(),
            pl.col("developer_id").str.strip_chars().str.len_chars() > 0,
            pl.col("timestamp").is_not_null(),
            pl.col("source").is_not_null(),
            pl.col("event_type").is_not_null(),
        )
    )

    return df


def load_to_clickhouse(df: pl.DataFrame) -> None:
    config = ClickHouseConfig.from_env()
    client = Client(
        host=config.host,
        port=config.port,
        user=config.username,
        password=config.password,
        database=config.database,
        settings=config.settings,
    )

    data = df.to_dicts()

    client.execute(f"TRUNCATE TABLE {TABLE}")

    client.execute(
        f"INSERT INTO {TABLE} (developer_id, timestamp, source, event_type) VALUES",
        data,
    )


if __name__ == "__main__":
    df = clean_events()
    print(f"Cleaned {len(df)} events.")
    print(df.head())

    load_to_clickhouse(df)
    print(f"Loaded {len(df)} events into {TABLE}.")
