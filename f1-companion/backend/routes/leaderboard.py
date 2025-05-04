from flask import Blueprint, jsonify
from datetime import datetime, timedelta

leaderboard_bp = Blueprint("leaderboard", __name__)

combined_data = []
leader = None

def merge_driver_position_data():
    from routes.drivers import get_driver_list
    driver_list = get_driver_list()
    from routes.position_data import positions_and_intervals, starting_position_data

    if positions_and_intervals is not None and driver_list is not None:

        processed_starting_positions = [
            {
                "driver_number": driver.get("driver_number"),
                "starting_position": driver.get("position")
            }
            for driver in starting_position_data
        ]

        driver_dictionary = {entry["driver_number"]: entry for entry in driver_list}
        starting_dictionary = {entry["driver_number"]: entry for entry in processed_starting_positions}

        combined_data.clear()
        for pos in positions_and_intervals:
            driver_number = pos["driver_number"]
            driver_info = driver_dictionary.get(driver_number, {})
            starting_info = starting_dictionary.get(driver_number, {})

            merged = {**pos, **driver_info, **starting_info}
            combined_data.append(merged)

        return combined_data
    
def dnf_check(data):
    
    latest_dt = None
    
    if data:   
        latest_record = max(data, key=lambda rec: datetime.fromisoformat(rec["date"].replace("Z", "+00:00")))
        latest_dt = datetime.fromisoformat(latest_record["date"].replace("Z", "+00:00"))
        threshold = latest_dt - timedelta(minutes=3)
    
        for driver in data:
            driver_date = driver.get("date")
            if driver_date is None:
                continue

            driver_dt = datetime.fromisoformat(driver_date.replace("Z", "00:00")) if driver_date else None

            if driver_dt < threshold:
                driver["interval"] = "DNF"
                driver["gap_to_leader"] = "DNF"

    return data
    
def process_story_data(story_data):

    if story_data is not None:

        processed_story = [
            {
                "driver_number": driver.get("driver_number"),
                "name_acronym": driver.get("name_acronym"),
                "position": driver.get("position"),
                "starting_position": driver.get("starting_position"),
                "position_change": driver.get("starting_position")-driver.get("position")
            }
            for driver in story_data
        ]

        for driver in processed_story:
            if driver["position_change"] == 0:
                driver["position_change"] = "--"
            elif driver["position_change"] > 0:
                driver["position_change"] = f"+{driver["position_change"]}"

        return processed_story
    
def emit_new_leader():

    global merged_data, leader

    temp_leader = None
    new_leader_alert = []

    #Merge driver data with positions and interval data
    merged_data = merge_driver_position_data()

    #Check if there is a new race leader
    if merged_data is not None:
        try:
            temp_leader = next((driver for driver in merged_data if driver.get("position")==1), None)
        except Exception as e:
            print("Missing data for driver running in first position.")
    if temp_leader is not None:
        if leader is None or leader != temp_leader:
            leader = temp_leader.copy()
            new_leader_alert.append(leader)

    return new_leader_alert 
        
@leaderboard_bp.route("/leaderboard", methods=['GET'])
def get_leaderboard():
    global merged_data

    leaderboard_data = dnf_check(merged_data)

    return jsonify(leaderboard_data if leaderboard_data is not None else {"message": "No leaderboard data recorded yet."})

@leaderboard_bp.route("/race-story", methods=['GET'])
def get_race_story():

    story_data = merge_driver_position_data()

    race_story_data = process_story_data(story_data)

    return jsonify(race_story_data if race_story_data is not None else {"message": "No race story data recorded yet."})

