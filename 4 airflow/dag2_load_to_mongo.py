from datetime import datetime
import pandas as pd
import logging

from airflow.decorators import dag, task
from airflow import Dataset
from airflow.providers.mongo.hooks.mongo import MongoHook

PROCESSED_FILE = "/opt/airflow/dags/data/processed_data.csv"
processed_dataset = Dataset(PROCESSED_FILE)

@dag(
    dag_id = "dag2_load_to_mongo",
    schedule = [processed_dataset],
    start_date = datetime(2026, 10, 30),
    catchup = False,
    tags = ["etl", "sensor"]
)
def dag2_load_to_mongo():

    @task(task_id = "load_to_mongo")
    def load_to_mongo():
        df = pd.read_csv(PROCESSED_FILE)
        records = df.to_dict(orient = "records")

        hook = MongoHook(mongo_conn_id = "mongo_default")
        client = hook.get_conn()

        db = client["airflow_db"]
        collection = db["processed_data"]

        if records:
            collection.delete_many({})

            collection.insert_many(records)
            logging.info(
                "Successfully loaded %d documents to MongoDB!",
                len(records)
            )
        else:
            logging.warning("There is no data to load")

    load_to_mongo()

dag2_load_to_mongo()
            