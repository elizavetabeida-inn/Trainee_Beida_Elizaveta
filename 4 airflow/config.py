from pathlib import Path

DATA_DIR = Path("/opt/airflow/dags/data")

INPUT_FILE = DATA_DIR / "tiktok_google_play_reviews.csv"

STEP1_NO_NULLS = DATA_DIR / "step1_no_nulls.csv"
STEP2_SORTED = DATA_DIR / "step2_sorted.csv"

PROCESSED_FILE = DATA_DIR / "processed_data.csv"
