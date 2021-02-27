from flask import Flask, render_template, jsonify, request, json
from datetime import datetime, timedelta
from multiprocessing import Process, freeze_support, set_start_method
import sqlite3
import pandas as pd
import statistics
import time
import importlib
import os
import subprocess
import numpy as np
from mapbox import Uploader
import geocoder
import mapbox
import json

dbFile = 'pue.db'

pueDictList = []
retrieveSqlTracker = 0
insertSql = 0

app = Flask(__name__)

def runFlask():
    app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)

#createDB()

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/_get_data/', methods=['GET', 'POST'])
def get_data():
    with open('gdf.json', 'r') as f:
        coordinateJson = json.load(f)
    f.close()
    return jsonify({'coordinates': coordinateJson})

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=8080, debug=True)
    #app.run(host='0.0.0.0', port=8080, debug=True)
    # set_start_method('spawn')
    p1 = Process(target=runFlask)
    p1.start()