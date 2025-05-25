from flask import Blueprint, jsonify
import requests
import time
import threading
from collections import deque
from config import Config
from datetime import datetime
#from extensions import socketio


battles_bp = Blueprint("battles", __name__)

battle_data = []
battle_history = []
existing_battles = []
new_battles = []
battle_record = None


def merge_battle_data(positions, cars, laps):
    global battle_data

    if positions and cars and laps is not None:
        car_dictionary = {entry["driver_number"]: entry for entry in cars}
        lap_dictionary = {driver: {"lap_number": lap} for driver, lap in laps.items()}
        """
        first_dictionary = {entry["driver_number"]: entry for entry in cars}
        second_dictionary = {driver: {"lap_number": lap} for driver, lap in laps.items()}
        """

        battle_data.clear()
        for position in positions:

            driver_number = position["driver_number"]
            car_info = car_dictionary.get(driver_number, {})
            lap_info = lap_dictionary.get(driver_number, {})
            

            merged = {**position, **car_info, **lap_info}

            battle_data.append(merged)
        
    else:
        battle_data.clear()

    return battle_data
    
def detect_battles(battle_data):
    global battle_history, existing_battles, new_battles

    new_battles.clear()
    for record in battle_data:

        interval_value = record.get("interval")

        #May need (isinstance(int, str) and int.endswith("L"))

        if interval_value in [None, "null"] or isinstance(interval_value, str) or "lap_number" not in record:
            continue

        try:
            current_position = int(record["position"])
        except Exception as e:
            print (f"Error converting position to int: {e}")
            continue

        try:
            driver_interval = float(record.get("interval", 999))
        except Exception as e:
            print(f"Error converting interval: {e}")
            continue

        drs_status = record.get("drs")
        battle_condition = False
        if driver_interval < 0.3:
            battle_condition = True
        elif driver_interval < 0.4 and drs_status in {10, 12, 14}:
            battle_condition = True

        driver_ahead = next((r for r in battle_data if int(r.get("position", 999)) == current_position-1), None)
        if driver_ahead is None:
            continue
        
        battle_key = {
            "lap_number": int(record.get("lap_number")),
            "driver_number": int(record.get("driver_number")),
            "driver_ahead_number": int(driver_ahead.get("driver_number"))
        }

        small_battle_key = {
            "driver_number": int(record.get("driver_number")),
            "driver_ahead_number": int(driver_ahead.get("driver_number"))
        }

        if battle_condition:
            if small_battle_key not in existing_battles:
                new_battles.append(battle_key)
                existing_battles.append(battle_key)

                if battle_key not in battle_history:
                    battle_history.append(battle_key)
        else:
            if small_battle_key in existing_battles:
                print(f"reached 1 - interval: {driver_interval}")
                if driver_interval > 0.8:
                    print(f"battle_key: {battle_key}")
                    existing_battles.remove(battle_key)
                    print(f"existing_battles: {existing_battles}")

        if battle_history is not None:
            battle_history = format_battle_data(battle_history)

    return battle_history

def format_battle_data(battles):
    from routes.drivers import get_driver_list
    driver_list = get_driver_list()

    data = []

    if battles is not None and driver_list is not None:
        
        processed_driver_list = [
            {
                "driver_number": driver.get("driver_number"),
                "name_acronym": driver.get("name_acronym")
            }
            for driver in driver_list
        ]

        driver_dictionary = {entry["driver_number"]: entry for entry in processed_driver_list}

        for battle in battles:
            driver_number = battle["driver_number"]
            driver_ahead_number = battle["driver_ahead_number"]
            attacking_driver_info = driver_dictionary.get(driver_number, {})
            driver_ahead_info = driver_dictionary.get(driver_ahead_number, {})

            driver_ahead_renamed = {
                f"ahead_{key}": val
                for key, val in driver_ahead_info.items()
                if key != "driver_number"
            }

            merged = {**battle, **attacking_driver_info, **driver_ahead_renamed}
            data.append(merged)

        return data

def emit_battles():
    #Returns detected battles.

    from routes.position_data import positions_and_intervals
    from routes.car_data import latest_car_data
    from routes.laps import current_laps

    global battle_record

    formatted_new_battles = []

    if positions_and_intervals and latest_car_data and current_laps is not None:
        merged_data = merge_battle_data(positions_and_intervals, latest_car_data, current_laps)
        battle_record = detect_battles(merged_data)

    if new_battles:
        formatted_new_battles = format_battle_data(new_battles)

    return formatted_new_battles

@battles_bp.route('/ongoing-battles', methods=['GET'])
def get_ongoing_battles():

    global existing_battles

    """existing_battles = [
            {"driver_number": 4,
             "name_acronym": "NOR",
             "driver_ahead_number": 44,
             "ahead_name_acronym": "HAM",
             "lap_number": 12
            },
            {"driver_number": 16,
             "name_acronym": "LEC",
             "driver_ahead_number": 1,
             "ahead_name_acronym": "VER",
             "lap_number": 14
            }
        ]"""
    return jsonify(existing_battles if existing_battles else {"message": "No battles currently taking place"})

@battles_bp.route('/battles', methods=['GET'])
def get_battle_data():

    global battle_record

    """if battle_record is None:
        battle_record = [
            {"driver_number": 4,
             "name_acronym": "NOR",
             "driver_ahead_number": 44,
             "ahead_name_acronym": "HAM",
             "lap_number": 12
            },
            {"driver_number": 16,
             "name_acronym": "LEC",
             "driver_ahead_number": 1,
             "ahead_name_acronym": "VER",
             "lap_number": 14
            },
            {"driver_number": 87,
             "name_acronym": "BEA",
             "driver_ahead_number": 20,
             "ahead_name_acronym": "DOO",
             "lap_number": 18
            }
        ]
"""
    return jsonify(battle_record if battle_record else {"message": "No battles yet."})

