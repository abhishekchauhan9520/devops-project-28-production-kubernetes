from flask import Flask, jsonify
import os, time

app = Flask(__name__)
STARTED_AT = time.time()
VERSION = os.getenv('APP_VERSION', '1.0.0')

@app.get('/')
def root():
    return jsonify(service='production-kubernetes-demo', version=VERSION)

@app.get('/healthz')
def healthz():
    return jsonify(status='ok', version=VERSION)

@app.get('/readyz')
def readyz():
    return jsonify(status='ready', uptime_seconds=round(time.time() - STARTED_AT, 2))
