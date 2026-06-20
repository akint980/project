# project
##Houston Traffic & Weather Data Pipeline — Phase 1 (Ingestion Layer)
Overview
Phase 1 establishes the ingestion layer of the Houston Traffic & Weather Data Pipeline.
This phase focuses on collecting raw traffic and weather data at scheduled intervals using Python scripts orchestrated by Airflow.

No transformations, cleaning, or modeling occur in this phase.
The goal is to reliably capture raw data and store it in timestamped JSON files.

Project Structure (Phase 1)
project/
│
├── ingestion/
│   ├── traffic_ingest.py
│   └── weather_ingest.py
│
├── dags/
│   ├── traffic_dag.py
│   └── weather_dag.py
│
├── raw_data/
│   ├── traffic/
│   └── weather/
│
├── logs/
├── venv/
├── .gitignore
├── requirements.txt
└── README.md
Ingestion Scripts
Traffic Ingestion
Fetches live Houston traffic incident data

Saves raw JSON files to raw_data/traffic/

Uses timestamped filenames for traceability

Weather Ingestion
Fetches Houston weather forecast data from NOAA

Saves raw JSON files to raw_data/weather/

Uses timestamped filenames

Airflow Orchestration
Two DAGs are used:
-traffic_ingestion_dag

-weather_ingestion_dag

Each DAG:

-Runs every 10 minutes

-Calls the corresponding ingestion script

-Logs execution details

-Stores raw data in the appropriate folder

-Airflow provides monitoring, retries, and scheduling.
