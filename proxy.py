from flask import request, jsonify
import requests
import time

# Configuración de servicios internos
INGEST_URL = "http://localhost:5001"
PROCESS_URL = "http://localhost:5002"

# Cache en memoria {key: (timestamp, data)}
cache = {}
TTL = 30  # segundos

def get_cache(key):
    entry = cache.get(key)
    if entry and (time.time() - entry[0] < TTL):
        return entry[1]
    cache.pop(key, None)
    return None

def set_cache(key, data):
    cache[key] = (time.time(), data)

def forward_post(path):
    cache.clear()
    resp = requests.post(f"{INGEST_URL}{path}", json=request.get_json())
    return jsonify(request.get_json(), resp.status_code)

def forward_get(path, cache_key=None):
    if cache_key:
        data = get_cache(cache_key)
        if data is not None:
            print(f"Cache hit for {cache_key}")
            return jsonify(data)
        print(f"Cache miss for {cache_key}")
    resp = requests.get(f"{INGEST_URL}{path}" if '/analysis' not in path else f"{PROCESS_URL}{path}")
    data = resp.json()
    if cache_key:
        set_cache(cache_key, data)
    return jsonify(data)