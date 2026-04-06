# Final Report

## Title

What Makes a PlayStation Game Successful?

## Question

This project studies which characteristics are associated with stronger PlayStation game performance. The working success measure is `playstation_score`, with supporting comparisons using review counts, Metacritic scores, genre, price, platform, and release timing.

## Dataset

The project uses a public PlayStation games dataset from Kaggle. The source data includes game title, release date, price, publisher, platform, and review-related fields. The raw file is stored in `data/raw/`, while the processed outputs are stored in `data/processed/`.

## Method

The pipeline follows five stages:

1. Load the public dataset from a reproducible local raw-data location.
2. Clean the data by standardizing missing values, converting types, parsing dates, fixing malformed price values, and removing duplicates.
3. Store the cleaned dataset in both CSV and SQLite formats.
4. Perform exploratory data analysis with summary statistics, missingness checks, distribution plots, and grouped comparisons.
5. Train a baseline random forest regression model to predict `playstation_score`.

## Tools Used

1. Python
2. Jupyter Notebook
3. SQLite
4. Google BigQuery

These satisfy the minimum requirement of using at least three technologies across the pipeline.

## Results

### Data Quality

- The raw dataset contains substantial missingness in the Metacritic fields.
- Price values required cleaning because some records included malformed non-numeric values.
- Duplicate records were removed using a `game_name + platform + release_date` key.

### EDA Findings

- User review signals appear to be the strongest indicators of PlayStation score where they exist.
- Genre and platform differences are visible in grouped summaries.
- Price has some relationship with score, but it is weaker than review-related features.
- Release timing shows variation across years and quarters, but the pattern is not strong enough on its own to explain success.

### Answers To The Analytics Questions

**Q1. What factors influence a PlayStation game's success?**

The strongest factors in this dataset are review-related variables, especially `metacritic_score` and `metacritic_user_score`. In the correlation analysis, `metacritic_score` had a correlation of about `0.457` with `playstation_score`, and `metacritic_user_score` had a correlation of about `0.415`. The baseline model also supports this result, with `metacritic_user_score` appearing as the single most important feature. Release timing and genre add some predictive signal, but price shows almost no direct linear relationship with PlayStation score in this dataset.

**Q2. Do cheaper PlayStation games perform better than expensive games?**

Cheaper games do not clearly perform worse, and in this dataset the `budget` price bucket actually had the highest average PlayStation score at about `4.44`. The other observed buckets were also close, with `midrange` around `4.38`, `premium` around `4.38`, and `collector` around `4.24`. This suggests that lower-priced games can perform just as well or better on user score, although price is not the strongest driver of success overall.

**Q3. Which genres have the highest player satisfaction?**

If very small genres are included, `Quiz` and `Brain training` rank highest, but those categories have relatively few games. Using a more stable cutoff of at least `100` games, the strongest genre in this dataset is `Role playing games`, with an average PlayStation score of about `4.38`. After that, the highest-scoring larger genres are `Casual`, `Adventure`, `Shooter`, and `Fighting`. This means role-playing and adventure-oriented categories appear to generate the strongest player satisfaction in the cleaned dataset.

**Q4. Does release timing affect a game's success?**

Release timing appears to matter somewhat, but not as strongly as review signals. By quarter, `Q3` has the highest average PlayStation score at about `4.21`, followed very closely by `Q2` and `Q1`, while `Q4` is slightly lower at about `4.18`. By year, more recent years such as `2023` and `2022` show stronger average scores than several earlier years. Overall, timing has a measurable effect, but it is a secondary factor rather than a dominant explanation of success.

**Q5. Do PlayStation exclusive games perform better than non-exclusive games?**

The dataset does not directly label exclusivity, so this question was approximated by comparing `single-platform listings` and `multi-platform listings`. The difference is very small: multi-platform listings averaged about `4.230`, while single-platform listings averaged about `4.227`. Based on this approximation, there is no strong evidence in the current dataset that one listing type clearly outperforms the other on PlayStation score. A stronger answer would require external metadata that explicitly identifies exclusives.

### Prediction Baseline

The baseline random forest regression model produced:

- MAE: `0.537`
- RMSE: `2.982`
- R²: `0.279`

This means the model captures some signal, but a large share of variation remains unexplained. It is a reasonable baseline rather than a final production-quality model.

## Cloud Bonus Extension

As an optional cloud extension, the cleaned dataset was prepared for Google BigQuery. The cloud workflow uses:

1. local ETL to produce the cleaned dataset
2. a BigQuery-ready CSV export and schema
3. upload to Google Cloud Storage
4. loading into a BigQuery table for cloud SQL analysis

This extends the project beyond local notebooks and files by adding a managed cloud warehouse layer. The repository includes the BigQuery assets and documentation in:

- `cloud/bigquery/`
- `docs/cloud_bonus_bigquery.md`

## Limitations

- Missing values are heavy in critic-related columns.
- The success target is defined using score rather than sales or revenue.
- The dataset may not represent the full PlayStation catalog evenly.
- Platform-combined listings make exclusivity difficult to determine precisely without external metadata.

## Changes from proposal
- Tableau to html for dashboard

## Next Steps

1. Reframe success as a classification task such as high-rated vs not high-rated.
2. Compare multiple model families and stronger validation strategies.
3. Export the dashboard and report into final submission formats such as PDF or slides.
4. Add external metadata if exclusivity must be measured more precisely.
