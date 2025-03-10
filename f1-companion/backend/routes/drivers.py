from flask import Blueprint, jsonify
import json
import requests
from config import Config
from models import Driver, db

drivers_bp = Blueprint("drivers", __name__)

@drivers_bp.route("/import-preseason-drivers", methods=['POST'])
def import_drivers_preseason():
    """Imports manually prepared driver data for 2025"""
    try:
        with open('data/drivers_2025.json', 'r') as file:
            data = json.load(file)

        added_count = 0
        updated_count = 0

        for driver in data:
            added, updated = process_driver_data(driver)
            added_count += added
            updated_count += updated

        db.session.commit()

        return jsonify({
        "message": "Preseason driver data imported.",
        "drivers_added": added_count,
        "drivers_updated": updated_count
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@drivers_bp.route("/drivers", methods=['GET'])
def get_drivers():

    drivers = Driver.query.all()
    driver_list = [
        {
            "driver_number": driver.driver_number,
            "full_name": driver.full_name,
            "team_name": driver.team_name,
            "team_colour": driver.team_colour,
            "headshot_url": driver.headshot_url,
            "name_acronym": driver.name_acronym,
            "country_code": driver.country_code
        }
        for driver in drivers
    ]
    return jsonify(driver_list)

def process_driver_data(driver):
    """Handles adding or updating a driver in the database."""
    country_code=driver["country_code"]
    driver_number=driver["driver_number"]
    full_name=driver["full_name"]
    headshot_url=driver["headshot_url"]
    last_name=driver["last_name"]
    name_acronym=driver["name_acronym"]
    team_colour=driver["team_colour"]
    team_name=driver["team_name"]

    print(f"Checking driver: {driver_number} - {full_name} - {team_name}")

    existing_driver = Driver.query.filter_by(full_name=full_name).first()

    if not existing_driver:

        db.session.add(Driver(
            country_code=country_code,
            driver_number=driver_number,
            full_name=full_name,
            headshot_url=headshot_url,
            last_name=last_name,
            name_acronym=name_acronym,
            team_colour=team_colour,
            team_name=team_name
        ))
        return 1,0
    
    updated_fields = {
        "driver_number": driver_number,
        "headshot_url": headshot_url,
        "team_colour": team_colour,
        "team_name": team_name
    }

    if any(getattr(existing_driver, key) != value for key, value in updated_fields.items()):
        for key, value in updated_fields.items():
            setattr(existing_driver, key, value)
        return 0, 1
    
    return 0, 0
"""Might remove this
@drivers_bp.route('/api/update-drivers-race-start', methods=['GET'])
def update_drivers_race_start():
    #Checks for updates to driver data at the start of race and updates accordingly.
    response = requests.get(f"{Config.OPENF1_API_URL}/drivers?session_key=latest")
    data = response.json()

    added_count = 0
    updated_count = 0
    
    for driver in data:
        added, updated = process_driver_data(driver)
        added_count += added
        updated_count += updated

    db.session.commit()

    return jsonify({
        "message": "Driver data checked and updated if needed.",
        "drivers_added": added_count,
        "drivers_updated": updated_count
    })
"""