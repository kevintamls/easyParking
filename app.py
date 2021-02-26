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

'''@app.route('/_get_data/', methods=['GET', 'POST'])
def _get_data():
    global insertSql
    global pueDictList
    oidData = []
    powerData = []
    realTimePowerData = []
    # Design Power Capacity Definition
    try:
        if idcModel == 1:
            designCoolCap = 3.0
            idcModelName = 'mini Duo'
        if idcModel == 2:
            designCoolCap = 3.0
            idcModelName = 'air'
        if idcModel == 3:
            designCoolCap = 1.5
            idcModelName = 'nano'
        if idcModel == 4:
            designCoolCap = 1.6
            idcModelName = 'edge'
        if idcModel == 5:
            designCoolCap = 2.6
            idcModelName = 'edge'
    except ValueError:
        designCoolCap = 0.0
        idcModelName = 'mini'

    try:
        if rackConfig == 1:
            idcRackConfig = '1 + 0'
        if rackConfig == 2:
            idcRackConfig = '1 + 1'
        if rackConfig == 3:
            idcRackConfig = '1 + 2'
    except ValueError:
        idcRackConfig = 'Error'

    session = Session(hostname=snmphost + ':' + str(snmpport), community=snmpcomm, version=1)
    for i in range(0, len(oids)):
        resultsList = []
        for element in oids[i]:
            try:
                resultsList.append(int(session.get(element).value))
            except (easysnmp.EasySNMPError, SystemError):
                resultsList.append([]) # Change logic here
        oidData.append(resultsList)

    #print(powerConnList)

    for list in powerConnList:
        if len(list) < 1:
            powerData.append([])
            realTimePowerData.append([])
        else:
            powerSession = Session(hostname=list[0] + ':' + str(list[1]), community=list[2], version=1)
            try:
                powerData.append(int(powerSession.get(list[3]).value))
            except (easysnmp.EasySNMPError, SystemError):
                powerData.append([])
            try:
                #print(int(powerSession.get(list[4]).value))
                realTimePowerData.append(int(powerSession.get(list[4]).value))
            except (easysnmp.EasySNMPError, SystemError, ValueError):
                realTimePowerData.append([])

        #print(powerData)
        #print(realTimePowerData)

    # IT Power and Efficiency Calculation
    inlinePowerKW = (powerData[0] if type(powerData[0]) == int else 0) / 10 + \
        (sum(i for i in powerData[1:4] if type(i) == int)/10)
    totalPduPowerKW = sum(i for i in powerData[4:] if type(i) == int) / 10

    totalInlinePower = sum(i for i in realTimePowerData[:4] if type(i) == int)
    rack1PduPower = sum(i for i in realTimePowerData[4:6] if type(i) == int)
    rack2PduPower = sum(i for i in realTimePowerData[6:8] if type(i) == int)
    rack3PduPower = sum(i for i in realTimePowerData[8:] if type(i) == int)
    totalPduPower = rack1PduPower + rack2PduPower + rack3PduPower
    pue = (totalInlinePower+tfpOffset) / totalPduPower+itPowerOffset if tfpOffset and itPowerOffset == int \
        else totalInlinePower / totalPduPower



    # Entry into SQL iterator
    try:
        avgPUE, dataframeLength = retrievePueDB()
        avgRealLifeTemp = statistics.mean(i for i in oidData[1] if type(i) == int)
        if dataframeLength <= 12:
            avgPUE = round(pue, (2))
        else:
            avgPUE = round(avgPUE, 2)

        if len(pueDictList) <= 12:
            timeNow = int(time.time())
            resultPueDict = dict([('TIME', timeNow), ('realTimeTFE', totalInlinePower),
                ('realTimeIEE', totalPduPower), ('realTimePUE', round(pue, 2)),
                ('accTimeTFE', inlinePowerKW), ('accTimeIEE', totalPduPowerKW),
                ('accTimePUE', avgPUE), ('realTimeTemp', (avgRealLifeTemp/10))])
            pueDictList.append(resultPueDict)
            if (totalInlinePower == 0 or totalPduPower == 0 or pue == 0 or \
                inlinePowerKW == 0 or totalPduPowerKW == 0 or avgPUE == 0):
                pass
            else:
                insertPueDB([pueDictList[insertSql]])
            insertSql += 1

        if len(pueDictList) >= 13 and len(pueDictList) <= 24:
            timeNow = int(time.time())
            resultPueDict = dict([('TIME', timeNow), ('realTimeTFE', totalInlinePower),
                ('realTimeIEE', totalPduPower), ('realTimePUE', round(pue, 2)),
                ('accTimeTFE', inlinePowerKW), ('accTimeIEE', totalPduPowerKW),
                ('accTimePUE', avgPUE), ('realTimeTemp', (avgRealLifeTemp/10))])
            pueDictList.append(resultPueDict)
        if len(pueDictList) == 25:
            if (totalInlinePower == 0 or totalPduPower == 0 or pue == 0 or
                    inlinePowerKW == 0 or totalPduPowerKW == 0 or avgPUE == 0):
                pass
            else:
                insertPueDB(pueDictList[12:24])
            del pueDictList[0:12]
    except IndexError:
        avgPUE = None
    except statistics.StatisticsError:
        avgPUE = None


    efficiencyPower = totalPduPower/int(designCoolCap*1000) * 100
    totalLoadRound = round(totalPduPower / 1000, 1)

    # Cooling Capacity Calculation
    realCoolCap = None
    if idcModel == 2:
        if rackConfig == 1:
            realCoolCap = 3.0
        elif rackConfig == 2:
            realCoolCap = 6.0
        elif rackConfig == 3:
            realCoolCap = 10.0
    else:
        realCoolCap = round(realCoolingCapacity(oidData[1][0] / 10) / 1000, 1)

    # Supply Air Temperature Average Calculation
    avg = None
    avg2 = None
    try:
        try:
            if type(oidData[0][0]) == int:
                if (len(avg_temp1)<=59):
                    avg_temp1.append(oidData[0][0])
                    avg=statistics.mean(avg_temp1)/10
                elif (len(avg_temp1)==60):
                    avg_temp1.pop(0)
                    avg_temp1.append(oidData[0][0])
                    avg=statistics.mean(avg_temp1)/10
            else:
                avg = 0
        except IndexError:
            avg = None
        # Avg supply air temp 2 calculation (for idcAir only)
        try:
            if type(oidData[0][1]) == int:
                if (len(avg_temp2) <= 59):
                    avg_temp2.append(oidData[0][1])
                    avg2 = statistics.mean(avg_temp2)/10
                elif (len(avg_temp2) == 60):
                    avg_temp2.pop(0)
                    avg_temp2.append(oidData[0][0])
                    avg2 = statistics.mean(avg_temp2)/10
            else:
                avg2 = 0
        except IndexError:
            avg2 = None
    except (ValueError, ZeroDivisionError, TypeError):
        avg = None
        avg2 = None

    # Temp range indicator calculation
    rack1IntTempStatus = None
    rack2IntTempStatus = None
    rack1ExtTempStatus = None
    rack2ExtTempStatus = None
    if idcModel == 2:
        try:
            rack1IntTemp = oidData[10][0]/10 if indexLookup(oidData, 10, 0) == True else 0
            rack2IntTemp = oidData[10][1]/10 if indexLookup(oidData, 10, 1) == True else 0
            rack1ExtTemp = oidData[1][0]/10 if indexLookup(oidData, 1, 0) == True else 0
            rack2ExtTemp = oidData[1][1]/10 if indexLookup(oidData, 1, 1) == True else 0
            if rack1IntTemp == 0:
                rack1IntTempStatus = 0
            elif rack1IntTemp < 15 or rack1IntTemp > 32:
                rack1IntTempStatus = 1
            elif 15 <= rack1IntTemp < 18 or 27 <= rack1IntTemp <= 32:
                rack1IntTempStatus = 2
            elif 18 <= rack1IntTemp < 27:
                rack1IntTempStatus = 3

            if rack2IntTemp == 0:
                rack2IntTempStatus = 0
            elif rack2IntTemp < 15 or rack2IntTemp > 32:
                rack2IntTempStatus = 1
            elif 15 <= rack2IntTemp < 18 or 27 <= rack2IntTemp <= 32:
                rack2IntTempStatus = 2
            elif 18 <= rack2IntTemp < 27:
                rack2IntTempStatus = 3

            if rack1ExtTemp == 0:
                rack1ExtTempStatus = 0
            if rack1ExtTemp < 15 or rack1ExtTemp > 32:
                rack1ExtTempStatus = 1
            elif 15 <= rack1ExtTemp < 18 or 27 <= rack1ExtTemp <= 32:
                rack1ExtTempStatus = 2
            elif 18 <= rack1ExtTemp < 27:
                rack1ExtTempStatus = 3

            if rack2ExtTemp == 0:
                rack2ExtTempStatus = 0
            elif rack2ExtTemp < 15 or rack2ExtTemp > 32:
                rack2ExtTempStatus = 1
            elif 15 <= rack2ExtTemp < 18 or 27 <= rack2ExtTemp <= 32:
                rack2ExtTempStatus = 2
            elif 18 <= rack2ExtTemp < 27:
                rack2ExtTempStatus = 3
        except (ValueError, ZeroDivisionError, IndexError):
            rack1IntTempStatus = 0
            rack2IntTempStatus = 0
            rack1ExtTempStatus = 0
            rack2ExtTempStatus = 0
    
    

    #avgPUE = 1.42

    #oidData[8][0] = 1
    #oidData[8].append(2)
    #oidData[7][0] = 0
    #oidData[7].append(0)
    #oidData[9][0] = 1
    #oidData[9].append(2)
    #oidData[9].append(2)
    #oidData[6][0] = []
    #avgPUE = 1.6
    #rack2PduPower = 1410
    #rack3PduPower = 1410
    #oidData[11][0] = None
    #oidData[9][0] = None
    #oidData[9][1] = None
    #oidData[9][2] = None

    return jsonify({'int': str(avg)[:4] + "°C" if avg is not None else None,
                    'int2': str(avg2)[:4] + "°C" if avg2 is not None else None,
                    'intGauge': str(avg),
                    'ext': str(oidData[1][0]/10)[:4] + "°C",
                    'ext2': str(oidData[1][1]/10)[:4] + "°C" if indexLookup(oidData, 1, 1) == True and type(oidData[1][1]) == int else None,
                    'load': str(totalLoadRound),
                    'realCoolCap': str(realCoolCap)+ " kW",
                    'designLoadCap': "/ " + str(designCoolCap) + " kW",
                    'rack1Load': 'Rack 1: ' + str('%.2f' % round(rack1PduPower / 1000, 2)) if rack1PduPower is not None and rack1PduPower != 0 else None,
                    'rack2Load': 'Rack 2: ' + str('%.2f' % round(rack2PduPower / 1000, 2)) if rack2PduPower is not None and rack2PduPower != 0 else None,
                    'rack3Load': 'Rack 3: ' + str('%.2f' % round(rack3PduPower / 1000, 2)) if rack3PduPower is not None and rack3PduPower != 0 else None,
                    'avgPUE': '%.2f' % avgPUE if avgPUE is not None and avgPUE >= 1.00 else '%.2f' % 1,
                    'waterStatus': int(oidData[11][0]) if indexLookup(oidData, 11, 0) == True and type(oidData[11][0]) == int else None,
                    'cooler1Status': int(oidData[6][0]) if indexLookup(oidData, 6, 0) == True and type(oidData[6][0]) == int else None,
                    'cooler2Status': int(oidData[6][1]) if indexLookup(oidData, 6, 1) == True and type(oidData[6][1]) == int else None,
                    'ups1Status': int(oidData[7][0]) if indexLookup(oidData, 7, 0) == True and type(oidData[7][0]) == int else None,
                    'ups2Status': int(oidData[7][1]) if indexLookup(oidData, 7, 1) == True and type(oidData[7][1]) == int else None,
                    'fireModule1Status': int(oidData[8][0]) if indexLookup(oidData, 8, 0) == True and type(oidData[8][0]) == int else None,
                    'fireModule2Status': int(oidData[8][1]) if indexLookup(oidData, 8, 1) == True and type(oidData[8][1]) == int else None,
                    'doorRack1Status': int(oidData[9][0]) if indexLookup(oidData, 9, 0) == True and type(oidData[9][0]) == int else None,
                    'doorRack2Status': int(oidData[9][1]) if indexLookup(oidData, 9, 1) == True and type(oidData[9][1]) == int else None,
                    'doorRack3Status': int(oidData[9][2]) if indexLookup(oidData, 9, 2) == True and type(oidData[9][2]) == int else None,
                    'rack1IntTemp': str(rack1IntTemp)[:4] + "°C" if indexLookup(oidData, 10, 0) == True and type(oidData[10][0]) == int else None,
                    'rack2IntTemp': str(rack2IntTemp)[:4] + "°C" if indexLookup(oidData, 10, 1) == True and type(oidData[10][1]) == int else None,
                    'rack1IntTempStatus': rack1IntTempStatus if not None and indexLookup(oidData, 10, 0 == True) else int(0),
                    'rack2IntTempStatus': rack2IntTempStatus if not None and indexLookup(oidData, 10, 1 == True) else int(0),
                    'rack1ExtTempStatus': rack1ExtTempStatus if not None and indexLookup(oidData, 1, 0 == True) else int(0),
                    'rack2ExtTempStatus': rack2ExtTempStatus if not None and indexLookup(oidData, 1, 1 == True) else int(0),
                    'rawdata': str(efficiencyPower),
                    'idcModel': int(idcModel),
                    'rackConfigForImg': int(rackConfig),
                    'idcModelName1': 'iDC',
                    'idcModelName2': str(idcModelName),
                    'serialLabel': 'Serial Number: ',
                    'rackConfigLabel': 'Rack Config: ',
                    'designCapInfoLabel': 'Design Capacity: ',
                    'controllerIPLabel': 'Controller IP Address: ',
                    'serial': str(serial),
                    'rackConfig': str(idcRackConfig),
                    'designCapInfo': str(designCoolCap) + ' kW',
                    'controllerIP': str(controllerIP),
                    'showDoorRackTitle': 2 if indexLookup(oidData, 9, 0) == True and type(oidData[9][0]) == int or \
                        indexLookup(oidData, 9, 1) == True and type(oidData[9][1]) == int or \
                        indexLookup(oidData, 9, 2) == True and type(oidData[9][2]) == int else None,
                    'monitorModel': int(monitorModel)})
'''
if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=8080, debug=True)
    #app.run(host='0.0.0.0', port=8080, debug=True)
    # set_start_method('spawn')
    p1 = Process(target=runFlask)
    p1.start()