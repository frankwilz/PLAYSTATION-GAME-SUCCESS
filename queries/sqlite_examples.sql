SELECT COUNT(*) AS cleaned_row_count
FROM cleaned_games;

SELECT platform,
       COUNT(*) AS game_count,
       ROUND(AVG(playstation_score), 3) AS avg_playstation_score
FROM cleaned_games
GROUP BY platform
HAVING COUNT(*) >= 25
ORDER BY avg_playstation_score DESC
LIMIT 10;

SELECT genre,
       COUNT(*) AS game_count,
       ROUND(AVG(playstation_score), 3) AS avg_playstation_score
FROM cleaned_games
WHERE genre IS NOT NULL
GROUP BY genre
ORDER BY game_count DESC
LIMIT 10;

