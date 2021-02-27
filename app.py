# Import libraries flask for web server backend processing, random and json python libraries
from flask import Flask, render_template, jsonify, request, json
from multiprocessing import Process, freeze_support, set_start_method
from random import randint
import json
import multiprocessing as mp
import subprocess

app = Flask(__name__) # Initialise flask app instance

# Function to execute flask application
def runFlask():
    app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=True)

# App route to direct to root, renders index.html (main page)
@app.route("/")
def index():
    return render_template('index.html')

# App route "get data" to receive simulation data for parking spot status updates
@app.route('/_get_data/', methods=['GET', 'POST'])
def get_data():
    tempCoorStore = []
    
    with open('gdf.json', 'r') as f: # Opens pre-process json file which stores coordinates of parking spaces
        coordinateJson = json.load(f)
        coordinateJsonConverted = json.loads(coordinateJson) # Converts into python dictionary for manipulation
        for items in coordinateJsonConverted['features']:
            tempCoorStore.append(items) # Add dictionary items into list for processing
        for i in range(len(tempCoorStore)):
            tempCoorStore[i]['properties'] = {'avail': str(randint(0,1))} # Modifies key "properties" to dictionary
                                                                          # with "avail" and stringified integer as
                                                                          # value
    f.close()
    finalDict = {"type": "FeatureCollection", "features": tempCoorStore} # Constructs final dictionary fit for
                                                                         # jsonification
    return jsonify({'coordinates': json.dumps(finalDict)}) # Returns jsonified dictionary into frontend JavaScript

if __name__ == "__main__":
    p1 = Process(target=runFlask) # Defines process to start Flask for multiprocessing
    p1.start() # Executes Flask