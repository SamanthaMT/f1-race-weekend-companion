import requests, time, threading
from config import Config
from flask import current_app
from datetime import datetime, timedelta, timezone

car_data = None
laps = None
pits = None
positions = None
intervals = None
race_control = None
stints = None
weather = None


def poll_api_3secs():
     from app import socketio
     global car_data, positions, intervals
     while True:
          date = datetime.now(timezone.utc) - timedelta(seconds=60)
          date_filter = date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]

          #For testing
          response = requests.get(f"{Config.OPENF1_API_URL}/car_data?session_key=latest&date>{date_filter}") 
          #response = requests.get(f"{Config.OPENF1_API_URL}/car_data?session_key=latest&date>2025-04-12T17:10:22.627")  
          if response.ok:
               car_data = response.json()
          else:
               print(f"Live car data API call failed. Code: {response.status_code}")     

          socketio.sleep(1)

          response = requests.get(f"{Config.OPENF1_API_URL}/position?session_key=latest")
          if response.ok:
               positions = response.json()
          else:
               print(f"Live position API call failed. Code: {response.status_code}")

          socketio.sleep(1)

          response = requests.get(f"{Config.OPENF1_API_URL}/intervals?session_key=latest")
          if response.ok:
               intervals = response.json()
          else:
               print(f"Live interval API call failed. Code: {response.status_code}")
        
          socketio.sleep(5)
                     
def poll_api_15secs():
     from app import socketio
     global laps, pits, race_control, stints
     while True:

          response = requests.get(f"{Config.OPENF1_API_URL}/laps?session_key=latest")
          if response.ok:
               laps = response.json()
          else:
               print(f"Live lap API call failed. Code: {response.status_code}")

          socketio.sleep(1)

          response = requests.get(f"{Config.OPENF1_API_URL}/pit?session_key=latest")
          if response.ok:
               pits = response.json()
          else:
               print(f"Live pit API call failed. Code: {response.status_code}")

          socketio.sleep(1)

          response = requests.get(f"{Config.OPENF1_API_URL}/race_control?session_key=latest")
          if response.ok:
               race_control = response.json()
          else:
               print(f"Live race control API call failed. Code: {response.status_code}")
          
          socketio.sleep(1)

          response = requests.get(f"{Config.OPENF1_API_URL}/stints?session_key=latest")
          if response.ok:
               stints = response.json()
          else:
               print(f"Live stints API call failed. Code: {response.status_code}")

          socketio.sleep(15)

def poll_api_240secs():
     from app import socketio
     global weather
     while True:
          response = requests.get(f"{Config.OPENF1_API_URL}/weather?session_key=latest")
          if response.ok:
               weather = response.json()
          else:
               print(f"Live weather API call failed. Code: {response.status_code}")

          socketio.sleep(240)

def start_polling():
     from app import socketio
     print("Starting the API data retrieval thread")
     socketio.start_background_task(poll_api_3secs)
     socketio.start_background_task(poll_api_15secs)
     socketio.start_background_task(poll_api_240secs)