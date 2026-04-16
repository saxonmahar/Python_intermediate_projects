from flask import Flask,rendera_template,request
import requests
app=Flask(__name__)
API_KEY="27c8576e477c570ae9764151d708655e"
BASE_URL="https://api.openweathermap.org/data/2.5/weather"

def fetch_weather(city):
    params={
        "q":city,
        "appid":API_KEY,
        "units":"metric"
    }
    
    response=requests.get(BASE_URL,params=params)
    if response.status_code==200:
        return response.json()
    else:
        return None
    
    
def parse_weather_data(data):
    city=data["name"]  
    temperature=data["main"]["temp"]
    description=data["weather"][0]["description"]
    humidity=data["main"]["humidity"]
    wind_speed=data["wind"]["speed"]
    return{
        "city":data["name"] ,
        "temperature":data["main"]["temp"],
        "description":data["weather"][0]["description"],
        "humidity":data["main"]["humidity"],
        "wind_speed":data["wind"]["speed"]
    }  