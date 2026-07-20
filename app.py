from flask import Flask,render_template,url_for,Blueprint
app = Flask(__name__)
from auth import auth_bp,init_auth_socket
from flask_socketio import SocketIO,emit
from structure import init_db
from main import main_bp

socketio = SocketIO(app)
init_db()
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)


init_auth_socket(socketio)

if __name__ == "__main__":
    socketio.run(app=app,ssl_context="adhoc",debug=True)