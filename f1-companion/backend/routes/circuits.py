from flask import Blueprint, jsonify
import json
from models import Circuit, db

circuits_bp = Blueprint("circuits", __name__)

@circuits_bp.route("/import-preseason-circuits", methods=['POST'])  
def import_circuits_preseason():
    """Imports manually prepared circuit data for 2025"""
    try:
        with open('data/circuits_2025.json', 'r') as file:
            data = json.load(file)

        added_count = 0
        updated_count = 0

        for circuit in data:
            added, updated = process_circuit_data(circuit)
            added_count += added
            updated_count += updated
        
        db.session.commit()

        return jsonify({
            "message": "preseason circuit data imported.",
            "circuits_added": added_count,
            "circuits_updated": updated_count
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@circuits_bp.route("/circuits", methods=['GET'])
def get_circuits():

    circuits = Circuit.query.all()
    circuit_list = [
        {
            "country_name": circuit.country_name,
            "location": circuit.location,
            "session_name": circuit.session_name,
            "date_time_local": circuit.date_time_local,
            "date_time_gmt": circuit.date_time_gmt,
            "meeting_official_name": circuit.meeting_official_name,
            "year": circuit.year
        }
        for circuit in circuits
    ]
    return jsonify(circuit_list)                                       

def process_circuit_data(circuit):
    """Handles adding or updating a circuit in the database."""
    country_name=circuit["country_name"]
    location=circuit["location"]
    session_name=circuit["session_name"]
    date_time_local=circuit["date_time_local"]
    date_time_gmt=circuit["date_time_gmt"]
    meeting_official_name=circuit["meeting_official_name"]
    year=circuit["year"]

    print(f"Checking circuit: {location} - {session_name} - {year}")

    existing_circuit = Circuit.query.filter(
        Circuit.location == location,
        Circuit.session_name == session_name,
        Circuit.year == year
    ).first()

    if not existing_circuit:
        new_circuit = Circuit(
            country_name=country_name,
            location=location,
            session_name=session_name,
            date_time_local=date_time_local,
            date_time_gmt=date_time_gmt,
            meeting_official_name=meeting_official_name,
            year=year
        )
        db.session.add(new_circuit)
        db.session.commit()
        return 1, 0
    
    updated_fields = {
        "country_name": country_name,
        "date_time_local": date_time_local,
        "date_time_gmt": date_time_gmt,
        "meeting_official_name": meeting_official_name
    }

    if any(str(getattr(existing_circuit, key)) != str(value) for key, value in updated_fields.items()):
        for key, value in updated_fields.items():
            setattr(existing_circuit, key, value)

        db.session.commit()
        return 0, 1
    
    return 0, 0