from flask import Flask, render_template, jsonify
import json
import os
import subprocess

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/threats')
def get_threats():
    try:
        with open(os.path.join(BASE_DIR, 'alerts/threats.json')) as f:
            threats = json.load(f)
    except:
        threats = []
    return jsonify(threats)

@app.route('/api/logs')
def get_logs():
    try:
        with open(os.path.join(BASE_DIR, 'logs/raw_logs.json')) as f:
            logs = json.load(f)
    except:
        logs = []
    return jsonify(logs)

@app.route('/api/scan')
def run_scan():
    try:
        result = subprocess.run(
            ['python3', os.path.join(BASE_DIR, 'main.py')],
            capture_output=True,
            text=True,
            timeout=60
        )
        return jsonify({
            'status': 'success',
            'output': result.stdout
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'output': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
