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


'''def dbConnect(dbFile):
    sqlite3_conn = None
    try:
        sqlite3_conn = sqlite3.connect(dbFile)
        return sqlite3_conn
    except sqlite3.Error as e:
        print(e)
        if sqlite3_conn is not None:
            sqlite3_conn.close()


def insertPueDB(resultPUE):
    dbConn = dbConnect(dbFile)

    if dbConn is not None:
        c = dbConn.cursor()

        # Create table results
        c.execute('CREATE TABLE IF NOT EXISTS PUE' +
                  '(TIME INT,'
                  'realTimeTFE REAL,'
                  'realTimeIEE REAL,'
                  'realTimePUE REAL,'
                  'accTimeTFE REAL,'
                  'accTimeIEE REAL,'
                  'accTimePUE REAL,'
                  'realTimeTemp REAL)')

        sqlDF = pd.DataFrame.from_dict(resultPUE)
        sqlDF.to_sql(name='PUE', con=dbConn, if_exists='append',
                     index=False, schema='PUE')
        dbConn.close()


def createDB():
    dbConn = dbConnect(dbFile)

    if dbConn is not None:
        c = dbConn.cursor()

        # Create table results
        c.execute('CREATE TABLE IF NOT EXISTS PUE' +
                  '(TIME INT,'
                  'realTimeTFE REAL,'
                  'realTimeIEE REAL,'
                  'realTimePUE REAL,'
                  'accTimeTFE REAL,'
                  'accTimeIEE REAL,'
                  'accTimePUE REAL,'
                  'realTimeTemp REAL)')
        dbConn.close()


def removePueDB():
    dbConn = dbConnect(dbFile)
    if dbConn is not None:
        c = dbConn.cursor()
        c.execute('DELETE from PUE where DATETIME(TIME, ' + '"unixepoch", ' +
                  '"localtime") < DATETIME ("now", "localtime", "-7 day");')
        dbConn.commit()
        dbConn.close()

def retrievePueDB():
    dbConn = dbConnect(dbFile)
    if dbConn is not None:
        c = dbConn.cursor()
        try:
            removePueDB()
        except sqlite3.OperationalError:
            pass

    pastResultsDF = pd.read_sql_query('SELECT * from PUE', dbConn)
    dataframeRows = len(pastResultsDF.index)

    if pueCalcMethod == 2:
        try:
            if len(pastResultsDF) <= 1:
                avgPUE = 0
            elif len(pastResultsDF) > 1:
                with np.errstate(all='raise'):
                    try:
                        inlineDifference = (
                            pastResultsDF.iloc[-1][4]/10) - (pastResultsDF.iloc[0][4]/10)
                        pduDifference = (
                            pastResultsDF.iloc[-1][5]/10) - (pastResultsDF.iloc[0][5]/10)
                        avgPUE = inlineDifference / pduDifference
                    except FloatingPointError:
                        avgPUE = pastResultsDF['realTimePUE'].mean()

        except (IndexError, ValueError):
            avgPUE = pastResultsDF['realTimePUE'].mean()
    elif pueCalcMethod == 1:
        avgPUE = pastResultsDF['realTimePUE'].mean()
    return avgPUE, dataframeRows


def retrievePUE():
    dbConn = dbConnect(dbFile)

    if dbConn is not None:
        c = dbConn.cursor()
        pastResultsDF = pd.read_sql_query('SELECT * from PUE', dbConn)
    avgPUE = pastResultsDF['realTimePUE'].mean()
    return str(round(avgPUE, 2))


def realCoolingCapacity(ext_temp):
    realCoolingCap = coolingCapMultiplier * (ext_temp) + coolingCapOffset
    return realCoolingCap


def indexLookup(list, index1, index2):
    if index2 < len(list[index1]):
        return True
    else:
        return False
'''


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
    print(coordinateJson)
    return jsonify({'coordinates': coordinateJson})

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=8080, debug=True)
    #app.run(host='0.0.0.0', port=8080, debug=True)
    # set_start_method('spawn')
    p1 = Process(target=runFlask)
    p1.start()