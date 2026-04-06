from __future__ import annotations

import json
import sqlite3

import pandas as pd

from playstation_success.config import (
    CLEANED_CSV_PATH,
    CLEANED_SQLITE_PATH,
    DATASET_PATH,
    DATA_QUALITY_REPORT_PATH,
    LEGACY_DATASET_PATH,
)


NUMERIC_COLUMNS = [
    "metacritic_score",
    "metacritic_rating_count",
    "metacritic_user_score",
    "metacritic_user_rating_count",
    "playstation_score",
    "playstation_rating_count",
]


def load_raw_dataset(csv_path=DATASET_PATH) -> pd.DataFrame:
    """Load the raw CSV and remove trailing empty columns."""
    csv_path = csv_path if csv_path.exists() else LEGACY_DATASET_PATH
    dataframe = pd.read_csv(csv_path, sep=";")
    valid_columns = [
        column
        for column in dataframe.columns
        if str(column).strip() and not str(column).startswith("Unnamed:")
    ]
    dataframe = dataframe.loc[:, valid_columns]
    dataframe = dataframe.dropna(axis=1, how="all")
    return dataframe


def clean_dataset(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Apply project-level cleaning so downstream analysis works consistently."""
    cleaned = dataframe.copy()

    text_columns = cleaned.select_dtypes(include="object").columns
    for column in text_columns:
        cleaned[column] = cleaned[column].astype("string").str.strip()

    cleaned = cleaned.replace({"--": pd.NA, "": pd.NA})

    cleaned["highest_price"] = (
        cleaned["highest_price"]
        .astype("string")
        .str.replace(r"[^\d.]", "", regex=True)
        .replace({"": pd.NA, ".": pd.NA})
        .pipe(pd.to_numeric, errors="coerce")
    )

    cleaned["release_date"] = pd.to_datetime(cleaned["release_date"], errors="coerce")

    for column in NUMERIC_COLUMNS:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    cleaned["game_name"] = cleaned["game_name"].str.strip()
    cleaned["genre"] = cleaned["genre"].str.replace(r"\s*/\s*", " / ", regex=True)
    cleaned["publisher"] = cleaned["publisher"].str.strip()
    cleaned["platform"] = cleaned["platform"].str.strip()

    cleaned = cleaned.drop_duplicates(
        subset=["game_name", "platform", "release_date"], keep="first"
    ).reset_index(drop=True)

    return cleaned


def load_clean_dataset(csv_path=DATASET_PATH) -> pd.DataFrame:
    return clean_dataset(load_raw_dataset(csv_path))


def build_data_quality_report(raw_dataframe: pd.DataFrame, clean_dataframe: pd.DataFrame) -> dict:
    report = {
        "raw_row_count": int(len(raw_dataframe)),
        "clean_row_count": int(len(clean_dataframe)),
        "removed_rows": int(len(raw_dataframe) - len(clean_dataframe)),
        "column_count": int(len(clean_dataframe.columns)),
        "missing_values": {
            column: int(value) for column, value in clean_dataframe.isna().sum().items()
        },
        "dtypes": {column: str(dtype) for column, dtype in clean_dataframe.dtypes.items()},
        "notes": [
            "Removed trailing empty columns from the source CSV.",
            "Standardized missing markers such as '--' and blank strings.",
            "Converted prices and review columns to numeric types.",
            "Parsed release_date into datetime values.",
            "Removed duplicates by game_name, platform, and release_date.",
        ],
    }
    return report


def export_clean_data_assets(
    raw_csv_path=DATASET_PATH,
    cleaned_csv_path=CLEANED_CSV_PATH,
    sqlite_path=CLEANED_SQLITE_PATH,
    report_path=DATA_QUALITY_REPORT_PATH,
) -> dict:
    raw_dataframe = load_raw_dataset(raw_csv_path)
    clean_dataframe = clean_dataset(raw_dataframe)

    cleaned_csv_path.parent.mkdir(parents=True, exist_ok=True)
    clean_dataframe.to_csv(cleaned_csv_path, index=False)

    with sqlite3.connect(sqlite_path) as connection:
        clean_dataframe.to_sql("cleaned_games", connection, if_exists="replace", index=False)

    report = build_data_quality_report(raw_dataframe, clean_dataframe)
    with open(report_path, "w", encoding="utf-8") as output_file:
        json.dump(report, output_file, indent=2)

    return report
