from flask import Blueprint, jsonify
import requests
import time
import threading
from config import Config
from datetime import datetime
from collections import Counter

stints_bp = Blueprint("stints", __name__)

stint_record = {}

"""

def get_stints():

    global stints, latest_stints

    while True:
        response = requests.get(f"{Config.OPENF1_API_URL}/stints?session_key=latest")

        if response.status_code == 200:
            stints = response.json()

            processed_stints = [
                {
                    "compound": att.get("compound"),
                    "driver_number": att.get("driver_number"),
                    "tyre_age": att.get("tyre_age_at_start") + (att.get("lap_end")-att.get("lap_start"))
                }
                for att in stints
            ]
            
        else:
            time.sleep(5)
            continue

        latest_stints = get_latest_stints(processed_stints)
        time.sleep(5)

threading.Thread(target=get_stints, daemon=True).start()

"""

def get_latest_stints(processed_stints):
    global stint_record

    for stint in processed_stints:
        if "driver_number" not in stint or "lap_end" not in stint or "compound" not in stint:
            continue

        driver= stint["driver_number"]

        if driver not in stint_record:
            stint_record[driver] = stint
        else:
            if stint["lap_end"] > stint_record[driver]["lap_end"]:
                stint_record[driver] = stint
       
    return list(stint_record.values())


@stints_bp.route("/stints", methods=['GET'])
def get_stints_update():
    import routes.api_data as api_data
    
    latest_stints = None
    
    if api_data.stints is not None:
        processed_stints = [
            {   
                "compound": att.get("compound"),
                "driver_number": att.get("driver_number"),
                "lap_end": att.get("lap_end"),
                "tyre_age": (
                    att.get("tyre_age_at_start") + (att.get("lap_end")-att.get("lap_start"))
                    if (att.get("tyre_age_at_start") is not None
                        and att.get("lap_start") is not None
                        and att.get("lap_end") is not None)
                    else None
                )
            }
            for att in api_data.stints
        ]

        latest_stints = get_latest_stints(processed_stints)

        for stint in latest_stints:
            if stint["compound"] == None:
                stint["compound"] = "UNKNOWN" 

    return jsonify(latest_stints if latest_stints is not None else {"message": "No attribute data available yet."})

