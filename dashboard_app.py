from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__, template_folder='templates', static_folder='static')
HOST = "localhost"
HOST_PORT = 5000
GATEWAY_URL = f"http://{HOST}:{HOST_PORT}/api"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/dashboard/data', methods=['GET'])
def dashboard_data():
    raw = requests.get(f"{GATEWAY_URL}/data").json()
    summary = requests.get(f"{GATEWAY_URL}/analysis/summary").json()
    corr = requests.get(f"{GATEWAY_URL}/analysis/correlation").json()
    return jsonify({'raw': raw, 'summary': summary, 'correlation': corr})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003)