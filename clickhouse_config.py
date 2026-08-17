import os
from dataclasses import dataclass


@dataclass
class ClickHouseConfig:
    host: str
    port: int
    username: str
    password: str
    database: str
    settings: dict

    @classmethod
    def from_env(cls):
        return cls(
            host=os.getenv("CLICKHOUSE_HOST", "localhost"),
            port=int(os.getenv("CLICKHOUSE_PORT", "9000")),
            username=os.getenv("CLICKHOUSE_USER", "default"),
            password=os.getenv("CLICKHOUSE_PASSWORD", ""),
            database=os.getenv("CLICKHOUSE_DB", "cognistream"),
            settings={},
        )
