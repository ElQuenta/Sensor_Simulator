from flask import Flask
import proxy  # nuestro módulo proxy

app = Flask(__name__)

# Rutas de ingestión y datos crudos
@app.route('/api/ingest', methods=['POST'])
def ingest():
    return proxy.forward_post('/ingest')

@app.route('/api/data', methods=['GET'])
def get_data():
    return proxy.forward_get('/data', cache_key='raw_data')

# Rutas de análisis
@app.route('/api/analysis/summary', methods=['GET'])
def summary():
    return proxy.forward_get('/analysis/summary', cache_key='summary')

@app.route('/api/analysis/correlation', methods=['GET'])
def correlation():
    return proxy.forward_get('/analysis/correlation', cache_key='correlation')

if __name__ == '__main__':
    app.run(port=5000)