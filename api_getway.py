from flask import Flask, request
import requests
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# URL del servicio de ingestión
INGESTION_URL = "http://localhost:5001/ingest"

@app.route("/api/data", methods=["POST"])
def gateway():
    """
    Endpoint principal que recibe datos de sensores y los reenvía al servicio de ingestión.
    """
    data = request.get_json()
    logging.info(f"Gateway recibió: {data}")
    # Reenvía al servicio de ingestión
    resp = requests.post(INGESTION_URL, json=data)
    return ("", resp.status_code)

if __name__ == "__main__":
    app.run(port=5000)