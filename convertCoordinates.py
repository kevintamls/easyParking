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

parking_df = pd.read_csv('ON_STREET_PARK.csv')

x_old_coor = list(parking_df['X_COOR'])
y_old_coor = list(parking_df['Y_COOR'])
print(len(x_old_coor))

# Function to convert coordinates. Takes both x and y old coordinates
def coordinateConvertion(x_old, y_old):
    numberOfProcs = 100
    out_q1 = mp.Queue()
    def worker1(x_old, y_old, out_q1):
        points = []
        for i in range(len(x_old)):
            url = 'http://www.geodetic.gov.hk/transform/v2/?inSys=hkgrid&outSys=wgsgeog&e=' + str(x_old[i]) + '&n=' + str(y_old[i])
            r = requests.get(url)
            data = r.json()
            coor = Point((data['wgsLong'], data['wgsLat']))
            #print(len(points))
            points.append(coor)
            #print(points)
        out_q1.put(points)
    
    # Chunksize to split large list on multiple processes
    chunksize = (int(math.ceil(len(x_old)/float(numberOfProcs))))
    #print(chunksize)

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
    
    results = []
    for i in range(numberOfProcs):
        results.append(out_q1.get())

    for p in procs:
        p.join()
    
    flatResults = list(itertools.chain.from_iterable(results))
    print(flatResults)
    d = {'geometry': flatResults}
    #print(d)
    gdf = gpd.GeoDataFrame(d, crs = 'EPSG:3857')
    gdfJson = gdf.to_json()
    with open('gdfLong.json', 'w') as f:
        json.dump(gdfJson, f)

    #geojsonio.display(gdf.to_json())

coordinateConvertion(x_old_coor, y_old_coor)