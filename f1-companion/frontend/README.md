# F1 Race Weekend Companion
## Description
A web-based application that delivers live Formula 1 race data straight to your brower, powered by the OpenF1 API. Designed to improve the fan experience during race weekends with real-time insights and statistics.
## Table of Contents
1.	[Demo](#demo)
2.	[Features](#features)
3.	[Technologies Used](#technologies-used)
4.	[Getting Started](#getting-started)
  -	[Prerequisites](#prerequisites)
  -	[Back End Setup](#back-end-setup)
  -	[Front End Setup](#front-end-setup)
  -	[Configuration](#configuration)
5.	[Running the App](#running-the-app)
6. [API & Websocket Reference](#api--websocket-reference)
  - [REST Endpoints](#rest-endpoints)
  - [Socketio Events](#socketio-events)
7. [Acknowledgements](#acknowledgements)

## Demo
WIP
## Features
- **Live Leaderboard** with positions and intervals.
- **Battle Detection** notifications and history.
- **Pit Stop** notices and statistics.
- **Race Control** messages including driver penalties and safety cars.
- **Fastest Lap** tracker and alerts.
- **Full-Stack**: Flask + PostgreSQL backend, React + Tailwind frontend, Socket.IO real-time updates.
## Technologies Used
**Back End:**
-	Python 3.10+, Flask, Flask-SocketIO, SQLAlchemy, Flask-Migrate
-	PostgreSQL
-	[OpenF1 API](https://api.openf1.org/) for live race data
  
**Front End:**
-	React 18, React Router, Socket.IO-client
-	Tailwind CSS
## Getting Started
### Prerequisites
-	[Python 3.10+](https://www.python.org/downloads/)
-	[Node.js 16+](https://nodejs.org/) 
-	PostgreSQL
### Back End Setup
1.	Clone repository & enter backend folder
```bash
   git clone https://github.com/SamanthaMT/f1-companion.git
   cd f1-companion/backend
```
2.	Create virtual environment
```bash
  python -m venv env
```
3.	Install Python dependencies
```bash
pip install -r requirements.txt
```
4.	Set up database
```bash
createdb f1_companion
flask db upgrade
```
### Front End Setup
1.	In a new terminal, go to the frontend folder
```bash
cd frontend
```
2.	Install npm packages
```bash
npm install
```
### Configuration
Add postgreSQL credentials into config.pg
```
DB_USER = os.getenv("POSTGRES_USER", "username")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
```
## Running the App
1.	Start the Flask server
```bash
cd backend

source venv/bin/activate       (Linux/maxOS)
venv\Scripts\activate          (Windows)

python app.py
```
2.	Start the React server
```bash
cd frontend
npm start
```
3.	Visit http://localhost:3000
## API & WebSocket Reference
### REST endpoints:
```
GET /battles
GET /ongoing-battles
GET /car-data
GET /circuits
GET /laps
GET /leaderboard
GET /race-story
GET /pits
GET /position-data
GET /race-control
GET /stints
GET /weather
```
### Socket.IO events
```
socket.on(“fastest_lap_update”)
socket.on(“pit_stop_update”)
socket.on(“race_control_update”)
socket.on(“battle_update”)
socket.on(“leader_update”)
```
## Acknowledgements
OpenF1 API for live Formula 1 data and the open-source contributors.
