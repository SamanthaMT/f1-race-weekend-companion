from flask import Blueprint, jsonify
import json
from models import Circuit, db

circuits_bp = Blueprint("circuits", __name__)

circuit_list = None
circuit_data = None

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

@circuits_bp.route("/circuits", methods=['GET'])
def get_circuits():
    circuit_list = get_circuit_list()
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