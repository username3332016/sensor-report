"""Génère data/sample_readings.csv (données fictives, graine fixée pour être reproductible)."""
import csv
import random
from datetime import datetime, timedelta

random.seed(42)
start = datetime(2026, 11, 1, 0, 0)
sensors = {"salon": 20.0, "cuisine": 22.0, "garage": 14.0}

with open("data/sample_readings.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "sensor_id", "temperature", "humidity"])
    for hour in range(72):  # 3 jours de mesures, une par heure
        moment = start + timedelta(hours=hour)
        for name, base in sensors.items():
            temp = round(base + random.gauss(0, 0.8), 1)
            hum = round(50 + random.gauss(0, 4), 1)
            # quelques valeurs aberrantes et manquantes pour tester le programme
            if hour == 30 and name == "cuisine":
                temp = 45.0
            if hour == 50 and name == "garage":
                hum = ""
            writer.writerow([moment.strftime("%Y-%m-%d %H:%M:%S"), name, temp, hum])
