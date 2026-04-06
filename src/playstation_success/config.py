from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
LEGACY_DATASET_PATH = PROJECT_ROOT / "game_details.csv"
DATASET_PATH = RAW_DATA_DIR / "game_details.csv"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
TABLES_DIR = OUTPUTS_DIR / "tables"
FIGURES_DIR = OUTPUTS_DIR / "figures"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
CLEANED_CSV_PATH = PROCESSED_DATA_DIR / "cleaned_game_details.csv"
CLEANED_SQLITE_PATH = PROCESSED_DATA_DIR / "playstation_games.sqlite"
DATA_QUALITY_REPORT_PATH = PROCESSED_DATA_DIR / "data_quality_report.json"
DASHBOARD_DIR = PROJECT_ROOT / "dashboard"
DASHBOARD_HTML_PATH = DASHBOARD_DIR / "playstation_success_dashboard.html"
