from google.transit import gtfs_realtime_pb2
import requests
from collections import defaultdict
import time
from datetime import datetime
import pandas as pd
from copy import deepcopy
import schedule
from cluster_cases.ST_DBSCAN.stdbscan import STDBSCAN
import sys


# read entity data from protobuffer
def get_entity_data(entity):
    vehicle_id = entity.vehicle.vehicle.id
    vehicle_lat = entity.vehicle.position.latitude
    vehicle_lon = entity.vehicle.position.longitude
    vehicle_route_id = str(int(float(entity.vehicle.trip.route_id)))
    vehicle_timestamp = entity.vehicle.timestamp
    return vehicle_id, vehicle_lat, vehicle_lon, vehicle_route_id, vehicle_timestamp


def read_feed():
    # print(OTD_RT_URL)
    feed = gtfs_realtime_pb2.FeedMessage()
    try:
        response = requests.get(OTD_RT_URL)
        feed.ParseFromString(response.content)
        # print("Feed at " + str(datetime.datetime.now()))
    except TimeoutError:
        print("URL Timeout")
    except requests.exceptions.ConnectionError:
        print('Max retries exceeded')
    return feed


def run_db_scan(df, spatial_threshold=50, temporal_threshold=20, min_neighbors=12):
    if len(df) == 0:
        print(df)
    st_dbscan = STDBSCAN(col_lat='lat', col_lon='lng',
                         col_time='timestamp', spatial_threshold=spatial_threshold,
                         temporal_threshold=temporal_threshold, min_neighbors=min_neighbors)
    df = st_dbscan.projection(df, p1_str='epsg:4326', p2_str='epsg:32635')
    result_t600 = st_dbscan.run(df)
    return result_t600


def save_to_dict():
    global remove_element_flag
    feed = read_feed()
    # print(feed)
    if time.time() - process_start_timestamp >= 1200:
        remove_element_flag = True
    for entity in feed.entity:
        # print(entity)
        vehicle_id, vehicle_lat, vehicle_lon, vehicle_route_id, vehicle_timestamp = get_entity_data(entity)
        if pb_data_dict.get(vehicle_id):
            pb_data_dict[vehicle_id]['lat'].append(vehicle_lat)
            pb_data_dict[vehicle_id]['lng'].append(vehicle_lon)
            pb_data_dict[vehicle_id]['timestamp'].append(datetime.fromtimestamp(int(vehicle_timestamp)))
            if remove_element_flag:
                print('deleted for ', vehicle_id)
                if len(pb_data_dict[vehicle_id]['lat']) <= 1:
                    del pb_data_dict[vehicle_id]
                else:
                    pb_data_dict[vehicle_id]['lat'].pop(0)
                    pb_data_dict[vehicle_id]['lng'].pop(0)
                    pb_data_dict[vehicle_id]['timestamp'].pop(0)
        else:
            vehicle_data_dict = defaultdict(list)
            vehicle_data_dict['lat'].append(vehicle_lat)
            vehicle_data_dict['lng'].append(vehicle_lon)
            vehicle_data_dict['timestamp'].append(datetime.fromtimestamp(int(vehicle_timestamp)))
            pb_data_dict[vehicle_id] = vehicle_data_dict
    # print(pb_data_dict)


def chk_cluster():
    global clustered_buses_list
    # production
    # spatial_threshold = 10
    # temporal_threshold = 900
    # min_neighbors = 90

    # testing (less time gap)
    spatial_threshold = 10
    temporal_threshold = 300
    min_neighbors = 30

    start = time.time()
    temp_list = list()
    for bus in pb_data_dict.keys():
        bus_data_df = pd.DataFrame.from_dict(pb_data_dict[bus])
        if len(bus_data_df) != 0:
            clustered_df = run_db_scan(deepcopy(bus_data_df), spatial_threshold=spatial_threshold,
                                       temporal_threshold=temporal_threshold, min_neighbors=min_neighbors)
            bus_data_df['cluster'] = clustered_df['cluster']
            # unique_clusters = chk_if_cluster_close_to_depot(bus_data_df)
            unique_clusters = pd.unique(bus_data_df.cluster)
            if len(unique_clusters) > 1:
                print('cluster detected for ', bus, pb_data_dict[bus])
                temp_list.append(bus)
            else:
                print('no cluster detected for ', bus)
    clustered_buses_list = temp_list
    print(clustered_buses_list)
    print(time.time() - start)


if __name__ == '__main__':
    OTD_API_KEY = sys.argv[1]
    OTD_RT_URL = f'https://otd.delhi.gov.in/api/realtime/VehiclePositions.pb?key={OTD_API_KEY}'
    print('OTD API URL', OTD_RT_URL)

    pb_data_dict = {}
    clustered_buses_list = list()
    remove_element_flag = False
    process_start_timestamp = time.time()
    schedule.every(10).seconds.do(save_to_dict)
    schedule.every(180).seconds.do(chk_cluster)
    while True:
        schedule.run_pending()
        time.sleep(1)
