from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__, template_folder='templates', static_folder='static')
GATEWAY_URL = "http://localhost:5000"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/dashboard/data', methods=['GET'])
def dashboard_data():
    raw = requests.get(f"{GATEWAY_URL}/api/data").json()
    summary = requests.get(f"{GATEWAY_URL}/api/analysis/summary").json()
    corr = requests.get(f"{GATEWAY_URL}/api/analysis/correlation").json()
    return jsonify({'raw': raw, 'summary': summary, 'correlation': corr})

if __name__ == '__main__':
    app.run(port=5003)