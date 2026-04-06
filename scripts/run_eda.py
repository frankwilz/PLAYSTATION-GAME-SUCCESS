from __future__ import annotations

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
MPLCONFIG_DIR = PROJECT_ROOT / ".mplconfig"

MPLCONFIG_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPLCONFIG_DIR))
os.environ.setdefault("MPLBACKEND", "Agg")

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from playstation_success.config import FIGURES_DIR, TABLES_DIR
from playstation_success.data import load_clean_dataset
from playstation_success.eda import export_eda_bundle


def main() -> None:
    dataframe = load_clean_dataset()
    export_eda_bundle(dataframe, TABLES_DIR, FIGURES_DIR)
    print(f"EDA tables written to: {TABLES_DIR}")
    print(f"EDA figures written to: {FIGURES_DIR}")


if __name__ == "__main__":
    main()
