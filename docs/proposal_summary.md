# Proposal Summary

This file captures the approved project direction reflected in the proposal screenshots supplied with the project.

## Dataset

- Dataset: PlayStation Games Info
- Dataset link: `https://www.kaggle.com/datasets/isaacmenard/playstation-games-info-2152025`
- License shown on Kaggle: `CC BY-SA 4.0`
- Description: PlayStation game records including title, price, release date, genre, publisher, platform, and available review metrics.

## Analytics Questions

1. What factors influence a PlayStation game's success?
2. Do cheaper PlayStation games perform better than expensive games?
3. Which genres have the highest player satisfaction?
4. Does release timing affect a game's success?
5. Do PlayStation exclusive or platform-specific listings perform better than multi-platform listings?

## Chosen Applied Task

- Prediction

Primary target used in the current baseline:

- `playstation_score`

## Planned Tools

1. Python
   - ETL, EDA, feature engineering, and predictive modeling
2. Jupyter Notebook
   - Analysis workflow and report presentation
3. SQLite
   - Storage of the cleaned dataset for queryable analysis

## Risks And Ethics

- Missingness is substantial in the Metacritic fields, which can bias results.
- The dataset may overrepresent certain platforms, publishers, or genres.
- Correlation should not be presented as causation.
- The dataset should be used in line with Kaggle dataset terms and platform terms.
