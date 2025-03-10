from extensions import socketio
from flask_socketio import emit

@socketio.on('connect')
def handle_connect():
    print("Client connected")

@socketio.on('message')
def handle_message(data):
    print(f"Message received in Flask console: {data}")  # Print to console only
    # No emit here to prevent looping messages back
