from flask import Blueprint, jsonify
import requests
import time
import threading
from collections import deque
from config import Config
from routes.car_data import recent_car_data
from extensions import socketio


battles_bp = Blueprint("battles", __name__)

recent_intervals = deque(maxlen=2)
battles = []


def get_intervals():
    #Fetches current intervals between drivers for the race.
    while True:
        response = requests.get(f"{Config.OPENF1_API_URL}/intervals?session_key=latest")
    
        if response.status_code == 200:
            recent_intervals.append(response.json())

        time.sleep(3)

threading.Thread(target=get_intervals, daemon=True).start()


def detect_battles():
    #Analyzes intervals to detect battles.
    global battles
    battles = []

    if len(recent_intervals) < 2 or len(recent_car_data) < 2:
        return
    
    latest_intervals = recent_intervals[-1]
    latest_car_data = recent_car_data[-1]


    for interval in latest_intervals:
        driver_a = interval["driver_number"]
        driver_b = interval["next_driver_number"]
        gap = interval["time_gap"]

        #Identify battle if gap between drivers is <0.2s
        if gap < 0.2:
            battles.append({
                "drivers": f"{driver_a} vs {driver_b}",
                "gap": gap,
                "reason": "Close gap (<0.2s)"
            })
            continue
        
        #Identify battle if gap between driver is <0.5 and drs is enabled
        driver_b_drs = next((drs_status["drs"] for drs_status in latest_car_data if drs_status["driver_number"] == driver_b), None)

        if gap < 0.5 and driver_b_drs in {10, 12, 14}:
            battles.append({
                "driver": f"{driver_a} vs {driver_b}",
                "gap": gap,
                "reason": "DRS active for Driver B"
            })

        if battles:
            socketio.emit("battle_update", battles)

threading.Thread(target=lambda: [time.sleep(5), detect_battles()], daemon=True).start()

@battles_bp.route('/battles', methods=['GET'])
def get_battle_data():
    #Returns detected battles.
    return jsonify(battles if battles else {"message": "No battles detected."})
