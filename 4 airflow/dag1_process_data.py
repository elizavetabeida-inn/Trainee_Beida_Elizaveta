from datetime import datetime
import os
import re
import pandas as pd

from airflow.decorators import dag, task, task_group
from airflow import Dataset

INPUT_FILE = "/opt/airflow/dags/data/tiktok_google_play_reviews.csv"
STEP1_FILE = "/opt/airflow/dags/data/step1_no_nulls.csv"
STEP2_FILE = "/opt/airflow/dags/data/step2_sorted.csv"
PROCESSED_FILE = "/opt/airflow/dags/data/processed_data.csv"

processed_dataset = Dataset(PROCESSED_FILE)

@dag(
    dag_id = "dag1_process_data",
    schedule = None,
    start_date = datetime(2026, 10, 30),
    catchup = False,
    tags = ["etl", "sensor"]
)
def dag1_process_data():

    # Sensor that reacts to the appearance of data file in the folder
    @task.sensor(
        task_id="wait_for_file",
        poke_interval=10,
        timeout=300,
        mode="reschedule"
    )
    def wait_for_file():
        if os.path.exists(INPUT_FILE):
            return True
        return False

    # Checks if the file is empty or not
    @task.branch(task_id = "check_file_empty")
    def check_file():
        if os.path.getsize(INPUT_FILE) == 0:
            return "log_empty_file"
        
        return "processing_group.replace_nulls"

    # Branch 1: file is empty
    @task.bash(task_id = "log_empty_file")
    def log_empty_file():
        return f'echo "WARNING: File {INPUT_FILE} is empty!"'

    # Branch 2: file is fine
    @task_group(group_id="processing_group")
    def data_processing_group():

        # Task 1: Replace all "null" values with "-"
        @task(task_id="replace_nulls")
        def replace_nulls():
            df = pd.read_csv(INPUT_FILE)
            
            df = df.fillna("-").replace(
                to_replace=r"(?i)^null$", value="-", regex=True
            )
            df.to_csv(STEP1_FILE, index=False)

        # Task 2: Sort data by created_date
        @task(task_id="sort_by_date")
        def sort_by_date():
            df = pd.read_csv(STEP1_FILE)

            if "at" in df.columns:
                df = df.rename(columns={"at": "created_date"})

            df["created_date"] = pd.to_datetime(df["created_date"])
            df = df.sort_values(by="created_date")
            df.to_csv(STEP2_FILE, index=False)

        # Task 3: Remove all unnecessary characters from the content column, leaving only text and punctuation marks
        @task(task_id="clean_content", outlets=[processed_dataset])
        def clean_content():
            df = pd.read_csv(STEP2_FILE)

            def clean_text(text):
                if not isinstance(text, str):
                    return text
                return re.sub(r"[^\w\s.,!?:;\-\'\"()«»—–]", "", text).strip()
 
            df["content"] = df["content"].apply(clean_text)
            df.to_csv(PROCESSED_FILE, index=False)

        replace_nulls() >> sort_by_date() >> clean_content()

    # Setting dependencies
    wait_for_file() >> check_file() >> [log_empty_file(), data_processing_group()]

dag1_process_data()
