import time
import random
import requests
from datetime import datetime

def generate_sensor_data(sensor_id):
    return {
        "sensor_id": sensor_id,
        "timestamp": datetime.utcnow().isoformat(),
        "temperature": round(random.uniform(20.0, 30.0), 2),
        "humidity": round(random.uniform(30.0, 70.0), 2)
    }


def main():
    url = "http://localhost:5000/api/ingest"
    sensor_ids = ["sensor_1", "sensor_2", "sensor_3"]

    while True:
        for sensor_id in sensor_ids:
            payload = generate_sensor_data(sensor_id)
            try:
                resp = requests.post(url, json=payload)
                print(f"{datetime.utcnow().isoformat()} - Enviado: {payload} - Estado: {resp.status_code}")
            except Exception as e:
                print(f"Error al enviar datos: {e}")
        time.sleep(random.uniform(5, 10))

if __name__ == "__main__":
    main()