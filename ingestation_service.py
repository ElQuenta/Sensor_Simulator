from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_PATH = 'sensor_data.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id TEXT,
            sent_timestamp TEXT,
            received_timestamp TEXT,
            temperature REAL,
            humidity REAL
        )
        '''
    )
    conn.commit()
    conn.close()

@app.route('/ingest', methods=['POST'])
def ingest():
    data = request.get_json()
    received_ts = datetime.utcnow().isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO readings(sensor_id, sent_timestamp, received_timestamp, temperature, humidity) VALUES (?, ?, ?, ?, ?)",
        (data['sensor_id'], data['timestamp'], received_ts, data['temperature'], data['humidity'])
    )
    conn.commit()
    conn.close()
    return ('', 201)

@app.route('/data', methods=['GET'])
def get_data():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT sensor_id, sent_timestamp, received_timestamp, temperature, humidity FROM readings")
    rows = c.fetchall()
    conn.close()
    result = [dict(sensor_id=r[0], sent_timestamp=r[1], received_timestamp=r[2], temperature=r[3], humidity=r[4]) for r in rows]
    return jsonify(result)

if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=5001)