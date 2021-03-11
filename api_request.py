import arrow
import requests

class ApiRequest:
    def __init__(self, station_id, lat, lng):
        self.station_id = station_id
        self.lat = lat
        self.lng = lng

    def get_api_request(self):

        # # Get the current hour
        # start = arrow.now('US/Pacific').floor('hour')
        # end = arrow.now('US/Pacific').ceil('hour')

        # api_key = '3ac08b94-db36-11ea-bdeb-0242ac130002-3ac08c5c-db36-11ea-bdeb-0242ac130002'
        # weather_params = ','.join(['windSpeed','gust','airTemperature','humidity'])
        # solar_params = ','.join(['uvIndex'])

        # # Request from Storm Glass weather endpoint
        # weather_response = requests.get(
        # 'https://api.stormglass.io/v2/weather/point',
        # params={
        # 'lat': self.lat,
        # 'lng': self.lng,
        # 'params': weather_params,
        # 'start': start.to('UTC').timestamp(),  # Convert to UTC timestamp
        # 'end': end.to('UTC').timestamp()  # Convert to UTC timestamp
        # },
        # headers={
        #     'Authorization': api_key
        # }
        # )

        # weather_data = weather_response.json()
        # # print(weather_data)

        # # Request from Storm Glass solar endpoint
        # solar_response = requests.get(
        # 'https://api.stormglass.io/v2/solar/point',
        # params={
        #     'lat': self.lat,
        #     'lng': self.lng,
        #     'params': solar_params,
        #     'start': start.to('UTC').timestamp(),  # Convert to UTC timestamp
        #     'end': end.to('UTC').timestamp()  # Convert to UTC timestamp
        # },
        # headers={
        #     'Authorization': api_key
        # }
        # )

        # solar_data = solar_response.json()
        # # print(solar_data)

        # Example Data
        weather_data = {'hours': [{'airTemperature': {'noaa': 13.19, 'sg': 13.19}, 'gust': {'noaa': 12.58, 'sg': 12.58}, 'humidity': {'noaa': 67.0, 'sg': 67.0}, 'time': '2021-03-09T20:00:00+00:00', 'windSpeed': {'icon': 10.34, 'noaa': 10.75, 'sg': 10.34}}], 'meta': {'cost': 1, 'dailyQuota': 50, 'end': '2021-03-09 20:59', 'lat': self.lat, 'lng': self.lng, 'params': ['windSpeed', 'gust', 'airTemperature', 'humidity'], 'requestCount': 2, 'start': '2021-03-09 20:00'}}
        solar_data = {'hours': [{'time': '2021-03-09T20:00:00+00:00', 'uvIndex': {'noaa': 0.16, 'sg': 0.16}}], 'meta': {'cost': 1, 'dailyQuota': 50, 'end': '2021-03-09 20:59', 'lat': self.lat, 'lng': self.lng, 'params': ['uvIndex'], 'requestCount': 3, 'start': '2021-03-09 20:00'}}

        data = {
        'airTemperature': weather_data['hours'][0]['airTemperature']['noaa'],
        'gust': weather_data['hours'][0]['gust']['noaa'],
        'humidity': weather_data['hours'][0]['humidity']['noaa'],
        'lat': weather_data['meta']['lat'],
        'lng': weather_data['meta']['lng'],
        'station_id': self.station_id,
        'time': weather_data['hours'][0]['time'],
        'uvIndex': solar_data['hours'][0]['uvIndex']['noaa'],
        'windSpeed': weather_data['hours'][0]['windSpeed']['noaa']
        }

        return data