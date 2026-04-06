-- Replace PROJECT_ID, DATASET_ID, TABLE_ID, and GCS_URI before running.
LOAD DATA OVERWRITE `PROJECT_ID.DATASET_ID.TABLE_ID`
(
  game_name STRING,
  highest_price FLOAT64,
  release_date DATE,
  genre STRING,
  publisher STRING,
  platform STRING,
  metacritic_score FLOAT64,
  metacritic_rating_count FLOAT64,
  metacritic_user_score FLOAT64,
  metacritic_user_rating_count FLOAT64,
  playstation_score FLOAT64,
  playstation_rating_count FLOAT64
)
FROM FILES (
  format = 'CSV',
  uris = ['GCS_URI'],
  skip_leading_rows = 1
);

