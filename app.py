from flask import Flask,render_template,url_for,Blueprint
app = Flask(__name__)
from auth import auth_bp,init_auth_socket
from flask_socketio import SocketIO,emit

socketio = SocketIO(app)

app.register_blueprint(auth_bp)

init_auth_socket(socketio)

if __name__ == "__main__":
    socketio.run(app=app,ssl_context="adhoc",debug=True)