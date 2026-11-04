from datetime import datetime
import os
import re
import pandas as pd

from airflow.decorators import dag, task, task_group
from airflow import Dataset

from config import (
    INPUT_FILE,
    STEP1_NO_NULLS,
    STEP2_SORTED,
    PROCESSED_FILE
)

processed_dataset = Dataset(str(PROCESSED_FILE))

@dag(
    dag_id = "dag1_process_data",
    schedule = None,
    start_date = datetime(2026, 10, 30),
    catchup = False,
    tags = ["etl", "sensor"]
)
def dag1_process_data():

    @task.sensor(
        task_id="wait_for_file",
        poke_interval=10,
        timeout=300,
        mode="reschedule"
    )
    def wait_for_file():
        """Wait for the input CSV file to appear"""
        if os.path.exists(INPUT_FILE):
            return True
        return False

    @task.branch(task_id = "check_file_empty")
    def check_file():
        """Check whether the input file is empty"""
        if os.path.getsize(INPUT_FILE) == 0:
            return "log_empty_file"
        
        return "processing_group.replace_nulls"

    @task.bash(task_id = "log_empty_file")
    def log_empty_file():
        """Branch 1: Log a warning if the input file is empty"""
        return f'echo "WARNING: File {INPUT_FILE} is empty!"'

    @task_group(group_id="processing_group")
    def data_processing_group():
        """Branch 2: Group all data processing tasks"""

        @task(task_id="replace_nulls")
        def replace_nulls():
            """Replace missing values and null strings with '-'"""
            df = pd.read_csv(INPUT_FILE)
            
            df = df.fillna("-")
            df = df.replace(["null", "NULL", "Null"], "-")

            df.to_csv(STEP1_NO_NULLS, index=False)

        @task(task_id="sort_by_date")
        def sort_by_date():
            """Sort reviews by created_date in ascending order"""
            
            df = pd.read_csv(STEP1_NO_NULLS)

            if "at" in df.columns:
                df = df.rename(columns={"at": "created_date"})

            df["created_date"] = pd.to_datetime(df["created_date"])
            df = df.sort_values(by="created_date")
            df.to_csv(STEP2_SORTED, index=False)

        @task(task_id="clean_content", outlets=[processed_dataset])
        def clean_content():
            """Remove unnecessary characters from review content"""

            df = pd.read_csv(STEP2_SORTED)

            def clean_text(text):
                if not isinstance(text, str):
                    return text
                return re.sub(r"[^\w\s.,!?:;\-\'\"()«»—–]", "", text).strip()
 
            df["content"] = df["content"].apply(clean_text)
            df.to_csv(PROCESSED_FILE, index=False)

        replace_nulls() >> sort_by_date() >> clean_content()

    wait_for_file() >> check_file() >> [log_empty_file(), data_processing_group()]

dag1_process_data()
