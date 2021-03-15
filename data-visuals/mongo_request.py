from pymongo import MongoClient
from bson import json_util
import datetime

import pandas
import json

client = MongoClient("mongodb+srv://tpacba:OneYear_95@cluster0.ufwrg.mongodb.net/station_data?retryWrites=true&w=majority")
db = client.station_data
cursor = db.list_stations.find({})

list_data = []

for item in cursor:
    item = json.loads(json_util.dumps(item))
    list_data.append(item)
    print(item)

pd_obj = pandas.read_json(json.dumps(list_data), orient='records')
pd_obj.to_csv('./data-visuals/station_data.csv')