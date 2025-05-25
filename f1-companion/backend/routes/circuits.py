from flask import Blueprint, jsonify
import json, requests, time
from models import Circuit, db
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from config import Config

circuits_bp = Blueprint("circuits", __name__)

circuit_list = None
circuit_data = None

london = ZoneInfo("Europe/London")

def load_circuit_data(reload=False):

    global circuit_data
    if reload or circuit_data is None:
        try:
            with open('data/circuits_2025.json', 'r') as file:
                circuit_data = json.load(file)
        except Exception as e:
            circuit_data = []
    return circuit_data

def get_circuit_list(reload=False):
    return load_circuit_data(reload)

def add_race_status(list):

    current_date = datetime.now(tz=london)

    for race in list:
        try:
            race_date = datetime.strptime(race["date_time_gmt"], '%Y-%m-%d %H:%M:%S')
            race_date = race_date.replace(tzinfo=london)
        except Exception as e:
            "Couldn't convert string to date"

        if current_date > (race_date + timedelta(hours=3)):
           race["status"] = "past"
        elif current_date < (race_date - timedelta(hours=1)):
            race["status"] = "future"
        else:
            race["status"] = "current"

    return list

def add_winner_data(list_status):
    from routes.drivers import get_driver_list
    driver_list = get_driver_list()

    complete_circuits = []

    if driver_list and list_status is not None:
        driver_dictionary = {entry["driver_number"]: entry for entry in driver_list}

        for race in list_status:
            driver_number = race["winner"]
            driver_info = driver_dictionary.get(driver_number, {})

            merged = {**race, **driver_info}
            complete_circuits.append(merged)

    return complete_circuits

@circuits_bp.route("/circuits", methods=['GET'])
def get_circuits():
    global circuit_list

    print("circuit route called!")
    current_circuit_list = get_circuit_list()

    if current_circuit_list is not None:
        circuit_list_status = add_race_status(current_circuit_list)
        circuit_list = add_winner_data(circuit_list_status)

    return jsonify(circuit_list)

@circuits_bp.route("/import-preseason-circuits", methods=['POST'])
def import_circuits_preseason():
    #Imports manually prepared circuit data for 2025
    try:
        data = load_circuit_data(reload=True)
        updated_count = 0

        for circuit in data:
            updated = process_circuit_data(circuit)
            updated_count += updated

        db.session.commit()

    except Exception as e:
        return jsonify({
            "message": "Preseason circuit data imported.",
            "circuits updated": updated_count
        })

def process_circuit_data(circuit):
    #Handles adding or updating a circuit in the database

    try:
        circuit_instance = Circuit(
            country_name=circuit["country_name"],
            location=circuit["location"],
            session_name=circuit["session_name"],
            date_time_local=circuit["date_time_local"],
            date_time_gmt=circuit["date_time_gmt"],
            meeting_official_name=circuit["meeting_official_name"],
            year=circuit["year"]
        )

        merged = db.session.merge(circuit_instance)

        return 1
    except Exception as e:
        print(f"Error processing circuit data: {e}")
        return 0