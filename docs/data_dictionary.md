# Data Dictionary

This data dictionary documents the cleaned dataset exported by the pipeline to `data/processed/cleaned_game_details.csv` and the SQLite table `cleaned_games`.

## Source Fields

| Field | Type | Description | Cleaning / Transformation |
| --- | --- | --- | --- |
| `game_name` | string | Game title shown in the source dataset | Trimmed whitespace |
| `highest_price` | float | Highest listed price for the game | Currency symbols removed, invalid price markers coerced to null |
| `release_date` | datetime | Game release date | Parsed from text to datetime with invalid dates set to null |
| `genre` | string | Genre label from source | Standardized slash spacing, `--` mapped to null |
| `publisher` | string | Publisher name | Trimmed whitespace, blanks mapped to null |
| `platform` | string | PlayStation platform or platform combination | Trimmed whitespace |
| `metacritic_score` | float | Metacritic critic score | Converted to numeric, invalid values mapped to null |
| `metacritic_rating_count` | float | Count of critic ratings on Metacritic | Converted to numeric |
| `metacritic_user_score` | float | Metacritic user score | Converted to numeric |
| `metacritic_user_rating_count` | float | Count of user ratings on Metacritic | Converted to numeric |
| `playstation_score` | float | PlayStation user score | Converted to numeric |
| `playstation_rating_count` | float | Count of PlayStation ratings | Converted to numeric |

## Feature Engineering Used In Analysis / Modeling

These fields are not stored in the cleaned CSV by default, but they are generated during analysis and modeling.

| Field | Type | Description |
| --- | --- | --- |
| `release_year` | float | Year extracted from `release_date` |
| `release_month` | float | Month extracted from `release_date` |
| `release_quarter` | float | Quarter extracted from `release_date` |
| `genre_primary` | string | First genre token from `genre` |
| `genre_count` | float | Number of genre tokens in `genre` |
| `is_multi_platform_listing` | float | `1` if the platform field contains multiple platforms, otherwise `0` |
| `has_metacritic` | float | `1` when a Metacritic score exists, otherwise `0` |
| `price_bucket` | string | Bucketed price label: `budget`, `midrange`, `premium`, or `collector` |

## Duplicate Rule

Rows are deduplicated on:

- `game_name`
- `platform`
- `release_date`

The first occurrence is retained.

