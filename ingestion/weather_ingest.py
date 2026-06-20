import requests
import json
from datetime import datetime
import os

def fetch_weather_data():
    lat, lon = 29.7604, -95.3698
    url = f"https://api.weather.gov/points/{lat},{lon}/forecast"

    headers = {"User-Agent": "(myweatherapp.com, contact@myweatherapp.com)"}

    response = requests.get(url, headers=headers)
    data = response.json()

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    os.makedirs("raw_data/weather", exist_ok=True)

    with open(f"raw_data/weather/weather_{timestamp}.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved weather data at {timestamp}")

if __name__ == "__main__":
    fetch_weather_data()
