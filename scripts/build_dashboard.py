from __future__ import annotations

import base64
import json
import os
import sys
from io import BytesIO
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
MPLCONFIG_DIR = PROJECT_ROOT / ".mplconfig"

MPLCONFIG_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPLCONFIG_DIR))
os.environ.setdefault("MPLBACKEND", "Agg")

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from playstation_success.config import (
    ARTIFACTS_DIR,
    DASHBOARD_HTML_PATH,
    DATA_QUALITY_REPORT_PATH,
)
from playstation_success.data import load_clean_dataset
from playstation_success.features import build_feature_frame


def figure_to_base64() -> str:
    buffer = BytesIO()
    plt.savefig(buffer, format="png", dpi=160, bbox_inches="tight", facecolor="#f4efe4")
    plt.close()
    return base64.b64encode(buffer.getvalue()).decode("ascii")


def style_axes(ax) -> None:
    ax.set_facecolor("#f4efe4")
    ax.tick_params(colors="#342a21", labelsize=9)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(axis="y", color="#d9cfc0", linewidth=0.7, alpha=0.7)
    ax.set_axisbelow(True)


def build_genre_chart(feature_df: pd.DataFrame) -> str:
    genre_summary = (
        feature_df.groupby("genre_primary", dropna=False)
        .agg(
            game_count=("game_name", "count"),
            avg_playstation_score=("playstation_score", "mean"),
        )
        .query("game_count >= 30")
        .sort_values("avg_playstation_score", ascending=False)
        .head(10)
        .sort_values("avg_playstation_score")
    )

    fig, ax = plt.subplots(figsize=(8.6, 5.2))
    style_axes(ax)
    ax.barh(
        genre_summary.index.astype(str),
        genre_summary["avg_playstation_score"],
        color="#205c5e",
    )
    ax.set_title("Top Genres By Average PlayStation Score", color="#1d1814", fontsize=14)
    ax.set_xlabel("Average PlayStation Score", color="#342a21")
    ax.set_ylabel("")
    return figure_to_base64()


def build_platform_chart(feature_df: pd.DataFrame) -> str:
    platform_summary = (
        feature_df.groupby("platform")
        .agg(
            game_count=("game_name", "count"),
            avg_playstation_score=("playstation_score", "mean"),
        )
        .query("game_count >= 25")
        .sort_values("avg_playstation_score", ascending=False)
        .head(10)
        .sort_values("avg_playstation_score")
    )

    fig, ax = plt.subplots(figsize=(8.6, 5.2))
    style_axes(ax)
    ax.barh(
        platform_summary.index.astype(str),
        platform_summary["avg_playstation_score"],
        color="#7a4c2f",
    )
    ax.set_title("Platform Leaderboard", color="#1d1814", fontsize=14)
    ax.set_xlabel("Average PlayStation Score", color="#342a21")
    ax.set_ylabel("")
    return figure_to_base64()


def build_price_chart(feature_df: pd.DataFrame) -> str:
    price_summary = (
        feature_df.groupby("price_bucket", dropna=False)
        .agg(
            game_count=("game_name", "count"),
            avg_playstation_score=("playstation_score", "mean"),
        )
        .dropna()
        .reindex(["budget", "midrange", "premium", "collector"])
    )

    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    style_axes(ax)
    ax.bar(
        price_summary.index.astype(str),
        price_summary["avg_playstation_score"],
        color=["#ceb888", "#d4965a", "#9e5f3f", "#4b3f72"],
    )
    ax.set_title("Price Bucket Comparison", color="#1d1814", fontsize=14)
    ax.set_xlabel("")
    ax.set_ylabel("Average PlayStation Score", color="#342a21")
    ax.grid(axis="x", visible=False)
    return figure_to_base64()


def build_scatter_chart(feature_df: pd.DataFrame) -> str:
    scatter_df = feature_df[["metacritic_score", "playstation_score"]].dropna()

    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    ax.set_facecolor("#f4efe4")
    ax.scatter(
        scatter_df["metacritic_score"],
        scatter_df["playstation_score"],
        s=18,
        alpha=0.35,
        color="#15616d",
        edgecolors="none",
    )
    ax.set_title("Metacritic vs PlayStation Score", color="#1d1814", fontsize=14)
    ax.set_xlabel("Metacritic Score", color="#342a21")
    ax.set_ylabel("PlayStation Score", color="#342a21")
    ax.grid(color="#d9cfc0", linewidth=0.7, alpha=0.7)
    for spine in ax.spines.values():
        spine.set_visible(False)
    return figure_to_base64()


def build_timing_heatmap(feature_df: pd.DataFrame) -> str:
    timing_summary = (
        feature_df.groupby(["release_year", "release_quarter"], dropna=False)
        .agg(avg_playstation_score=("playstation_score", "mean"))
        .reset_index()
        .dropna(subset=["release_year", "release_quarter"])
    )
    recent_timing = timing_summary.query("release_year >= 2014")
    pivot_timing = recent_timing.pivot(
        index="release_year",
        columns="release_quarter",
        values="avg_playstation_score",
    ).astype(float)

    fig, ax = plt.subplots(figsize=(7.8, 5.4))
    ax.set_facecolor("#f4efe4")
    heatmap = ax.imshow(pivot_timing.values, cmap="YlGnBu", aspect="auto")
    ax.set_title("Release Timing Heatmap", color="#1d1814", fontsize=14)
    ax.set_xticks(range(len(pivot_timing.columns)))
    ax.set_xticklabels([f"Q{int(value)}" for value in pivot_timing.columns], color="#342a21")
    ax.set_yticks(range(len(pivot_timing.index)))
    ax.set_yticklabels([str(int(value)) for value in pivot_timing.index], color="#342a21")
    ax.set_xlabel("Release Quarter", color="#342a21")
    ax.set_ylabel("Release Year", color="#342a21")
    for spine in ax.spines.values():
        spine.set_visible(False)
    colorbar = fig.colorbar(heatmap, ax=ax, shrink=0.82)
    colorbar.outline.set_visible(False)
    colorbar.ax.tick_params(labelsize=8, colors="#342a21")
    return figure_to_base64()


def build_feature_importance_chart() -> str:
    importance = pd.read_csv(ARTIFACTS_DIR / "feature_importance.csv").head(10)
    importance = importance.iloc[::-1]
    labels = [value.replace("numeric__", "").replace("categorical__", "") for value in importance["feature"]]

    fig, ax = plt.subplots(figsize=(8.8, 5.2))
    style_axes(ax)
    ax.barh(labels, importance["importance"], color="#a33b20")
    ax.set_title("Top Baseline Model Features", color="#1d1814", fontsize=14)
    ax.set_xlabel("Importance", color="#342a21")
    ax.set_ylabel("")
    return figure_to_base64()


def render_card(title: str, value: str, note: str) -> str:
    return f"""
    <article class="metric-card">
      <div class="metric-title">{title}</div>
      <div class="metric-value">{value}</div>
      <div class="metric-note">{note}</div>
    </article>
    """


def render_table(dataframe: pd.DataFrame) -> str:
    table = dataframe.copy()
    for column in table.columns:
        if pd.api.types.is_numeric_dtype(table[column]):
            table[column] = table[column].map(
                lambda value: f"{value:,.2f}" if pd.notna(value) else ""
            )
    return table.to_html(index=False, classes="summary-table", border=0)


def build_dashboard_html() -> str:
    feature_df = build_feature_frame(load_clean_dataset())
    quality_report = json.loads(DATA_QUALITY_REPORT_PATH.read_text())
    model_metrics = json.loads((ARTIFACTS_DIR / "model_metrics.json").read_text())

    platform_count = int(feature_df["platform"].dropna().nunique())
    avg_score = float(feature_df["playstation_score"].dropna().mean())
    avg_price = float(feature_df["highest_price"].dropna().mean())
    top_genre = (
        feature_df.groupby("genre_primary")["playstation_score"].mean().sort_values(ascending=False).index[0]
    )

    insight_table = (
        feature_df.groupby("price_bucket", dropna=False)
        .agg(
            games=("game_name", "count"),
            avg_playstation_score=("playstation_score", "mean"),
        )
        .dropna()
        .reset_index()
    )

    feature_table = pd.read_csv(ARTIFACTS_DIR / "feature_importance.csv").head(5)
    feature_table["feature"] = feature_table["feature"].str.replace("numeric__", "", regex=False)
    feature_table["feature"] = feature_table["feature"].str.replace("categorical__", "", regex=False)

    cards_html = "".join(
        [
            render_card("Cleaned Games", f"{quality_report['clean_row_count']:,}", "Rows available for analysis after ETL"),
            render_card("Platforms", f"{platform_count}", "Distinct platform labels in the cleaned dataset"),
            render_card("Average Score", f"{avg_score:.2f}", "Mean PlayStation score across rated games"),
            render_card("Average Price", f"EUR {avg_price:.2f}", "Mean listed price after cleaning"),
            render_card("Baseline R²", f"{model_metrics['r2']:.3f}", "Random forest regression benchmark"),
            render_card("Strongest Signal", top_genre, "Highest average-scoring primary genre"),
        ]
    )

    charts = {
        "genre_chart": build_genre_chart(feature_df),
        "platform_chart": build_platform_chart(feature_df),
        "price_chart": build_price_chart(feature_df),
        "scatter_chart": build_scatter_chart(feature_df),
        "timing_chart": build_timing_heatmap(feature_df),
        "importance_chart": build_feature_importance_chart(),
    }

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>PlayStation Game Success Dashboard</title>
  <style>
    :root {{
      --paper: #f4efe4;
      --ink: #1d1814;
      --muted: #6c6258;
      --line: #d9cfc0;
      --panel: rgba(255, 252, 247, 0.8);
      --accent: #205c5e;
      --accent-2: #a33b20;
      --accent-3: #7a4c2f;
      --shadow: 0 18px 40px rgba(30, 20, 10, 0.12);
    }}
    * {{
      box-sizing: border-box;
    }}
    body {{
      margin: 0;
      font-family: Georgia, "Times New Roman", serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(32, 92, 94, 0.12), transparent 28%),
        radial-gradient(circle at top right, rgba(163, 59, 32, 0.12), transparent 25%),
        linear-gradient(180deg, #f8f2e8 0%, #efe5d6 100%);
    }}
    .wrap {{
      width: min(1280px, calc(100% - 40px));
      margin: 0 auto;
      padding: 28px 0 48px;
    }}
    .hero {{
      display: grid;
      grid-template-columns: 1.5fr 1fr;
      gap: 22px;
      align-items: stretch;
      margin-bottom: 22px;
    }}
    .hero-panel, .side-panel, .section, .table-panel {{
      background: var(--panel);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(217, 207, 192, 0.8);
      border-radius: 24px;
      box-shadow: var(--shadow);
    }}
    .hero-panel {{
      padding: 30px 30px 26px;
      min-height: 260px;
    }}
    .eyebrow {{
      text-transform: uppercase;
      letter-spacing: 0.18em;
      font-size: 12px;
      color: var(--accent);
      margin-bottom: 12px;
      font-weight: 700;
    }}
    h1 {{
      margin: 0 0 14px;
      font-size: clamp(38px, 5vw, 62px);
      line-height: 0.96;
      font-weight: 700;
    }}
    .subtitle {{
      font-size: 18px;
      line-height: 1.5;
      max-width: 58ch;
      color: var(--muted);
      margin: 0 0 18px;
    }}
    .tag-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }}
    .tag {{
      border-radius: 999px;
      padding: 8px 12px;
      background: rgba(32, 92, 94, 0.09);
      color: #214e50;
      font-size: 13px;
      border: 1px solid rgba(32, 92, 94, 0.16);
    }}
    .side-panel {{
      padding: 26px;
      display: grid;
      gap: 14px;
    }}
    .side-block-title {{
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.16em;
      color: var(--accent-2);
      font-weight: 700;
      margin-bottom: 6px;
    }}
    .side-block-text {{
      font-size: 15px;
      line-height: 1.5;
      color: var(--muted);
    }}
    .metrics-grid {{
      display: grid;
      grid-template-columns: repeat(6, minmax(0, 1fr));
      gap: 14px;
      margin-bottom: 22px;
    }}
    .metric-card {{
      background: rgba(255, 252, 247, 0.8);
      border: 1px solid rgba(217, 207, 192, 0.8);
      border-radius: 20px;
      padding: 18px 16px;
      box-shadow: var(--shadow);
      min-height: 148px;
    }}
    .metric-title {{
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      color: var(--muted);
      margin-bottom: 12px;
      font-weight: 700;
    }}
    .metric-value {{
      font-size: 32px;
      line-height: 1;
      margin-bottom: 10px;
      font-weight: 700;
    }}
    .metric-note {{
      font-size: 14px;
      line-height: 1.45;
      color: var(--muted);
    }}
    .section-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 18px;
      margin-bottom: 18px;
    }}
    .section {{
      padding: 18px 18px 16px;
    }}
    .section-title {{
      margin: 0 0 12px;
      font-size: 24px;
    }}
    .section-note {{
      margin: 0 0 14px;
      color: var(--muted);
      line-height: 1.5;
      font-size: 15px;
    }}
    .chart {{
      width: 100%;
      border-radius: 18px;
      display: block;
      background: #f4efe4;
    }}
    .table-grid {{
      display: grid;
      grid-template-columns: 1.15fr 0.85fr;
      gap: 18px;
    }}
    .table-panel {{
      padding: 18px;
    }}
    .summary-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
      overflow: hidden;
      border-radius: 14px;
    }}
    .summary-table th {{
      text-align: left;
      padding: 12px 10px;
      background: rgba(32, 92, 94, 0.09);
      color: var(--ink);
      font-weight: 700;
      border-bottom: 1px solid var(--line);
    }}
    .summary-table td {{
      padding: 10px;
      border-bottom: 1px solid rgba(217, 207, 192, 0.7);
      color: #342a21;
    }}
    .summary-table tr:last-child td {{
      border-bottom: none;
    }}
    .footer {{
      margin-top: 18px;
      padding: 18px 4px 0;
      color: var(--muted);
      font-size: 13px;
    }}
    @media (max-width: 1080px) {{
      .hero,
      .section-grid,
      .table-grid,
      .metrics-grid {{
        grid-template-columns: 1fr 1fr;
      }}
    }}
    @media (max-width: 760px) {{
      .hero,
      .section-grid,
      .table-grid,
      .metrics-grid {{
        grid-template-columns: 1fr;
      }}
      .wrap {{
        width: min(100% - 24px, 1280px);
      }}
      h1 {{
        font-size: 36px;
      }}
    }}
  </style>
</head>
<body>
  <main class="wrap">
    <section class="hero">
      <div class="hero-panel">
        <div class="eyebrow">Presentation Dashboard</div>
        <h1>What Makes a PlayStation Game Successful?</h1>
        <p class="subtitle">
          A polished reporting layer built from the project notebook pipeline. This view combines ETL-backed metrics,
          exploratory findings, and the baseline prediction model into a dashboard that is ready for class presentation,
          demo recording, or slide capture.
        </p>
        <div class="tag-row">
          <span class="tag">Public Kaggle Dataset</span>
          <span class="tag">ETL + Storage + EDA + Prediction</span>
          <span class="tag">Python + Jupyter + SQLite</span>
        </div>
      </div>
      <aside class="side-panel">
        <div>
          <div class="side-block-title">Question</div>
          <div class="side-block-text">
            The project asks which factors are associated with stronger PlayStation game outcomes, using
            <strong>playstation_score</strong> as the primary success signal.
          </div>
        </div>
        <div>
          <div class="side-block-title">Method</div>
          <div class="side-block-text">
            Raw data is cleaned, stored in CSV and SQLite, explored through grouped summaries and visuals, and then used
            in a baseline random forest regression model.
          </div>
        </div>
        <div>
          <div class="side-block-title">Headline Takeaway</div>
          <div class="side-block-text">
            Review-related signals carry the strongest predictive weight. Genre, platform, price, and release timing
            still matter, but they appear secondary to score and engagement proxies.
          </div>
        </div>
      </aside>
    </section>

    <section class="metrics-grid">
      {cards_html}
    </section>

    <section class="section-grid">
      <article class="section">
        <h2 class="section-title">Genre Leaders</h2>
        <p class="section-note">Primary genres with at least 30 games, ranked by average PlayStation score.</p>
        <img class="chart" src="data:image/png;base64,{charts['genre_chart']}" alt="Genre leaderboard chart">
      </article>
      <article class="section">
        <h2 class="section-title">Platform Performance</h2>
        <p class="section-note">Platforms with enough volume to be comparable on average score.</p>
        <img class="chart" src="data:image/png;base64,{charts['platform_chart']}" alt="Platform leaderboard chart">
      </article>
      <article class="section">
        <h2 class="section-title">Price Positioning</h2>
        <p class="section-note">Budget versus premium listings, showing that price alone is not the strongest driver.</p>
        <img class="chart" src="data:image/png;base64,{charts['price_chart']}" alt="Price bucket chart">
      </article>
      <article class="section">
        <h2 class="section-title">Score Relationship</h2>
        <p class="section-note">Where critic scores exist, they generally move in the same direction as PlayStation scores.</p>
        <img class="chart" src="data:image/png;base64,{charts['scatter_chart']}" alt="Score relationship scatter plot">
      </article>
      <article class="section">
        <h2 class="section-title">Release Timing</h2>
        <p class="section-note">A quarter-by-quarter view for recent releases. Timing varies, but no single quarter dominates across years.</p>
        <img class="chart" src="data:image/png;base64,{charts['timing_chart']}" alt="Release timing heatmap">
      </article>
      <article class="section">
        <h2 class="section-title">Model Feature Importance</h2>
        <p class="section-note">The baseline model confirms that review-derived fields dominate the current signal mix.</p>
        <img class="chart" src="data:image/png;base64,{charts['importance_chart']}" alt="Feature importance chart">
      </article>
    </section>

    <section class="table-grid">
      <article class="table-panel">
        <h2 class="section-title">Price Bucket Summary</h2>
        <p class="section-note">A compact table that works well for screenshots or slide inserts.</p>
        {render_table(insight_table)}
      </article>
      <article class="table-panel">
        <h2 class="section-title">Top Model Signals</h2>
        <p class="section-note">Best-performing features from the baseline random forest model.</p>
        {render_table(feature_table)}
      </article>
    </section>

    <section class="table-grid" style="margin-top: 18px;">
      <article class="table-panel">
        <h2 class="section-title">Results</h2>
        <p class="section-note">
          The cleaned dataset contains <strong>{quality_report['clean_row_count']:,}</strong> rows after ETL. The
          model benchmark reached <strong>R² = {model_metrics['r2']:.3f}</strong>,
          <strong>MAE = {model_metrics['mae']:.3f}</strong>, and
          <strong>RMSE = {model_metrics['rmse']:.3f}</strong>.
        </p>
        <p class="section-note">
          This is a credible baseline for class reporting: it demonstrates a real analytics workflow, produces concrete
          insights, and leaves room for future refinement without overstating predictive power.
        </p>
      </article>
      <article class="table-panel">
        <h2 class="section-title">Limitations</h2>
        <p class="section-note">
          Metacritic fields are heavily missing, success is represented by score rather than sales, and platform-combined
          listings make exclusivity harder to define precisely. These constraints should be stated clearly in the final report.
        </p>
        <p class="section-note">
          Next steps: convert the report to PDF, record the 5-minute demo, and publish the project with this dashboard as a
          presentation artifact.
        </p>
      </article>
    </section>

    <div class="footer">
      Generated from the PlayStation Game Success pipeline. Recommended use: open in a browser, present directly, or capture sections for slides.
    </div>
  </main>
</body>
</html>
"""


def main() -> None:
    DASHBOARD_HTML_PATH.parent.mkdir(parents=True, exist_ok=True)
    html = build_dashboard_html()
    DASHBOARD_HTML_PATH.write_text(html, encoding="utf-8")
    print(f"Dashboard written to: {DASHBOARD_HTML_PATH}")


if __name__ == "__main__":
    main()
