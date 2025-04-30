# Ejecución del mini Proyecto
1. Ejecuta **ingestion_service.py** (puerto 5001)  
2. Ejecuta **processing_service.py** (puerto 5002)  
3. Ejecuta **api_gateway.py** (puerto 5000)  
4. Ejecuta **simulator.py** para generar datos  
5. Ejecuta **dashboard_app.py** (puerto 5003) para Visualizar los datos
6. Consume los endpoints vía Gateway:
   - `POST http://localhost:5000/api/ingest`
   - `GET  http://localhost:5000/api/data`
   - `GET  http://localhost:5000/api/analysis/summary`
   - `GET  http://localhost:5000/api/analysis/correlation`
