from flask import Blueprint, jsonify
import requests
from collections import deque
import time
import threading
from config import Config

car_data_bp = Blueprint("car_data", __name__)

recent_car_data = deque(maxlen=2)

def get_car_data_updates():
    #Fetches car metrics and stores recent data, including speed tracking.
    while True:
        response = requests.get(f"{Config.OPENF1_API_URL}/car_data?session_key=latest")

        if response.status_code == 200:
            car_data = response.json()
            recent_car_data.append(car_data)

        time.sleep(3)

threading.Thread(target=get_car_data_updates, daemon=True).start()

@car_data_bp.route("/car-data", methods=['GET'])
def get_car_data():
    return jsonify(recent_car_data[-1] if recent_car_data else {"message": "No car data available yet."})
