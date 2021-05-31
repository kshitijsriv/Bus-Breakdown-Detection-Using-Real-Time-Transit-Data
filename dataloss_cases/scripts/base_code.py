import gmplot
import csv
import pickle	
import googlemaps
import pandas as pd
import numpy as np
from geopy.distance import geodesic
import sqlite3
from datetime import datetime, timedelta
import os
import matplotlib.pyplot as plt
import time
import folium
import math

# loading all destination coordinates from file wrt the trip_id
with open('../pickles/trip_to_stop.pkl', 'rb') as f:  
    tripstop = pickle.load(f)

# loading all source coordinates from file wrt the trip_id
with open('../pickles/trip_to_source.pkl', 'rb') as f:  
    tripsource = pickle.load(f)

# load normalised network grid
with open('../pickles/norm_grid200.pkl', 'rb') as f:
    fgrid = pickle.load(f)

# load the no. of buses from comp. register for each day
with open('../pickles/vehnum_perday.pkl', 'rb') as f:
    complaint_vehnum_perday = pickle.load(f)

# store buses in KN depot in KND_BUSES
KND_BUSES = []      
with open("../data/knd_buses.csv", "r") as f:
    reader = csv.reader(f)
    for bus in reader:
        KND_BUSES.append(bus[0])

# for alloting points into cells in the grid
min_lat, min_lng = (28.404181, 76.83831)
max_lat, max_lng = (28.88382, 77.343689)
cells = 200
cols = np.linspace(min_lng, max_lng, num=cells)
rows = np.linspace(min_lat, max_lat, num=cells)


time_difference = lambda t1, t2: (int(t2) - int(t1))/60     #return time diff b/w 2 pts
distance = lambda s1, s2: geodesic(s1, s2).km * 1000        #return distance b/w 2 pts
