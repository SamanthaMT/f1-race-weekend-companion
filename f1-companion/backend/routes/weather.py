from flask import Blueprint, jsonify
import requests
from config import Config
from collections import deque
import time
import threading
#from extensions import socketio
from datetime import datetime

weather_bp = Blueprint("weather", __name__)

def get_latest_weather(weather):

    current_weather = max(weather, key=lambda x: datetime.fromisoformat(x["date"].replace("Z", "00:00")))

    return current_weather

@weather_bp.route("/weather", methods=['GET'])
def get_weather_data():
    import routes.api_data as api_data

    weather_data = None

    if api_data.weather is not None:
        try:
            weather_data = max(api_data.weather, key=lambda x: datetime.fromisoformat(x["date"].replace("Z", "00:00")))
        except Exception as e:
            print("Date missing in collected weather data.")
    
    return jsonify(weather_data if weather_data is not None else {"message": "No weather data available yet."})