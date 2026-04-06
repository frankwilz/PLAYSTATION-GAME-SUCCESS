from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from playstation_success.features import (
    CATEGORICAL_FEATURES,
    MODEL_FEATURES,
    NUMERIC_FEATURES,
    TARGET_COLUMN,
    make_modeling_frame,
)


@dataclass
class TrainingResult:
    pipeline: Pipeline
    metrics: dict[str, float]
    predictions: pd.DataFrame
    feature_importance: pd.DataFrame
    train_rows: int
    test_rows: int


def train_baseline_model(dataframe: pd.DataFrame) -> TrainingResult:
    modeling_frame = make_modeling_frame(dataframe)
    features = modeling_frame[MODEL_FEATURES]
    target = modeling_frame[TARGET_COLUMN]

    x_train, x_test, y_train, y_test = train_test_split(
        features, target, test_size=0.2, random_state=42
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numeric",
                Pipeline([("imputer", SimpleImputer(strategy="median"))]),
                NUMERIC_FEATURES,
            ),
            (
                "categorical",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("encoder", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                CATEGORICAL_FEATURES,
            ),
        ]
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "model",
                RandomForestRegressor(
                    n_estimators=300,
                    min_samples_leaf=2,
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    pipeline.fit(x_train, y_train)
    predictions = pipeline.predict(x_test)

    metrics = {
        "row_count": float(len(modeling_frame)),
        "train_rows": float(len(x_train)),
        "test_rows": float(len(x_test)),
        "mae": float(mean_absolute_error(y_test, predictions)),
        "rmse": float(np.sqrt(mean_squared_error(y_test, predictions))),
        "r2": float(r2_score(y_test, predictions)),
    }

    prediction_frame = x_test.copy()
    prediction_frame["actual_playstation_score"] = y_test.values
    prediction_frame["predicted_playstation_score"] = predictions
    prediction_frame["absolute_error"] = (
        prediction_frame["actual_playstation_score"]
        - prediction_frame["predicted_playstation_score"]
    ).abs()

    transformed_feature_names = pipeline.named_steps["preprocessor"].get_feature_names_out()
    importance_values = pipeline.named_steps["model"].feature_importances_
    feature_importance = (
        pd.DataFrame(
            {
                "feature": transformed_feature_names,
                "importance": importance_values,
            }
        )
        .sort_values("importance", ascending=False)
        .reset_index(drop=True)
    )

    return TrainingResult(
        pipeline=pipeline,
        metrics=metrics,
        predictions=prediction_frame.sort_values("absolute_error", ascending=False),
        feature_importance=feature_importance,
        train_rows=len(x_train),
        test_rows=len(x_test),
    )

