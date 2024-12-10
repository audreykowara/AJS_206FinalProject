import requests 
import sqlite3
import time
#import matpotlib.pyplot as plt
import pandas as pd

#AccuWeather API key and URL
BASE_URL = "http://dataservice.accuweather.com/locations/v1/cities/search"
API_KEY = "4CFp5OziXB2x7O8uAoQICsg3BKDE94tv"

#SQLite Datababse Set up
def setup_database():
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            temperature REAL,
            weather_condition TEXT,
            wind_speed REAL,
            humidity INTEGER,
            observation_time TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Wind (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            wind_speed REAL,
            observation_time TEXT,
            FOREIGN KEY(id) REFERENCES Weather(id)
        )
    ''')
    conn.commit()
    conn.close()

#Function to get current weather data
def get_weather(city):
    #Get location key for the city
    location_url = f"{BASE_URL}locations/v1/cities/search"
    location_params = {
        'apikey': API_KEY,
        'query': "Chicago"  
    }

    location_response = requests.get(location_url, params=location_params)
    if location_response.status_code == 200:
        location_data = location_response.json()
        if location_data:
             location_key = location_data[0]['Key']  # Use the first location key
             city_name = location_data[0]['LocalizedName']

             #Get current conditions sing the location key
             weather_url = f"{BASE_URL}currentconditions/v1/{location_key}"
             weather_params = {
                'apikey': API_KEY,
                'details': 'true'  # Optional: provides additional details
            }
             weather_response = requests.get(weather_url, params=weather_params)
             if weather_response.status_code == 200:
                weather_data = weather_response.json()
                if weather_data:
                    return {
                        'temperature': weather_data[0]['Temperature']['Metric']['Value'],  # Temperature in Celsius
                        'weather_condition': weather_data[0]['WeatherText'],
                        'wind_speed': weather_data[0]['Wind']['Speed']['Metric']['Value'],  # Wind speed in km/h
                        'humidity': weather_data[0].get('RelativeHumidity', None),
                        'observation_time': weather_data[0]['LocalObservationDateTime']
                    }
    return None

#Function to store weather data in the database
def store_weather_data(city, wetaher_data):
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Weather (city, temperature, weather_condition, wind_speed, humidity, observation_time)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (city, weather_data['temperature'], weather_data['weather_condition'], weather_data['wind_speed'], weather_data['humidity'], weather_data['observation_time']))
    cursor.execute('''
        INSERT INTO Wind (city, wind_speed, observation_time)
        VALUES (?, ?, ?)
    ''', (city, weather_data['wind_speed'], weather_data['observation_time']))
    conn.commit()
    conn.close()

#Main function to gather data
def main():
    setup_database()
    cities = ['Chicago']

    for city in cities:
        for _ in range(25):  # Gather data multiple times to reach 100 records
            weather_data = get_weather(city)
            if weather_data:
                store_weather_data(city, weather_data)
                print(f"Stored data for {city}")
            else:
                print(f"Could not get weather data for {city}")
            # Delay to avoid hitting the rate limit of the API
            time.sleep(1)




                   
    





