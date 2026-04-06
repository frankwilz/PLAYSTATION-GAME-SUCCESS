from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from playstation_success.config import (
    CLEANED_CSV_PATH,
    CLEANED_SQLITE_PATH,
    DATA_QUALITY_REPORT_PATH,
)
from playstation_success.data import export_clean_data_assets


def main() -> None:
    report = export_clean_data_assets()
    print(f"Cleaned CSV written to: {CLEANED_CSV_PATH}")
    print(f"SQLite database written to: {CLEANED_SQLITE_PATH}")
    print(f"Data quality report written to: {DATA_QUALITY_REPORT_PATH}")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
