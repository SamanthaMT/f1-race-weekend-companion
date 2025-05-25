from flask import Blueprint, jsonify
#from extensions import socketio
import requests
from config import Config
import time
import threading
import os
import datetime

laps_bp = Blueprint('laps', __name__)

processed_time = None
fastest_lap = None
processed_fastest_lap = None
fastest_lap_record = {}

current_laps = {}

def update_latest_laps(processed_laps):
    global current_laps

    if processed_laps is not None:
        for lap in processed_laps:
            driver_number = lap.get("driver_number")
            lap_number = lap.get("lap_number")

            if driver_number not in current_laps:
                current_laps[driver_number] = lap_number
            else:
            
                if lap_number > current_laps[driver_number]:
                    current_laps[driver_number] = lap_number

    else:
        print("No lap data received yet.")
    
    return current_laps

def get_fastest_lap(processed_laps):
    #Fetches current lap times to determine the fastest lap of the race.
    global processed_time
    fastest_time = None
    
    try:
        for lap in processed_laps:
            lap_time = lap["lap_duration"]

            if lap_time is None:
                continue
                    
            if fastest_time is None:
                fastest_time = lap
            elif lap_time < fastest_time["lap_duration"]:
                fastest_time = lap

    except Exception as e:
        print(f"Error fetching lap data: {e}")
        
    return fastest_time

def format_lap(lap):
    from routes.drivers import get_driver_list
    driver_list = get_driver_list()

    if driver_list is not None and lap is not None:

        #Convert lap time from minutes into seconds, minutes
        time_to_convert = lap["lap_duration"]
        minutes = int(time_to_convert // 60)
        seconds = time_to_convert % 60

        result = f"{minutes:02d}:{seconds:06.3f}"
        lap["lap_duration"] = result

        #Add driver info
        driver_dictionary = {entry["driver_number"]: entry for entry in driver_list}
        
        driver_number = lap["driver_number"]
        driver_info = driver_dictionary.get(driver_number, {})

        merged_data = {**lap, **driver_info}

    return merged_data

def emit_fastest_lap():
    import routes.api_data as api_data
    global fastest_lap_record, new_fastest_lap, processed_fastest_lap

    new_fastest_lap = []

    if api_data.laps is not None:
        processed_laps = [
            {
                "driver_number": lap.get("driver_number"),
                "lap_duration": lap.get("lap_duration"),
                "lap_number": lap.get("lap_number"),
                "top_speed": lap.get("st_speed"),
                "date": lap.get("date_start")
            }
            for lap in api_data.laps
        ]

        #Update drivers current lap
        update_latest_laps(processed_laps)
        
        #update fastest lap
        current_fastest = get_fastest_lap(processed_laps)

        #Compare fastest lap in records to fastest lap in latest data and updated overall fastest lap accordingly.
        if fastest_lap_record != current_fastest:
            fastest_lap_record.clear()
            fastest_lap_record.update(current_fastest)

            lap_to_format = fastest_lap_record.copy()
            processed_fastest_lap = format_lap(lap_to_format)
            new_fastest_lap.append(processed_fastest_lap)

    return new_fastest_lap

@laps_bp.route("/laps", methods=['GET'])
def get_lap_data():
        
    return jsonify(processed_fastest_lap if processed_fastest_lap is not None else {"message": "No laps recorded yet."})
