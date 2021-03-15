from pymongo import MongoClient
from bson import json_util

import pandas
import json

client = MongoClient("mongodb+srv://tpacba:OneYear_95@cluster0.ufwrg.mongodb.net/station_data?retryWrites=true&w=majority")
db = client.station_data
cursor = db.list_stations.find({})

list_data = []

for item in cursor:
    item = json.loads(json_util.dumps(item))
    list_data.append(
        {
            'airTemperature': item['airTemperature'],
            'gust': item['gust'],
            'humidity': item['humidity'],
            'lat': item['lat'],
            'lng': item['lng'],
            'station_id': item['station_id'],
            'time': item['time'],
            'uvIndex': item['uvIndex'],
            'windSpeed': item['windSpeed']
        }
    )

pd_obj = pandas.read_json(json.dumps(list_data), orient='records')
pd_df = pd_obj.drop_duplicates()
print(pd_df)
pd_df.to_csv('./data-visuals/station_data.csv')
