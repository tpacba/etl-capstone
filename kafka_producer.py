from kafka import KafkaProducer
from json import dumps
from time import sleep
from api_request import ApiRequest

# Connect kafka producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x:
                         dumps(x).encode('utf-8'))
print('Connected to Kafka!')

# Stations and their lat/lng for api request
stations = [
    {'station_id': 'SE482', 'lat':33.43628, 'lng': -118.49236},
    {'station_id': 'SE687', 'lat':34.51605, 'lng': -120.38485},
    {'station_id': 'SE793', 'lat':33.78849, 'lng': -118.37804},
    {'station_id': 'SE574', 'lat':34.14406, 'lng': -116.40036},
    {'station_id': 'SE283', 'lat':34.90743, 'lng': -118.52388},
    {'station_id': 'SE278', 'lat':36.05461, 'lng': -118.74505}
]

for station in stations:
    # Request api for each station
    location = ApiRequest(station['station_id'],station['lat'],station['lng'])
    location_data = location.get_api_request()

    # Send to topic 'datastation'
    producer.send('datastation', value=location_data)
    print(location_data)

    sleep(10)


