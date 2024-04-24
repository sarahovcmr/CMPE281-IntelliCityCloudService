import json
import os

from datetime import datetime, timedelta
from dotenv import load_dotenv
from pymongo import MongoClient
from statistics import mean
load_dotenv()

class MongoDBProcessor:
    def __init__(self):
        #mongoDB connection
        self.client = MongoClient(os.getenv('mongodb_uri'))
        self.db = self.client['smartcity']
        self.iot_collection = self.db['iot']

        # get device info
    def get_iot_info(self, station_id):
        iot_info = self.iot_collection.find_one({'station_id': int(station_id)})

        # return iot_info
        station_id = iot_info['station_id']
        address = str(iot_info['Fwy']) + ' ' + str(iot_info['Dir'])
        latitude = iot_info['location'][0]
        longitude = iot_info['location'][1]
        district = iot_info['District']
        hourlySpeed = self.get_hourly_speed(station_id)

        return {
            'station_id': station_id,
            'address': address,
            'district': district,
            'latitude': latitude,
            'longitude': longitude,
            'hourlySpeed': hourlySpeed
        }

    # Search by station_id or freeway or district
    def search_iot_info(self, search):
        iot_info = self.iot_collection.find({'$or': [{'station_id': int(search)}, {'Fwy': int(search)}, {'District': search}]}).limit(100)
        iot_data = []
        for iot in iot_info:
            station_id = iot['station_id']
            address = str(iot['Fwy']) + ' ' + str(iot['Dir'])
            latitude = iot['location'][0]
            longitude = iot['location'][1]
            district = iot['District']
            iot_data.append({
                'id': station_id,
                'address': address,
                'district': district,
                'latitude': latitude,
                'longitude': longitude
            })
        return iot_data

    def get_hourly_speed(self, station_id):
        # Fetch data from MongoDB
        station_data = self.iot_collection.find_one({"station_id": station_id})

        # Process timeseries data
        timeseries = station_data['timeseries']
        hourly_speeds = []

        # Group data by hour and calculate average speed
        for i in range(24):
            hour_data = [entry['Speed'] for entry in timeseries[i*12:(i+1)*12]]
            if hour_data and not any(x is None for x in hour_data):  # Ensure there is data to average
                average_speed = mean(hour_data)
                # Round the average speed to two decimal places
                rounded_average = round(average_speed, 2)
                hourly_speeds.append(rounded_average)
            else:
                # Append a default value or handle missing data as needed
                hourly_speeds.append(0.00)  # Example default value

        print(hourly_speeds)
        return json.dumps(hourly_speeds)




    
    