# Libraries Import
import pandas as pd
import numpy as np
import json
import geopandas as gpd
import requests
import geojson
import geojsonio
from shapely.geometry import Point
import multiprocessing as mp
import math
import itertools

# Define dataframe for reading parking spaces csv
parking_df = pd.read_csv('ON_STREET_PARK.csv')

# Seperately defined list for x,y coordinates of parking spaces
x_old_coor = list(parking_df['X_COOR'])
y_old_coor = list(parking_df['Y_COOR'])

# Function to convert coordinates. Takes both x and y old coordinates
def coordinateConvertion(x_old, y_old):
    numberOfProcs = 100 # Number of instances to initialise for multiprocessing
    out_q1 = mp.Queue() # Queue for multiprocessing
    # Worker definition for multiprocessing
    def worker1(x_old, y_old, out_q1):
        points = []
        for i in range(len(x_old)):
            url = 'http://www.geodetic.gov.hk/transform/v2/?inSys=hkgrid&outSys=wgsgeog&e=' + str(x_old[i]) + '&n=' + str(y_old[i])
            r = requests.get(url)
            data = r.json()
            coor = Point((data['wgsLong'], data['wgsLat']))
            points.append(coor)
        out_q1.put(points)
    
    # Chunksize to split large list on multiple processes
    chunksize = (int(math.ceil(len(x_old)/float(numberOfProcs))))

    # List to keep t rack of currently running processes
    procs = []

    # Multiprocesses execution for loop
    for i in range(numberOfProcs):
        p = mp.Process(
            target = worker1,
            args = (x_old[chunksize * i:chunksize * (i+1)], 
                y_old[chunksize * i:chunksize * (i+1)],
                out_q1)
        )
        procs.append(p)
        p.start()
    
    results = [] # List to store queue results
    for i in range(numberOfProcs):
        results.append(out_q1.get())

    for p in procs:
        p.join() # Joins all processes into one and terminates
    
    flatResults = list(itertools.chain.from_iterable(results)) # Flatten dictionary list for jsonification
    d = {'geometry': flatResults} # Variable for GeoDataframe insertion
    gdf = gpd.GeoDataFrame(d, crs = 'EPSG:3857') # Creating GeoDataFrame
    gdfJson = gdf.to_json() # Jsonification and export to external json file
    with open('gdfLong.json', 'w') as f:
        json.dump(gdfJson, f)

coordinateConvertion(x_old_coor, y_old_coor) # Executes function for convertion