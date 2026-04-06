# PlayStation Game Success Analysis

This repository implements an end-to-end analytics pipeline around a public PlayStation games dataset. It covers:

- data loading and ETL
- cleaned-data storage
- exploratory data analysis (EDA)
- a prediction task
- reporting artifacts and notebooks

# Notice GenAI was used in project

## Dataset

Source dataset:

- Kaggle: `https://www.kaggle.com/datasets/isaacmenard/playstation-games-info-2152025`
- License shown on dataset page: `CC BY-SA 4.0`

Current local raw-data location:

- `data/raw/game_details.csv`

Legacy local copy still supported by the loader:

- `game_details.csv`

Dataset use should follow Kaggle platform terms and the dataset page terms shown for the source.

Reproducible download step with the Kaggle CLI:

```bash
kaggle datasets download -d isaacmenard/playstation-games-info-2152025 -p data/raw --unzip
```

This requires a configured Kaggle API token and acceptance of the dataset terms on Kaggle.

## Analytics Questions

1. What factors influence a PlayStation game's success?
2. Do cheaper PlayStation games perform better than expensive games?
3. Which genres have the highest player satisfaction?
4. Does release timing affect a game's success?
5. Do platform-specific or multi-platform listings perform differently?

## Applied Task

- Prediction

The current baseline predicts `playstation_score`.

## Tools Used

This project uses at least three technologies across the pipeline:

1. Python
2. Jupyter Notebook
3. SQLite

Optional presentation tooling can be added later, but the minimum requirement is already satisfied.

## Project Structure

```text
.
├── data
│   ├── raw
│   └── processed
├── docs
├── notebooks
├── outputs
├── queries
├── requirements.txt
├── scripts
│   ├── prepare_data_assets.py
│   ├── prepare_bigquery_assets.py
│   ├── run_eda.py
│   ├── train_model.py
│   └── build_dashboard.py
├── dashboard
├── cloud
└── src
    └── playstation_success
        ├── config.py
        ├── data.py
        ├── eda.py
        ├── features.py
        └── model.py
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Reproducible Pipeline

Prepare cleaned storage assets:

```bash
PYTHONPATH=src python3 scripts/prepare_data_assets.py
```

This step writes:

- `data/processed/cleaned_game_details.csv`
- `data/processed/playstation_games.sqlite`
- `data/processed/data_quality_report.json`

Run EDA exports:

```bash
PYTHONPATH=src python3 scripts/run_eda.py
```

Train the baseline model:

```bash
PYTHONPATH=src python3 scripts/train_model.py
```

Build the polished presentation dashboard:

```bash
PYTHONPATH=src python3 scripts/build_dashboard.py
```

Prepare BigQuery cloud bonus assets:

```bash
python3 scripts/prepare_bigquery_assets.py
```

Open the notebooks:

```bash
jupyter notebook notebooks/playstation_success_analysis.ipynb
jupyter notebook notebooks/playstation_success_report.ipynb
```

## Outputs

EDA exports are written to:

- `outputs/tables/`
- `outputs/figures/`

Model artifacts are written to:

- `artifacts/baseline_random_forest.joblib`
- `artifacts/model_metrics.json`
- `artifacts/feature_importance.csv`
- `artifacts/test_predictions.csv`

Cleaned storage outputs are written to:

- `data/processed/cleaned_game_details.csv`
- `data/processed/playstation_games.sqlite`
- `data/processed/data_quality_report.json`

Presentation dashboard output:

- `dashboard/playstation_success_dashboard.html`

Cloud bonus outputs are written to:

- `cloud/bigquery/exports/`
- `cloud/bigquery/schema/`
- `cloud/bigquery/sql/`

## ETL Notes

The ETL pipeline currently handles:

- trailing empty columns in the source CSV
- missing markers such as `--` and blank strings
- numeric type conversion for review and rating counts
- malformed price strings
- date parsing for `release_date`
- duplicate removal using `game_name`, `platform`, and `release_date`

Outliers are reviewed during EDA rather than dropped automatically. That choice is intentional because expensive collector editions and low-priced titles can be valid observations for this dataset.

Field descriptions and transformations are documented in:

- `docs/data_dictionary.md`

## Reporting Artifacts

- Proposal summary: `docs/proposal_summary.md`
- Final report draft: `docs/final_report.md`
- Demo outline: `docs/demo_outline.md`
- Cloud bonus guide: `docs/cloud_bonus_bigquery.md`
- Presentation notebook: `notebooks/playstation_success_report.ipynb`

## SQLite Usage

The cleaned dataset is also stored in SQLite so it is queryable outside pandas.

Example queries are included in:

- `queries/sqlite_examples.sql`

Example command:

```bash
sqlite3 data/processed/playstation_games.sqlite < queries/sqlite_examples.sql
```

## Current Modeling Choice

The initial baseline predicts `playstation_score` as a regression problem. That choice was influenced by EDA and missingness checks: `playstation_score` is available for substantially more rows than the Metacritic fields, so it provides a better starting target for a repeatable baseline.

## Remaining Submission Items Outside The Repo

Two rubric items still require a manual submission step outside local code generation:

1. export `docs/final_report.md` or the report notebook to PDF for final submission
2. publish the project and add the final public link
