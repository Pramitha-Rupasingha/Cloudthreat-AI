from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/threats')
def get_threats():
    try:
        with open('../alerts/threats.json') as f:
            threats = json.load(f)
    except:
        threats = []
    return jsonify(threats)

@app.route('/api/logs')
def get_logs():
    try:
        with open('../logs/raw_logs.json') as f:
            logs = json.load(f)
    except:
        logs = []
    return jsonify(logs)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
