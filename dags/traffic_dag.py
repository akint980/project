from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add ingestion folder to Python path
#sys.path.append(os.path.join(os.path.dirname(__file__), "..", "ingestion"))
PROJECT_ROOT = "/home/adex/project"
INGESTION_PATH = os.path.join(PROJECT_ROOT, "ingestion")
sys.path.append(INGESTION_PATH)

from traffic_ingest import fetch_traffic_data

default_args = {
    "owner": "ade",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="traffic_ingestion_dag",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval="*/10 * * * *",
    catchup=False,
) as dag:

    run_traffic_ingestion = PythonOperator(
        task_id="run_traffic_ingestion",
        python_callable=fetch_traffic_data,
    )

    run_traffic_ingestion
