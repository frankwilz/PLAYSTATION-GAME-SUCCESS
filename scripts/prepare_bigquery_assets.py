from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from playstation_success.config import CLEANED_CSV_PATH


BIGQUERY_EXPORT_DIR = PROJECT_ROOT / "cloud" / "bigquery" / "exports"
BIGQUERY_SCHEMA_DIR = PROJECT_ROOT / "cloud" / "bigquery" / "schema"
BIGQUERY_SQL_DIR = PROJECT_ROOT / "cloud" / "bigquery" / "sql"
BIGQUERY_EXPORT_CSV = BIGQUERY_EXPORT_DIR / "cleaned_game_details_bigquery.csv"
BIGQUERY_SCHEMA_JSON = BIGQUERY_SCHEMA_DIR / "cleaned_games_schema.json"


SCHEMA = [
    {"name": "game_name", "type": "STRING", "mode": "NULLABLE"},
    {"name": "highest_price", "type": "FLOAT", "mode": "NULLABLE"},
    {"name": "release_date", "type": "DATE", "mode": "NULLABLE"},
    {"name": "genre", "type": "STRING", "mode": "NULLABLE"},
    {"name": "publisher", "type": "STRING", "mode": "NULLABLE"},
    {"name": "platform", "type": "STRING", "mode": "NULLABLE"},
    {"name": "metacritic_score", "type": "FLOAT", "mode": "NULLABLE"},
    {"name": "metacritic_rating_count", "type": "FLOAT", "mode": "NULLABLE"},
    {"name": "metacritic_user_score", "type": "FLOAT", "mode": "NULLABLE"},
    {"name": "metacritic_user_rating_count", "type": "FLOAT", "mode": "NULLABLE"},
    {"name": "playstation_score", "type": "FLOAT", "mode": "NULLABLE"},
    {"name": "playstation_rating_count", "type": "FLOAT", "mode": "NULLABLE"},
]


def build_bigquery_export() -> None:
    dataframe = pd.read_csv(CLEANED_CSV_PATH)
    dataframe["release_date"] = pd.to_datetime(
        dataframe["release_date"], errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    BIGQUERY_EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    BIGQUERY_SCHEMA_DIR.mkdir(parents=True, exist_ok=True)
    BIGQUERY_SQL_DIR.mkdir(parents=True, exist_ok=True)

    dataframe.to_csv(BIGQUERY_EXPORT_CSV, index=False)
    BIGQUERY_SCHEMA_JSON.write_text(json.dumps(SCHEMA, indent=2), encoding="utf-8")

    print(f"BigQuery CSV export written to: {BIGQUERY_EXPORT_CSV}")
    print(f"BigQuery schema written to: {BIGQUERY_SCHEMA_JSON}")


if __name__ == "__main__":
    build_bigquery_export()
