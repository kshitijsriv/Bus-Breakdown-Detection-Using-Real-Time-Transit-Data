# For detection of cluster breakdown cases

ST-DBSCAN code source - [Py-ST-DBSCAN](https://github.com/eubr-bigsea/py-st-dbscan)

## Executing the realtime cluster detection script

- register for real-time GTFS data from [OTD Delhi platform](https://otd.delhi.gov.in/data/realtime/)
- copy the API key, request will be approved in a few hours
- pass the __API KEY__ as a command line argument

        ```python rt_cluster.py {API-KEY}```

*can also plug in other realtime data sources with minor tweaks
