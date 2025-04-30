from flask import Flask, jsonify
import requests

app = Flask(__name__)
HOST = "localhost"
HOST_PORT = 5000
INGESTION_URL = f"http://{HOST}:{HOST_PORT}/api/data"  
PORT = 5002 

@app.route('/analysis/summary', methods=['GET'])
def summary():
    resp = requests.get(INGESTION_URL)
    data = resp.json()
    if not data:
        return jsonify({'message': 'No hay datos'}), 204
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
    app.run(host="0.0.0.0", port=PORT)