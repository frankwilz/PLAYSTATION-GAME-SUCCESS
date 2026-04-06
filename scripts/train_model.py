from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from playstation_success.config import ARTIFACTS_DIR
from playstation_success.data import load_clean_dataset
from playstation_success.model import train_baseline_model


def main() -> None:
    dataframe = load_clean_dataset()
    result = train_baseline_model(dataframe)

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(result.pipeline, ARTIFACTS_DIR / "baseline_random_forest.joblib")
    result.feature_importance.to_csv(
        ARTIFACTS_DIR / "feature_importance.csv", index=False
    )
    result.predictions.to_csv(ARTIFACTS_DIR / "test_predictions.csv", index=False)
    with open(ARTIFACTS_DIR / "model_metrics.json", "w", encoding="utf-8") as output_file:
        json.dump(result.metrics, output_file, indent=2)

    print(json.dumps(result.metrics, indent=2))
    print(f"Artifacts written to: {ARTIFACTS_DIR}")


if __name__ == "__main__":
    main()
