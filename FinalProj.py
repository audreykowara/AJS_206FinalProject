#AJS Force: Audrey Kowara, Jessica Yang, Sydney Emuakhagbon
#206 Final Project "Chicago Holiday Planning"


import requests
import sqlite3
import time
import matplotlib.pyplot as plt
#import pandas as pd

# AccuWeather API key and base URL
API_KEY = '4CFp5OziXB2x7O8uAoQICsg3BKDE94tv'
BASE_URL = 'http://dataservice.accuweather.com/'

# SQLite Database setup
def setup_database():
    conn = sqlite3.connect('weather_data.db')
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
    url  = f"{BASE_URL}"
    params = {
        'access_key': API_KEY,
        'query' : "Chicago"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "current" in data:
            return {
                'temperature': data['current']['temperature'],  # Temperature in Celsius
                'weather_condition': data['current']['weather_descriptions'][0],
                'wind_speed': data['current']['wind_speed'],  # Wind speed in km/h
                'humidity': data['current']['humidity'],
                'observation_time': data['location']['localtime']
            }
    return None

#Function to store weather data in the database
def store_weather_data(city, weather_data):
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

# Main function to gather data
def main():
    setup_database()
    cities = ['Chicago']  # Example city

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


