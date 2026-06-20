from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add ingestion folder to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "ingestion"))

from weather_ingest import fetch_weather_data

default_args = {
    "owner": "ade",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="weather_ingestion_dag",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval="*/10 * * * *",
    catchup=False,
) as dag:

    run_weather_ingestion = PythonOperator(
        task_id="run_weather_ingestion",
        python_callable=fetch_weather_data,
    )

    run_weather_ingestion
