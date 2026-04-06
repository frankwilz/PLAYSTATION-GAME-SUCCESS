# Cloud Bonus: BigQuery

This document explains how to use Google BigQuery as the cloud bonus component for the project.

## Why BigQuery Fits This Project

BigQuery adds a meaningful cloud layer because it turns the cleaned dataset into a managed, queryable cloud warehouse rather than just a local file. That satisfies the bonus requirement more credibly than simple file hosting.

Cloud role in this project:

1. Store the cleaned dataset in Google Cloud Storage and BigQuery.
2. Query the data in a cloud warehouse using SQL.
3. Use cloud-hosted results as evidence of a cloud analytics workflow in the final report and demo.

## Proposed Cloud Architecture

1. Run the local ETL pipeline.
2. Export the cleaned dataset for BigQuery.
3. Upload the exported CSV to Google Cloud Storage.
4. Load the file into a BigQuery table named `cleaned_games`.
5. Run analysis queries directly in BigQuery.
6. Reference the cloud dataset and queries in the final report and presentation.

## Local Preparation

Generate the cloud-ready CSV and schema:

```bash
python3 scripts/prepare_bigquery_assets.py
```

This creates:

- `cloud/bigquery/exports/cleaned_game_details_bigquery.csv`
- `cloud/bigquery/schema/cleaned_games_schema.json`

## BigQuery Steps

### 1. Create the dataset

Use the SQL in:

- `cloud/bigquery/sql/create_dataset.sql`

### 2. Upload the cleaned CSV to Cloud Storage

Use:

```bash
gcloud storage cp cloud/bigquery/exports/cleaned_game_details_bigquery.csv gs://YOUR_BUCKET/cleaned_game_details_bigquery.csv
```

### 3. Load the CSV into BigQuery

You can use either:

- `cloud/bigquery/sql/load_from_gcs.sql`
- `cloud/bigquery/load_commands.sh`

### 4. Run cloud analysis

Use the reusable queries in:

- `cloud/bigquery/sql/analysis_queries.sql`

## What To Show In The Demo

- BigQuery dataset and table created in Google Cloud
- Cloud Storage object containing the cleaned CSV
- At least one SQL query run in BigQuery
- A short explanation that the cleaned dataset exists in both local storage and cloud warehouse form

## How To Describe It In The Report

Suggested wording:

> As an optional cloud extension, the cleaned dataset was loaded into Google BigQuery after local ETL. This enabled cloud-based storage and SQL analysis on the processed PlayStation games data, extending the project beyond local notebooks and files.

## Official References

The implementation path here is based on official Google Cloud BigQuery documentation:

- Create datasets: https://cloud.google.com/bigquery/docs/datasets
- Batch loading data and local-file loading options: https://cloud.google.com/bigquery/docs/batch-loading-data
- Introduction to loading data: https://cloud.google.com/bigquery/docs/loading-data
- Loading CSV data from Cloud Storage: https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv

## Current Status

The repository now contains all local artifacts needed to execute the BigQuery bonus path. Actual cloud execution still requires:

- a Google Cloud project
- BigQuery enabled
- a Cloud Storage bucket
- authenticated `gcloud` and `bq` access

