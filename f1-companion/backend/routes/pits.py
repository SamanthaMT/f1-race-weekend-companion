from flask import Blueprint, jsonify
from extensions import socketio
import requests
from config import Config
import time
import threading
import os

pits_bp = Blueprint("pits", __name__)

last_pit_stops = {}

#Function to fetch and send Pit updates
def get_pit_updates():
    global last_pit_stops

    while True:
        response = requests.get(f"{Config.OPENF1_API_URL}/pit?session_key=latest")
        if response.status_code == 200:
            pit_stops = response.json()

            new_pit_stops = []
            for stop in pit_stops:

                if "driver_number" not in stop or "lap_number" not in stop:
                    print(f"Skipping incomplete entry: {stop}")
                    continue
                
                driver = stop["driver_number"]
                lap = stop["lap_number"]

                if driver not in last_pit_stops:
                    new_pit_stops.append(stop)
                    last_pit_stops.update({driver: lap})
                elif last_pit_stops[driver] < lap:
                    new_pit_stops.append(stop)
                    last_pit_stops[driver] = lap
            
            if new_pit_stops:
                socketio.emit("pit_stop_update", new_pit_stops)

            time.sleep(10)


threading.Thread(target=get_pit_updates, daemon=True).start()

@pits_bp.route("/pits", methods=['GET'])
def get_pits():
    print("Pit page visited! Sending message to Flask console...")
    socketio.emit('message', "Pit page reached")  # Send message to Flask console
    return jsonify(last_pit_stops if last_pit_stops else {"message": "No pit stop updates yet."})

@pits_bp.route("/pit_manual")
def pit_manual():
    print("Manually emitting new pit update, PID:", os.getpid())
    socketio.emit("pit_stop_update", {
        "driver_number": 4,
        "lap_number": 18,
    })
    return jsonify({"status": "Manual pit event emitted"})