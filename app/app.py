import os
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.get('/health')
def health():
    return jsonify(status='ok')

@app.post('/telemetry')
def telemetry():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict) or not payload:
        return jsonify(error='expected a non-empty JSON object'), 400
    return jsonify(accepted=True, fields=sorted(payload.keys())), 202

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', '8080')))
