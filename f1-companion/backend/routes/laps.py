from flask import Blueprint, jsonify
from extensions import socketio
import requests
from config import Config
import time
import threading
import os


laps_bp = Blueprint('laps', __name__)

fastest_lap = None

def get_lap_updates():
    #Fetches current lap times to determine the fastest lap of the race.
    global fastest_lap
    
    while True:
        try:
            response = requests.get(f"{Config.OPENF1_API_URL}/laps?session_key=latest")
            if response.status_code == 200:
                lap_data = response.json()

                for lap in lap_data:
                    lap_time = lap["lap_duration"]

                    if lap_time is None:
                        continue
                    
                    if fastest_lap is None:
                        fastest_lap = lap
                        print(f"New Fastest Lap: {fastest_lap}")
                        socketio.emit("fastest_lap_update", fastest_lap)
                    elif lap_time < fastest_lap["lap_duration"]:
                        fastest_lap = lap
                        print(f"New Fastest Lap: {fastest_lap}")
                        socketio.emit("fastest_lap_update", fastest_lap)
        except Exception as e:
            print(f"Error fetching lap data: {e}")

        time.sleep(15)

threading.Thread(target=get_lap_updates, daemon=True).start()

@laps_bp.route("/laps", methods=['GET'])
def get_fastest_lap():
    print("Lap page visited! Sending message to Flask console...")
    socketio.emit('message', "Lap page reached")  # Send message to Flask console
    return jsonify(fastest_lap if fastest_lap else {"message": "No laps recorded yet."})

#For testing
@laps_bp.route("/lap_manual")
def lap_manual():
    print("Manually emitting fastest lap update, PID:", os.getpid())
    socketio.emit("fastest_lap_update", {
        "driver": "Max Verstappen",
        "lap_number": 18,
        "lap_duration": 87.562
    })
    return jsonify({"status": "Manual lap event emitted"})
