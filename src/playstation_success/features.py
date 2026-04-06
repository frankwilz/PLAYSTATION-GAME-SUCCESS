from __future__ import annotations

import numpy as np
import pandas as pd


TARGET_COLUMN = "playstation_score"
MODEL_FEATURES = [
    "highest_price",
    "release_year",
    "release_month",
    "release_quarter",
    "genre_primary",
    "genre_count",
    "publisher",
    "platform",
    "is_multi_platform_listing",
    "metacritic_score",
    "metacritic_rating_count",
    "metacritic_user_score",
    "metacritic_user_rating_count",
    "has_metacritic",
    "price_bucket",
]
NUMERIC_FEATURES = [
    "highest_price",
    "release_year",
    "release_month",
    "release_quarter",
    "genre_count",
    "is_multi_platform_listing",
    "metacritic_score",
    "metacritic_rating_count",
    "metacritic_user_score",
    "metacritic_user_rating_count",
    "has_metacritic",
]
CATEGORICAL_FEATURES = [
    "genre_primary",
    "publisher",
    "platform",
    "price_bucket",
]


def _first_genre(genre_value: object) -> str:
    if pd.isna(genre_value):
        return "Unknown"
    parts = [part.strip() for part in str(genre_value).split("/") if part.strip()]
    return parts[0] if parts else "Unknown"


def _genre_count(genre_value: object) -> int:
    if pd.isna(genre_value):
        return 0
    return len([part for part in str(genre_value).split("/") if part.strip()])


def build_feature_frame(dataframe: pd.DataFrame) -> pd.DataFrame:
    feature_frame = dataframe.copy()

    feature_frame["release_year"] = feature_frame["release_date"].dt.year
    feature_frame["release_month"] = feature_frame["release_date"].dt.month
    feature_frame["release_quarter"] = feature_frame["release_date"].dt.quarter
    feature_frame["genre_primary"] = feature_frame["genre"].apply(_first_genre)
    feature_frame["genre_count"] = feature_frame["genre"].apply(_genre_count)
    feature_frame["is_multi_platform_listing"] = (
        feature_frame["platform"].fillna("").str.contains("/", regex=False).astype(int)
    )
    feature_frame["has_metacritic"] = feature_frame["metacritic_score"].notna().astype(int)
    feature_frame["price_bucket"] = pd.cut(
        feature_frame["highest_price"],
        bins=[-np.inf, 20, 40, 60, np.inf],
        labels=["budget", "midrange", "premium", "collector"],
    ).astype("string")

    return feature_frame


def make_modeling_frame(dataframe: pd.DataFrame) -> pd.DataFrame:
    feature_frame = build_feature_frame(dataframe)
    required_columns = MODEL_FEATURES + [TARGET_COLUMN]
    modeling_frame = feature_frame.loc[:, required_columns].dropna(subset=[TARGET_COLUMN])

    numeric_columns = NUMERIC_FEATURES + [TARGET_COLUMN]
    for column in numeric_columns:
        modeling_frame[column] = (
            pd.to_numeric(modeling_frame[column], errors="coerce").astype(float)
        )

    for column in CATEGORICAL_FEATURES:
        series = modeling_frame[column].astype("object")
        modeling_frame[column] = series.where(pd.notna(series), np.nan)

    return modeling_frame.reset_index(drop=True)
