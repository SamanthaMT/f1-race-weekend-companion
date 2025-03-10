from flask import Blueprint, jsonify
from extensions import socketio
import requests
from config import Config
import time
import threading
import os

race_control_bp = Blueprint("race_control", __name__)

last_race_message = []

#Function to fetch and send Race Control updates
def get_race_control_updates():
    from extensions import socketio
    global last_race_message

    while True:
        response = requests.get(f"{Config.OPENF1_API_URL}/race_control?session_key=latest")
        if response.status_code == 200:
            messages = response.json()

            if messages != last_race_message:
                print("Emitting race_control_update")
                socketio.emit("race_control_update", messages)
                last_race_message = messages

        time.sleep(5)

threading.Thread(target=get_race_control_updates, daemon=True).start()

@race_control_bp.route("/race-control", methods=['GET'])
def get_race_control():
    print("Race control page visited! Sending message to Flask console...")
    socketio.emit('message', "Race control page reached")  # Send message to Flask console
    return jsonify(last_race_message if last_race_message else {"message": "No race control updates yet."})

#For testing
@race_control_bp.route("/race_control_manual")
def race_control_manual():
    print("Manually emitting new race control update, PID:", os.getpid())
    socketio.emit("race_control_update", {
        "message": "Safety Car Deployed"
    })
    return jsonify({"status": "Manual race control event emitted"})