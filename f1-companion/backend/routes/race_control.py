from flask import Blueprint, jsonify
import requests
from config import Config
import time
import threading
import os
from collections import deque
from datetime import datetime

race_control_bp = Blueprint("race_control", __name__)

last_race_message = {}
messages = {}

message_history = []

last_message_date = None

def filter_messages(race_message):
    global last_message_date
    new_messages = []
    last_dt = None

    for message in race_message:
        if "message" not in message:
            continue
    
        message_date = message["date"]
        message_flag = message["flag"]
        message_dt = datetime.fromisoformat(message_date.replace("Z", "+00:00")) if message_date else None

        if message_flag == "CHEQUERED" or message_flag == "RED" or message_flag is None:
            if last_message_date is None or last_message_date < message_dt:
                new_messages.append(message)
                if last_dt is None or last_dt < message_dt:
                    last_dt = message_dt
        else:
            continue

    if last_dt is not None:
        last_message_date = last_dt
            
    return new_messages

def emit_race_control():
    import routes.api_data as api_data
    global message_history

    if api_data.race_control is not None:
        processed_messages = [
            {
                "flag": mess.get("flag"),
                "lap_number": mess.get("lap_number"),
                "message": mess.get("message"),
                "date": mess.get("date")
            }
            for mess in api_data.race_control
        ]

        #method to filter messages and find new ones
        new_messages = filter_messages(processed_messages)

        if new_messages:
            if message_history is None:
                message_history = new_messages
            else:
                for messages in new_messages:
                    message_history.append(messages)

    else:
        new_messages = []

    return new_messages

@race_control_bp.route("/race-control", methods=['GET'])
def get_race_control():
    
    return jsonify(message_history if message_history is not None else {"message": "No race control updates yet."})
