from flask import Blueprint, jsonify
import requests
import time
import threading
from collections import deque
from config import Config
from routes.battles import recent_intervals
from extensions import socketio

leaderboard_bp = Blueprint("leaderboard", __name__)

recent_positions = deque(maxlen=2)
leaderboard = []


def get_positions():
    #Fetches current drivers positions for the race.
    if True:
        response = requests.get(f"{Config.OPENF1_API_URL}/position?session_key=latest")

        if response.status_code == 200:
            recent_positions.append(response.json())

        time.sleep(3)

threading.Thread(target=get_positions, daemon=True).start()

def generate_leaderboard():
    #Combines position & interval data to generate leaderboard.
    global leaderboard
    leaderboard = []

    if not recent_positions or not recent_intervals:
        return
    
    latest_positions = recent_positions[-1]
    latest_intervals = recent_intervals[-1]
    

    for driver in latest_positions:
        driver_number = driver["driver_number"]
        position = driver["position"]


        gap_to_next_driver = next((driver_interval["interval"] for driver_interval in latest_intervals if driver_interval["driver_number"] == driver_number), "N/A")
        gap_to_leader = next((leader_interval["gap_to_leader"] for leader_interval in latest_intervals if leader_interval["driver_number"] == driver_number), "N/A")

        leaderboard.append({
            "driver": driver_number,
            "position": position,
            "interval": gap_to_next_driver,
            "gap_to_leader": gap_to_leader
        })

    socketio.emit("leaderboard_update", leaderboard)

threading.Thread(target=lambda: [time.sleep(5), generate_leaderboard()], daemon=True).start()

@leaderboard_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    #Returns the leaderboard.
    return jsonify(leaderboard if leaderboard else {"message": "Leaderboard not available yet."})