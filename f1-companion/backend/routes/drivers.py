from flask import Blueprint, jsonify, request
import json
from config import Config
from models import Driver, db

drivers_bp = Blueprint("drivers", __name__)

driver_list = None
driver_data = None

def load_driver_data(reload=False):

    global driver_data
    if reload or driver_data is None:
        try:
            with open('data/drivers_2025.json', 'r') as file:
                driver_data = json.load(file)

        except Exception as e:
            driver_data = []
    return driver_data

def get_driver_list(reload=False):
    return load_driver_data(reload)

@drivers_bp.route("/drivers", methods=['GET'])
def get_drivers():
    driver_list = get_driver_list()
    return jsonify(driver_list)

@drivers_bp.route("/import-preseason-drivers", methods=['POST'])
def import_drivers_preseason():
    #Imports manually prepared driver data for 2025
    try:
        data = load_driver_data(reload=True)
        updated_count = 0

        for driver in data:
            updated = process_driver_data(driver)
            updated_count +=updated

        db.session.commit()

        return jsonify({
        "message": "Preseason driver data imported.",
        "drivers updated": updated_count
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def process_driver_data(driver):
    #Handles adding or updating a driver in the database.

    try:
        driver_instance = Driver(
            country_code=driver["country_code"],
            driver_number=driver["driver_number"],
            full_name=driver["full_name"],
            headshot_url=driver["headshot_url"],
            last_name=driver["last_name"],
            name_acronym=driver["name_acronym"],
            team_colour=driver["team_colour"],
            team_name=driver["team_name"]
        )

        merged = db.session.merge(driver_instance)
    
        return 1
    except Exception as e:
        print(f"Error processing driver data: {e}")
        return 0