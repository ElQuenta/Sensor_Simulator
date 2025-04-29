import time
import json
import random
import requests
from datetime import datetime

def generate_sensor_data(sensor_id):
    """
    Genera un diccionario con datos simulados de un sensor:
    - sensor_id: Identificador del sensor
    - timestamp: Fecha y hora UTC en formato ISO
    - temperature: Temperatura simulada (20.0 - 30.0 °C)
    - humidity: Humedad simulada (30.0 - 70.0 %)
    """
    return {
        "sensor_id": sensor_id,
        "timestamp": datetime.utcnow().isoformat(),
        "temperature": round(random.uniform(20.0, 30.0), 2),
        "humidity": round(random.uniform(30.0, 70.0), 2)
    }


def main():
    # URL del API Gateway
    url = "http://localhost:5000/api/data"
    # Lista de sensores a simular
    sensor_ids = ["sensor_1", "sensor_2", "sensor_3"]

    while True:
        for sensor_id in sensor_ids:
            payload = generate_sensor_data(sensor_id)
            try:
                response = requests.post(url, json=payload)
                print(f"{datetime.utcnow().isoformat()} - Enviado: {payload} - Estado: {response.status_code}")
            except Exception as e:
                print(f"Error de envío: {e}")
        # Espera aleatoria entre 5 y 10 segundos
        time.sleep(random.uniform(5, 10))


if __name__ == "__main__":
    main()