import requests
import json
from datetime import datetime
import os

def fetch_traffic_data():
    url = "https://traffic.houstontranstar.org/api/incidents_sample.json"
    response = requests.get(url)
    data = response.json()

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    os.makedirs("raw_data/traffic", exist_ok=True)

    with open(f"raw_data/traffic/traffic_{timestamp}.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved traffic data at {timestamp}")

if __name__ == "__main__":
    fetch_traffic_data()
