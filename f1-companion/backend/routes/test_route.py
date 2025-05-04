from flask import Blueprint, render_template
#from extensions import socketio

test_bp = Blueprint('test', __name__)

@test_bp.route("/test")
def test():
    print("Test page visited! Sending message to Flask console...")
    #socketio.emit('message', "Test page reached")  # Send message to Flask console
    return render_template("index.html")
