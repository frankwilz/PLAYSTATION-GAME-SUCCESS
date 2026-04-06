-- Top platforms by average PlayStation score
SELECT
  platform,
  COUNT(*) AS game_count,
  ROUND(AVG(playstation_score), 3) AS avg_playstation_score
FROM `PROJECT_ID.DATASET_ID.cleaned_games`
GROUP BY platform
HAVING COUNT(*) >= 25
ORDER BY avg_playstation_score DESC
LIMIT 10;

-- Price bucket comparison
WITH price_buckets AS (
  SELECT
    CASE
      WHEN highest_price IS NULL THEN NULL
      WHEN highest_price <= 20 THEN 'budget'
      WHEN highest_price <= 40 THEN 'midrange'
      WHEN highest_price <= 60 THEN 'premium'
      ELSE 'collector'
    END AS price_bucket,
    playstation_score
  FROM `PROJECT_ID.DATASET_ID.cleaned_games`
)
SELECT
  price_bucket,
  COUNT(*) AS game_count,
  ROUND(AVG(playstation_score), 3) AS avg_playstation_score
FROM price_buckets
WHERE price_bucket IS NOT NULL
GROUP BY price_bucket
ORDER BY avg_playstation_score DESC;

-- Release year and quarter comparison
SELECT
  EXTRACT(YEAR FROM release_date) AS release_year,
  EXTRACT(QUARTER FROM release_date) AS release_quarter,
  COUNT(*) AS game_count,
  ROUND(AVG(playstation_score), 3) AS avg_playstation_score
FROM `PROJECT_ID.DATASET_ID.cleaned_games`
WHERE release_date IS NOT NULL
GROUP BY release_year, release_quarter
ORDER BY release_year, release_quarter;

