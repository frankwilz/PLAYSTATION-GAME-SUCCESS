# 5-Minute Demo Outline

## 1. Project Goal

- Introduce the question: what makes a PlayStation game successful?

## 2. Dataset

- Show the public Kaggle source
- Mention key fields: price, release date, genre, platform, and review metrics

## 3. Pipeline

- Raw data in `data/raw/`
- Cleaning and ETL in `src/playstation_success/data.py`
- Cleaned outputs in CSV and SQLite
- EDA exports in `outputs/`
- Baseline model artifacts in `artifacts/`

## 4. Findings

- Missingness is high for Metacritic variables
- Review-related variables are strongest signals
- Genre, price, and release timing show secondary effects

## 5. Model

- Show baseline metrics
- Explain that the model is a first benchmark, not a final optimized system

## 6. Limitations And Next Steps

- Missing data
- Definition of success
- Opportunity to improve with better targets and dashboarding

## 7. Cloud Bonus

- Show the BigQuery bonus package in `cloud/bigquery/`
- Explain that the cleaned dataset can be loaded into Google BigQuery for cloud SQL analysis
- Mention that this adds cloud storage and warehouse querying beyond the local pipeline
