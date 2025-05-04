
from flask import Blueprint, jsonify
import requests
import time
import threading
from config import Config
from datetime import datetime


position_data_bp = Blueprint("position_data", __name__)

latest_position_data = {}
latest_interval_data = {}
starting_position_data = {}
positions_and_intervals = {}
positions_data = None
intervals_data = None
initial = True

def simulated_positions_response():
    return [{
        "driver_number": 1,
        "position": 3,
        "date": "2025-03-16T04:20:49.979000+00:00"
    },
    {
        "driver_number": 4,
        "position": 1,
        "date": "2025-03-16T04:20:49.979000+00:00"
    },
    {
        "driver_number": 5,
        "position": 2,
        "date": "2025-03-16T04:20:49.979000+00:00"
    },
    {
        "driver_number": 16,
        "position": 4,
        "date": "2025-03-16T04:20:49.979000+00:00"
    }]


def simulated_intervals_response():

    return [{
        "driver_number": 1,
        "interval": 0.298,
        "gap_to_leader": 0.425,
        "date": "2025-03-16T04:20:49.979000+00:00"
    },
    {
        "driver_number": 4,
        "interval": "null",
        "gap_to_leader": "null",
        "date": "2025-03-16T04:20:49.979000+00:00"
    },
    {
        "driver_number": 5,
        "interval": 0.127,
        "gap_to_leader": 0.127,
        "date": "2025-03-16T04:20:49.979000+00:00"
    },
    {
        "driver_number": 16,
        "interval": 0.335,
        "gap_to_leader": 0.76,
        "date": "2025-03-16T04:20:49.979000+00:00"
    }]

def combined_positions_intervals(latest_positions, latest_intervals):

    if not latest_positions or not latest_intervals:
        return []
    combined_dictionary = {entry["driver_number"]: entry for entry in latest_intervals}

    combined_data = []
    for position in latest_positions:
        driver_number = position["driver_number"]
        extra = combined_dictionary.get(driver_number, {})

        merged = {**position, **extra}
        combined_data.append(merged)
    return combined_data

def get_latest_positions(position_data):
    #Fetches latest data on driver's current positions on the grid.
    global latest_position_data

    for position in position_data:
        if "driver_number" not in position or "date" not in position or "position" not in position:
            continue
        
        driver = position["driver_number"]
        position_date = position["date"]
        position_dt = datetime.fromisoformat(position_date.replace("Z", "00:00")) if position_date else None

        if driver in latest_position_data:
            prev_date_str = latest_position_data[driver].get("date")
            prev_dt = datetime.fromisoformat(prev_date_str.replace("Z", "+00:00")) if prev_date_str else None

            if position_dt and prev_dt and position_dt > prev_dt:
                latest_position_data[driver] = position
        else:
            latest_position_data[driver] = position
            
    return list(latest_position_data.values())

def get_starting_positions(position_data):

    global starting_position_data

    for position in position_data:
        if "driver_number" not in position or "date" not in position or "position" not in position:
            continue

        driver = position["driver_number"]
        position_date = position["date"]
        position_dt = datetime.fromisoformat(position_date.replace("Z", "00:00")) if position_date else None

        if driver in starting_position_data:
            prev_date_str = starting_position_data[driver].get("date")
            prev_dt = datetime.fromisoformat(prev_date_str.replace("Z", "+00:00")) if prev_date_str else None

            if position_dt and prev_dt and position_dt < prev_dt:
                starting_position_data[driver] = position
        else:
            starting_position_data[driver] = position
        
    return list(starting_position_data.values())

def get_latest_intervals(interval_data):
    #Fetched latest data on current intervals between drivers.
    global latest_interval_data

    for interval in interval_data:
        if "driver_number" not in interval or "date" not in interval or "interval" not in interval:
            continue

        driver = interval["driver_number"]
        interval_date = interval["date"]
        interval_dt = datetime.fromisoformat(interval_date.replace("Z", "+00:00")) if interval_date else None

        if driver in latest_interval_data:
            prev_date_str = latest_interval_data[driver].get("date")
            prev_dt = datetime.fromisoformat(prev_date_str.replace("Z", "+00:00")) if prev_date_str else None

            if interval_dt and prev_dt and interval_dt > prev_dt:
                latest_interval_data[driver] = interval
        else:
            latest_interval_data[driver] = interval

    return list(latest_interval_data.values())

@position_data_bp.route("/position-data", methods=['GET'])
def get_positions_and_intervals():
    import routes.api_data as api_data
    global positions_data, intervals_data, starting_position_data, positions_and_intervals, initial

    simulated = False
        
    if simulated == True:
        positions_data = simulated_positions_response()
        intervals_data = simulated_intervals_response()
        starting_position_data = simulated_positions_response()

    else:
        if api_data.positions is not None:
            processed_positions = [
                {
                    "date": pos.get("date"),
                    "driver_number": pos.get("driver_number"),
                    "position": pos.get("position")   
                }
                for pos in api_data.positions
            ]

            positions_data = get_latest_positions(processed_positions)

            if initial == True:
                starting_position_data = get_starting_positions(processed_positions)
                initial = False

        if api_data.intervals is not None:
            processed_intervals = [
                {
                    "date": inter.get("date"),
                    "driver_number": inter.get("driver_number"),
                    "gap_to_leader": inter.get("gap_to_leader"),
                    "interval": inter.get("interval")
                }
                for inter in api_data.intervals
            ]
            intervals_data = get_latest_intervals(processed_intervals)

    if positions_data and intervals_data is not None:
        positions_and_intervals = combined_positions_intervals(positions_data, intervals_data)

    return jsonify(positions_and_intervals if positions_and_intervals is not None else {"message": "No position or interval data available yet."})