# 3-Minute Demo Script

## Title

What Makes a PlayStation Game Successful?

## Script

Hello, my name is Frank Williams, and this project is called *What Makes a PlayStation Game Successful?*

In this project, I built an end-to-end data analytics pipeline using a public PlayStation games dataset from Kaggle. The goal was to move through the full analytics workflow: loading the data, cleaning it, storing the cleaned version, analyzing it, building a prediction model, and then presenting the results in a report notebook and dashboard.

The main question for the project was: what factors seem to influence a PlayStation game’s success? I also looked at supporting questions, including whether cheaper games perform better than expensive ones, which genres have the highest player satisfaction, whether release timing matters, and how platform listings compare.

The raw dataset includes information such as game title, price, release date, genre, publisher, platform, Metacritic scores, and PlayStation user scores. I kept the raw data separate from the cleaned data. The raw file is stored in the `data/raw` folder, and the processed outputs are stored in `data/processed`.

For the ETL stage, I cleaned several issues in the source file. I removed trailing empty columns, standardized missing values, converted prices and rating fields into numeric types, parsed release dates, and removed duplicate rows using game name, platform, and release date. I also documented the fields and transformations in a data dictionary so the process is reproducible and easy to explain.

For storage, I saved the cleaned dataset in two forms: a processed CSV file and a SQLite database. This was important because the project required cleaned data to be stored in a structured and queryable format.

For exploratory data analysis, I generated summary tables and visuals. The EDA showed that review-related fields were the strongest signals in the dataset. In particular, user review information had a stronger relationship with PlayStation score than price alone. Genre and platform also showed meaningful differences, while release timing had some variation but did not appear to be the dominant factor by itself.

For the applied task, I chose prediction. I built a baseline random forest regression model to predict `playstation_score`. The model used features such as price, release timing, genre, platform, and review variables. The baseline model achieved an R-squared value of about 0.279, with a mean absolute error of about 0.537. This means the model captures some useful signal, but there is still a large amount of variation left unexplained, so it should be treated as a solid baseline rather than a final model.

For reporting and visualization, I created two notebooks and a polished HTML dashboard. The first notebook is for analysis, the second is for presentation, and the dashboard is designed for slide-ready visuals and quick communication of the key findings.

I also added a cloud bonus path using Google BigQuery. The cleaned dataset was prepared for upload to BigQuery with a cloud-ready CSV export, schema file, and SQL queries. This extends the project beyond local files and notebooks by showing how the same processed data can be stored and queried in a cloud warehouse.

Overall, this project demonstrates the complete analytics pipeline from raw public data to cleaned storage, exploratory analysis, prediction, visualization, and cloud extension. The next steps would be to improve the prediction target, compare more models, and finalize the report and recorded demo for submission.

Thank you.

