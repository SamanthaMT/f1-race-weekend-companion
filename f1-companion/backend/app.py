import eventlet
eventlet.monkey_patch()

from flask import Flask, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_caching import Cache

from flask_socketio import SocketIO, emit

from config import Config
from database import init_db, db
from routes.api_data import start_polling

def create_app():
    # Initialise Flask
    app = Flask(__name__, template_folder="../frontend/templates")
    app.config.from_object(Config)
    CORS(app, resources={r"/*": {"origins": "*"}})

    #Initialise extensions
    init_db(app)
    Migrate(app, db)
    Cache(app)

# Import and register blueprints
    from routes.index import index_bp
    from routes.test_route import test_bp
    from routes.laps import laps_bp
    from routes.pits import pits_bp
    from routes.race_control import race_control_bp
    from routes.circuits import circuits_bp
    from routes.drivers import drivers_bp
    from routes.car_data import car_data_bp
    from routes.weather import weather_bp
    from routes.battles import battles_bp
    from routes.leaderboard import leaderboard_bp
    from routes.position_data import position_data_bp
    from routes.stints import stints_bp

    app.register_blueprint(index_bp)
    app.register_blueprint(test_bp)
    app.register_blueprint(laps_bp)
    app.register_blueprint(pits_bp)
    app.register_blueprint(race_control_bp)
    app.register_blueprint(circuits_bp)
    app.register_blueprint(drivers_bp)
    app.register_blueprint(car_data_bp)
    app.register_blueprint(weather_bp)
    app.register_blueprint(battles_bp)
    app.register_blueprint(leaderboard_bp)
    app.register_blueprint(position_data_bp)
    app.register_blueprint(stints_bp)

    return app

app = create_app()

socketio = SocketIO(
    app,
    async_mode="eventlet",
    cors_allowed_origins="*"
)


@socketio.on("connect")
def on_connect():
    print(f"SOCKET.IO: Client connected -> sid={request.sid}")

#Socketio Alerts
def alert_dispatcher():

    from datetime import datetime, timezone

    from routes.race_control import emit_race_control
    from routes.pits import emit_pits
    from routes.laps import emit_fastest_lap
    from routes.battles import emit_battles
    from routes.leaderboard import emit_new_leader

    while True:

        for event_name, fn in [
            ("race_control_update", emit_race_control),
            ("pit_stop_update", emit_pits),
            ("fastest_lap_update", emit_fastest_lap),
            ("battle_update", emit_battles),
            ("leader_update", emit_new_leader)
        ]:
            try:
                new = fn()
                if new:
                    socketio.emit(event_name, new)
            except Exception as e:
                print(f"{event_name} dispatch failed:", e)

        socketio.sleep(2)


if __name__ == "__main__":
    start_polling()
    socketio.start_background_task(alert_dispatcher)

    socketio.run(app, host="0.0.0.0", port=5000, debug=False, use_reloader=False)
