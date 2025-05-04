from flask import Blueprint, jsonify
import requests
from collections import deque
import time
import threading
from config import Config
from datetime import datetime

car_data_bp = Blueprint("car_data", __name__)

latest_car_data = {}
car_data_record = {}

def get_latest_car_data(car_data):
    global car_data_record
    
    for car in car_data:

        if "driver_number" not in car or "drs" not in car or "date" not in car:
            continue

        driver = car["driver_number"]
        car_date = car["date"]
        car_dt = datetime.fromisoformat(car_date.replace("Z", "00:00")) if car_date else None

        if driver in car_data_record:
            prev_date_str = car_data_record[driver].get("date")
            prev_dt = datetime.fromisoformat(prev_date_str.replace("Z", "+00:00")) if prev_date_str else None

            if car_dt and prev_dt and car_dt > prev_dt:
                car_data_record[driver] = car
        else:
            car_data_record[driver] = car

    return list(car_data_record.values())


@car_data_bp.route("/car-data", methods=['GET'])
def get_car_data():
    global latest_car_data
    import routes.api_data as api_data
    #from routes.api_data import car_data
    latest_car_data = None

    if api_data.car_data is not None:
        processed_cars = [
            {
                "driver_number": car.get("driver_number"),
                "drs": car.get("drs"),
                "date": car.get("date")
            }
            for car in api_data.car_data
        ]

        latest_car_data = get_latest_car_data(processed_cars)

    return jsonify(latest_car_data if latest_car_data is not None else {"message": "No car data available yet."})
    

