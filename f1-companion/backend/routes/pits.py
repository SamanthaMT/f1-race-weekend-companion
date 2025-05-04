from flask import Blueprint, jsonify
import requests
from config import Config
import time
import threading
import os
import json
from collections import Counter

pits_bp = Blueprint("pits", __name__)

complete_pit_record = None

new_pit_stop_alert = []
pit_record = {}

def check_new_pits(processed_pits):
    global new_pit_stop_alert, pit_record

    new_pit_stop_alert.clear()
    for stop in processed_pits:
        if "driver_number" not in stop or "lap_number" not in stop or "pit_duration" not in stop or "date" not in stop or "pit_stops" not in stop:
            continue
                
        driver = stop["driver_number"]

        if driver not in pit_record:
            pit_record[driver] = stop
            new_pit_stop_alert.append(stop)
        else:
            if stop["lap_number"] > pit_record[driver]["lap_number"]:
                pit_record[driver] = stop
                new_pit_stop_alert.append(stop)

    return list(pit_record.values())

def merge_pit_data(pit_record):
    from routes.drivers import get_driver_list
    driver_list = get_driver_list()
    from routes.stints import stint_record
    latest_stints = list(stint_record.values())

    pit_data = []

    if driver_list and pit_record and latest_stints is not None:
        driver_dictionary = {entry["driver_number"]: entry for entry in driver_list}
        stints_dictionary = {entry["driver_number"]: entry for entry in latest_stints}

        pit_data.clear()
        for record in pit_record:
            driver_number = record["driver_number"]
            driver_info = driver_dictionary.get(driver_number, {})
            stints_info = stints_dictionary.get(driver_number, {})

            merged = {**record, **driver_info, **stints_info}
            pit_data.append(merged)

        return pit_data
    
def emit_pits():
    import routes.api_data as api_data
    global complete_pit_record, new_pit_stop_alert

    if api_data.pits is not None:
        processed_pits = [
            {
                "driver_number": pit.get("driver_number"),
                "pit_duration": pit.get("pit_duration"),
                "lap_number": pit.get("lap_number"),
                "date": pit.get("date")
            }
            for pit in api_data.pits
        ]
        
        pit_stop_counter = Counter(pit["driver_number"] for pit in processed_pits)

        for pit in processed_pits:
            pit["pit_stops"] = pit_stop_counter[pit["driver_number"]]

        #Condense pit data into one entry for each driver
        pit_record = check_new_pits(processed_pits)

        #Merge pit data with driver and tyre info
        complete_pit_record = merge_pit_data(pit_record)
        if new_pit_stop_alert:
            new_pit_stop_alert = merge_pit_data(new_pit_stop_alert)
    
    return new_pit_stop_alert
            

@pits_bp.route("/pits", methods=['GET'])
def get_pits():

    return jsonify(complete_pit_record if complete_pit_record is not None else {"message": "No pits recorded yet."})
        

    
    
