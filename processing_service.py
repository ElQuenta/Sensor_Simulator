from flask import Flask, jsonify
import requests
#import sqlite3  # Conexión SQLite comentada
#import pandas as pd

app = Flask(__name__)
#DB_PATH = 'sensor_data.db'  # Ruta base de datos comentada

INGESTION_URL = "http://localhost:5001/data"  # Servicio de ingestión

@app.route('/analysis/summary', methods=['GET'])
def summary():
    """
    Obtiene datos crudos vía HTTP GET al servicio de ingestión y calcula estadísticas.
    """
    # Conexión SQLite previa (comentada):
    # conn = sqlite3.connect(DB_PATH)
    # df = pd.read_sql_query("SELECT temperature, humidity FROM readings", conn)
    # conn.close()

    # Solicitud HTTP al servicio de ingestión
    resp = requests.get(INGESTION_URL)
    data = resp.json()
    if not data:
        return jsonify({'message': 'No hay datos'}), 204

    # Cálculo de estadísticas con pandas
    # df = pd.DataFrame(data)
    # stats = df.agg(['mean','min','max']).to_dict()
    # para no depender de pandas:
    temps = [d['temperature'] for d in data]
    hums = [d['humidity'] for d in data]
    stats = {
        'temperature': {
            'mean': sum(temps)/len(temps),
            'min': min(temps),
            'max': max(temps)
        },
        'humidity': {
            'mean': sum(hums)/len(hums),
            'min': min(hums),
            'max': max(hums)
        }
    }
    return jsonify(stats)

@app.route('/analysis/correlation', methods=['GET'])
def correlation():
    """
    Obtiene datos crudos y calcula correlación entre temperatura y humedad.
    """
    # conn = sqlite3.connect(DB_PATH)
    # df = pd.read_sql_query("SELECT temperature, humidity FROM readings", conn)
    # conn.close()

    resp = requests.get(INGESTION_URL)
    data = resp.json()
    if not data:
        return jsonify({'message': 'No hay datos'}), 204

    # Cálculo de correlación sin pandas
    temps = [d['temperature'] for d in data]
    hums = [d['humidity'] for d in data]
    n = len(temps)
    mean_t = sum(temps)/n
    mean_h = sum(hums)/n
    cov = sum((temps[i]-mean_t)*(hums[i]-mean_h) for i in range(n)) / n
    var_t = sum((temps[i]-mean_t)**2 for i in range(n)) / n
    var_h = sum((hums[i]-mean_h)**2 for i in range(n)) / n
    corr_val = cov / ((var_t**0.5)*(var_h**0.5)) if var_t and var_h else None

    return jsonify({'temperature_humidity_correlation': corr_val})

if __name__ == '__main__':
    app.run(port=5002)