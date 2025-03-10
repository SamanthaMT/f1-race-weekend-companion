from flask import Flask
from extensions import socketio  # Import socketio from the separate file
from config import Config
from flask_cors import CORS
from database import init_db, db
from config import Config
from flask_migrate import Migrate
from flask_caching import Cache


# Initialise Flask
app = Flask(__name__, template_folder="../frontend/templates")
app.config.from_object(Config)
CORS(app, resources={r"/*": {"origins": "*"}})

#Initialise extensions
init_db(app)
migrate = Migrate(app, db)
socketio.init_app(app)
cache = Cache(app)

# Import and register blueprints
def register_blueprints():
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

register_blueprints()

import socket_events  # Import WebSocket events after app is initialized

if __name__ == "__main__":
    socketio.run(app, debug=True)
