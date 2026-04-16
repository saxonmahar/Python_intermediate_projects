import os
import requests
from flask import Flask, render_template, request, flash
from dotenv import load_dotenv

# Professional setup: Load environment variables
load_dotenv()

app=Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default-dev-key-change-this")

API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Professional check: Ensure API key exists before starting
if not API_KEY:
    raise ValueError("CRITICAL ERROR: OPENWEATHER_API_KEY not found in environment variables.")

BASE_URL="https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL="https://api.openweathermap.org/data/2.5/forecast"

def fetch_weather(city):
    """Fetches current weather with error handling."""
    try:
        params={"q": city, "appid": API_KEY, "units": "metric"}
        response = requests.get(BASE_URL, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        return None
    return None

def fetch_forecast(city):
    """Fetches 5-day forecast data."""
    try:
        params={"q": city, "appid": API_KEY, "units": "metric"}
        response = requests.get(FORECAST_URL, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        return None
    return None

def parse_weather_data(data):
    """Extracts current weather and icon."""
    return{
        "city":data["name"] ,
        "temperature":data["main"]["temp"],
        "description":data["weather"][0]["description"].capitalize(),
        "icon": data["weather"][0]["icon"],
        "humidity":data["main"]["humidity"],
        "wind_speed":data["wind"]["speed"]
    }

def parse_forecast_data(data):
    """Processes forecast to show one snapshot per day with icons."""
    forecast_list = []
    if not data or "list" not in data:
        return forecast_list

    # The API returns 3-hour increments (8 per day). 
    # We take every 8th item to represent a daily snapshot.
    for entry in data.get("list", [])[::8]:
        forecast_list.append({
            "date": entry["dt_txt"].split(" ")[0],
            "temp": entry["main"]["temp"],
            "description": entry["weather"][0]["description"].capitalize(),
            "icon": entry["weather"][0]["icon"]
        })
    return forecast_list

@app.route('/', methods=["GET", "POST"])
def home():
    weather = None
    forecast = None

    if request.method == "POST":
        city = request.form.get("city", "").strip()
        weather_raw = fetch_weather(city)
        forecast_raw = fetch_forecast(city)

        if weather_raw:
            weather = parse_weather_data(weather_raw)
            forecast = parse_forecast_data(forecast_raw)
        else:
            flash(f"Could not find weather for '{city}'.", "danger")

    return render_template("index.html", weather=weather, forecast=forecast)


if __name__ == "__main__":
    app.run(debug=True)
                