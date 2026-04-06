#!/usr/bin/env bash
set -euo pipefail

# Replace these values before running.
PROJECT_ID="your-project-id"
DATASET_ID="playstation_game_success"
TABLE_ID="cleaned_games"
LOCATION="US"
BUCKET_NAME="your-bucket-name"

CSV_PATH="cloud/bigquery/exports/cleaned_game_details_bigquery.csv"
GCS_URI="gs://${BUCKET_NAME}/cleaned_game_details_bigquery.csv"

echo "Creating dataset..."
bq --location="${LOCATION}" mk --dataset "${PROJECT_ID}:${DATASET_ID}" || true

echo "Uploading CSV to Cloud Storage..."
gcloud storage cp "${CSV_PATH}" "${GCS_URI}"

echo "Loading table into BigQuery..."
bq --location="${LOCATION}" load \
  --replace \
  --source_format=CSV \
  --skip_leading_rows=1 \
  "${PROJECT_ID}:${DATASET_ID}.${TABLE_ID}" \
  "${GCS_URI}" \
  "./cloud/bigquery/schema/cleaned_games_schema.json"

echo "Done. Table loaded: ${PROJECT_ID}:${DATASET_ID}.${TABLE_ID}"

