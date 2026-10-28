import os
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.get('/health/live')
def live():
    return jsonify(status='alive')

@app.get('/health/ready')
def ready():
    # This example API has no external dependency to check before serving traffic.
    return jsonify(status='ready')

@app.get('/health')
def health_alias():
    return live()

@app.post('/telemetry')
def telemetry():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict) or not payload:
        return jsonify(error='expected a non-empty JSON object'), 400
    return jsonify(accepted=True, fields=sorted(payload.keys())), 202

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', '8080')))
