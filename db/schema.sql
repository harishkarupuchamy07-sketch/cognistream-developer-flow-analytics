CREATE DATABASE IF NOT EXISTS cognistream;

CREATE TABLE IF NOT EXISTS cognistream.events (
    developer_id String,
    timestamp DateTime64(3),
    source LowCardinality(String),
    event_type LowCardinality(String)
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (developer_id, timestamp, event_type)
SETTINGS index_granularity = 8192;
