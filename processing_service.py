from flask import Flask, jsonify
import sqlite3
import pandas as pd

app = Flask(__name__)
DB_PATH = 'sensor_data.db'

@app.route('/analysis/summary', methods=['GET'])
def summary():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT temperature, humidity FROM readings", conn)
    conn.close()
    if df.empty:
        return jsonify({'message': 'No hay datos'}), 204
    stats = df.agg(['mean','min','max']).to_dict()
    return jsonify(stats)

@app.route('/analysis/correlation', methods=['GET'])
def correlation():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT temperature, humidity FROM readings", conn)
    conn.close()
    if df.empty:
        return jsonify({'message': 'No hay datos'}), 204
    corr_val = df['temperature'].corr(df['humidity'])
    return jsonify({'temperature_humidity_correlation': corr_val})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002)