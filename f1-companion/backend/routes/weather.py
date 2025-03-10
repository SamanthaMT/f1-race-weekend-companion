from flask import Blueprint, jsonify
import requests
from config import Config
from collections import deque
import time
import threading


weather_bp = Blueprint("weather", __name__)

recent_weather_data = deque(maxlen=1)

def get_weather():
    #Fetches live weather data for the race track.
    while True:
        response = requests.get(f"{Config.OPENF1_API_URL}/weather?session_key=latest")

        if response.status_code == 200:
            weather_data = response.json()
            recent_weather_data.append(weather_data)

        time.sleep(180)

threading.Thread(target=get_weather, daemon=True).start()

@weather_bp.route("/weather", methods=['GET'])
def get_weather_data():
    return jsonify(recent_weather_data[-1] if recent_weather_data else {"message": "No weather data available yet."})
