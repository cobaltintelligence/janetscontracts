'''
server.py
Yuan Wang
'''

import sqlite3
from flask import Flask, request
import requests
import json




app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/receive', methods=['POST'])
def receive():
    data = request.get_json()

    conn = sqlite3.connect(sqlite_file)
	c = conn.cursor()

    ## END
    return 'received'

app.run(host='0.0.0.0')