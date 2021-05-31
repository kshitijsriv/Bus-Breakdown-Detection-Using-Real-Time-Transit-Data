'''
create a dictionary with keys as date and values as a list of 
vehicle numbers from the complaint register
'''

import csv
import pandas as pd
import pickle
from datetime import datetime, timedelta

KND_BUSES = []      # buses in KN depot
with open("../data/knd_buses.csv", "r") as f:
    reader = csv.reader(f)
    for bus in reader:
        KND_BUSES.append(bus[0])

dat = pd.read_excel('../data/analysis.xlsx')
dat['date'] = dat['date'].astype(str)
dates = dat.date.values
bus_num = dat.vehicle.values

# create dictionary with key as date and value as list of buses on that day
bus_per_day = {}
for single_date in (datetime.strptime('2019-07-01', '%Y-%M-%d') + timedelta(n) for n in range(27)):
    this_date = str(single_date.strftime('%Y-%M-%d'))
    perday = []
    for i in range(len(dates)):
        if this_date == dates[i]:
            perday.append(bus_num[i])
    bus_per_day[this_date] = perday

# change the bus number(6702) with the vehicle number(DL1PC6702)
vehnum_perday = {}
for single_date in (datetime.strptime('2019-07-01', '%Y-%M-%d') + timedelta(n) for n in range(27)):
    this_date = str(single_date.strftime('%Y-%M-%d'))
    l = []
    for j in range(len(KND_BUSES)):
        if int(KND_BUSES[j][-4:]) in bus_per_day[this_date]:
            l.append(KND_BUSES[j])
    vehnum_perday[this_date] = l

with open('../pickles/buses_per_day_compreg.pkl', 'wb') as f:
    pickle.dump(vehnum_perday, f)
