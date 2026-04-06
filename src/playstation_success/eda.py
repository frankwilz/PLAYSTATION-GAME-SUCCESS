from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from playstation_success.features import build_feature_frame


EDA_NUMERIC_COLUMNS = [
    "highest_price",
    "metacritic_score",
    "metacritic_rating_count",
    "metacritic_user_score",
    "metacritic_user_rating_count",
    "playstation_score",
    "playstation_rating_count",
]


def build_eda_tables(dataframe: pd.DataFrame) -> dict[str, pd.DataFrame]:
    enriched = build_feature_frame(dataframe)

    missing_values = dataframe.isna().sum().rename("missing_count").to_frame()
    numeric_summary = dataframe[EDA_NUMERIC_COLUMNS].describe().transpose()
    platform_summary = (
        enriched.groupby("platform", dropna=False)
        .agg(
            game_count=("game_name", "count"),
            avg_price=("highest_price", "mean"),
            avg_playstation_score=("playstation_score", "mean"),
            avg_metacritic_score=("metacritic_score", "mean"),
        )
        .sort_values("game_count", ascending=False)
    )
    genre_summary = (
        enriched.groupby("genre_primary", dropna=False)
        .agg(
            game_count=("genre_primary", "count"),
            avg_playstation_score=("playstation_score", "mean"),
            avg_price=("highest_price", "mean"),
        )
        .sort_values("game_count", ascending=False)
    )
    year_summary = (
        enriched.groupby("release_year", dropna=False)
        .agg(
            game_count=("game_name", "count"),
            avg_playstation_score=("playstation_score", "mean"),
            avg_price=("highest_price", "mean"),
        )
        .sort_index()
    )
    correlations = dataframe[EDA_NUMERIC_COLUMNS].corr(numeric_only=True)

    return {
        "missing_values": missing_values,
        "numeric_summary": numeric_summary,
        "platform_summary": platform_summary,
        "genre_summary": genre_summary,
        "year_summary": year_summary,
        "correlations": correlations,
    }


def export_eda_bundle(dataframe: pd.DataFrame, tables_dir: Path, figures_dir: Path) -> None:
    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    tables = build_eda_tables(dataframe)
    for name, table in tables.items():
        table.to_csv(tables_dir / f"{name}.csv")

    _save_price_distribution(dataframe, figures_dir / "price_distribution.png")
    _save_score_relationship(dataframe, figures_dir / "metacritic_vs_playstation_score.png")
    _save_platform_score_chart(dataframe, figures_dir / "platform_average_scores.png")


def _save_price_distribution(dataframe: pd.DataFrame, output_path: Path) -> None:
    prices = dataframe["highest_price"].dropna()

    plt.figure(figsize=(10, 6))
    plt.hist(prices, bins=30, edgecolor="black")
    plt.title("Price Distribution")
    plt.xlabel("Highest Price")
    plt.ylabel("Game Count")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def _save_score_relationship(dataframe: pd.DataFrame, output_path: Path) -> None:
    score_frame = dataframe[["metacritic_score", "playstation_score"]].dropna()

    plt.figure(figsize=(10, 6))
    plt.scatter(
        score_frame["metacritic_score"],
        score_frame["playstation_score"],
        alpha=0.4,
    )
    plt.title("Metacritic Score vs PlayStation Score")
    plt.xlabel("Metacritic Score")
    plt.ylabel("PlayStation Score")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def _save_platform_score_chart(dataframe: pd.DataFrame, output_path: Path) -> None:
    platform_scores = (
        dataframe.groupby("platform")
        .agg(avg_playstation_score=("playstation_score", "mean"), games=("game_name", "count"))
        .query("games >= 25")
        .sort_values("avg_playstation_score", ascending=False)
        .head(10)
    )

    plt.figure(figsize=(12, 6))
    plt.bar(platform_scores.index.astype(str), platform_scores["avg_playstation_score"])
    plt.title("Average PlayStation Score by Platform")
    plt.xlabel("Platform")
    plt.ylabel("Average PlayStation Score")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

