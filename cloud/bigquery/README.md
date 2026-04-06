# BigQuery Bonus Path

This folder contains the reproducible assets needed to use Google BigQuery as the cloud bonus component for the project.

## What This Adds

- cloud storage and queryable warehouse usage through BigQuery
- a cloud-ready export of the cleaned dataset
- an explicit BigQuery schema
- reusable SQL queries for analysis inside BigQuery

## Files

- `exports/cleaned_game_details_bigquery.csv`
- `schema/cleaned_games_schema.json`
- `sql/create_dataset.sql`
- `sql/load_from_gcs.sql`
- `sql/analysis_queries.sql`
- `load_commands.sh`

## Workflow

1. Create a Google Cloud project and enable BigQuery.
2. Create a dataset in BigQuery.
3. Upload the cleaned CSV to a Cloud Storage bucket.
4. Load the CSV from Cloud Storage into a BigQuery table.
5. Run the analysis queries in `sql/analysis_queries.sql`.
6. Cite the cloud architecture and results in the final report.

