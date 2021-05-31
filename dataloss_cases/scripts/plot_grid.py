import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import geopandas
from geopandas import GeoSeries
from shapely.geometry import Polygon


min_lat, min_lng = (28.404181, 76.83831)
max_lat, max_lng= (28.88382, 77.343689)
top_left = (max_lat, min_lng)
top_right = (max_lat, max_lng)
bot_left = (min_lat, min_lng)
bot_right = (min_lat, max_lng)

n = 200
cols = np.linspace(min_lng, max_lng, num=n)
rows = np.linspace(min_lat, max_lat, num=n)

f = open('norm_grid200.pkl','rb')
fgrid = pickle.load(f)
f.close()

boxes = []
for i in range(len(rows)-1):
    for j in range(len(cols)-1):
        boxes.append(Polygon([(rows[i],cols[j]),(rows[i],cols[j+1]),(rows[i+1],cols[j+1]),(rows[i+1],cols[j])])) 

gr = []
for i in range(len(rows)-1):
    for j in range(len(cols)-1):
         gr.append(fgrid[i][j])

df = pd.DataFrame(
    {'val' : gr,
     'Coordinates': boxes})

gdf = geopandas.GeoDataFrame(df, geometry='Coordinates')
gdf.plot(column = 'val',legend=True, figsize=(10,10))
plt.show()
gdf.plot(column = 'val',legend=True, figsize=(10,10),cmap='hot')
plt.show()