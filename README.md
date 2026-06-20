# project
##Houston Traffic & Weather Data Pipeline — Phase 1 (Ingestion Layer)
Overview
Phase 1 establishes the ingestion layer of the Houston Traffic & Weather Data Pipeline.
This phase focuses on collecting raw traffic and weather data at scheduled intervals using Python scripts orchestrated by airflow

- Quick Start  
- Full Setup Guide  
- Troubleshooting   
# **📘 Project README (Full Version)**

## **🚀 Overview**
This project uses Apache Airflow to orchestrate two ingestion pipelines:

- **Traffic ingestion** (`traffic_ingestion_dag`)
- **Weather ingestion** (`weather_ingestion_dag`)

Each DAG runs every 10 minutes and writes JSON output into the `raw_data/` directory.

The system is designed for local development using:

- Airflow + SQLite + SequentialExecutor (dev only)
- Python ingestion scripts
- Absolute paths for reliable imports
- A clean project structure

---

## **📁 Project Structure**

```
project/
│
├── dags/
│   ├── traffic_dag.py
│   └── weather_dag.py
│
├── ingestion/
│   ├── traffic_ingest.py
│   └── weather_ingest.py
│
├── raw_data/
│   ├── traffic/
│   └── weather/
│
├── logs/
├── venv/
└── requirements.txt
```

---

## **⚙️ Airflow Configuration**

### **Set Airflow to use the project DAG folder**

Edit:

```
~/airflow/airflow.cfg
```

Update:

```
dags_folder = /home/ad/project/dags
```

Verify:

```
airflow config get-value core dags_folder
```

---

## **📌 Importing Ingestion Modules (Critical Fix)**

Airflow runs DAGs from `~/airflow`, not your project directory.  
Relative imports **will fail**.

Add this to the top of each DAG:

```python
import sys
import os

PROJECT_ROOT = "/home/ad/project"
INGESTION_PATH = os.path.join(PROJECT_ROOT, "ingestion")
sys.path.append(INGESTION_PATH)
```

Then import normally:

```python
from traffic_ingest import fetch_traffic_data
from weather_ingest import fetch_weather_data
```

---

## **🛠️ Ingestion Scripts**

### **Traffic Ingestion (`traffic_ingest.py`)**

```python
import requests
import json
from datetime import datetime
import os

BASE_DIR = "/home/ad/project"
OUTPUT_DIR = os.path.join(BASE_DIR, "raw_data/traffic")

def fetch_traffic_data():
    url = "https://traffic.houstontranstar.org/api/incidents_sample.json"
    response = requests.get(url)
    data = response.json()

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(os.path.join(OUTPUT_DIR, f"traffic_{timestamp}.json"), "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved traffic data at {timestamp}")
```

---

### **Weather Ingestion (`weather_ingest.py`)**

```python
import requests
import json
from datetime import datetime
import os

BASE_DIR = "/home/ad/project"
OUTPUT_DIR = os.path.join(BASE_DIR, "raw_data/weather")

def fetch_weather_data():
    lat, lon = 29.7604, -95.3698
    url = f"https://api.weather.gov/points/{lat},{lon}/forecast"

    headers = {"User-Agent": "(myweatherapp.com, contact@myweatherapp.com)"}
    response = requests.get(url, headers=headers)
    data = response.json()

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(os.path.join(OUTPUT_DIR, f"weather_{timestamp}.json"), "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved weather data at {timestamp}")
```

---

## **📅 DAG Definitions**

### **Traffic DAG**

```python
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
```

### **Weather DAG**

```python
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
```

---

## **🚀 Running Airflow**

### **Start Scheduler**

```
airflow scheduler
```

### **Start Webserver**

```
airflow webserver -p 8080
```

### **Restart Airflow after changes**

```
pkill -f airflow
```

Then restart both processes.

---

## **🧪 Troubleshooting**

### **1. DAG Import Errors**
Check:

**Browse → DAG Import Errors**

Common causes:

- Misspelled function names  
- Missing `requests` import  
- Wrong ingestion path  
- Writing to relative paths  
- DAG folder not updated  

---

### **2. Scheduler Not Running**
Fix:

```
pkill -f airflow
airflow scheduler
airflow webserver -p 8080
```

---

### **3. VS Code Terminal Cannot Find `airflow`**
Activate venv:

```
source venv/bin/activate
```

---

## **📐 Architecture Diagram (ASCII)**

```
                ┌──────────────────────────┐
                │        Airflow UI        │
                └─────────────┬────────────┘
                              │
                              ▼
                ┌──────────────────────────┐
                │       Scheduler          │
                └─────────────┬────────────┘
                              │
                ┌─────────────┴────────────┐
                │           DAGs            │
                │  traffic / weather        │
                └─────────────┬────────────┘
                              │
                ┌─────────────┴────────────┐
                │     Python Operators      │
                └─────────────┬────────────┘
                              │
                ┌─────────────┴────────────┐
                │     Ingestion Scripts     │
                │ traffic_ingest.py         │
                │ weather_ingest.py         │
                └─────────────┬────────────┘
                              │
                ┌─────────────┴────────────┐
                │        raw_data/          │
                │ traffic/   weather/       │
                └───────────────────────────┘
```

---

## **🎯 Quick Start**

1. Clone repo  
2. Create venv  
3. Install requirements  
4. Update `airflow.cfg`  
5. Start scheduler + webserver  
6. Turn DAGs ON  
7. Watch JSON files populate  


