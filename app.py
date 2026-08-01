from flask import Flask,render_template,url_for,Blueprint
app = Flask(__name__)
from auth import auth_bp,init_auth_socket
from flask_socketio import SocketIO,emit
from structure import init_db
from main import main_bp
from search import search_for_user,search_bp
from notifications import notifications_bp
from settings import settings_bp

socketio = SocketIO(app)
init_db()
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(search_bp)
app.register_blueprint(notifications_bp)
app.register_blueprint(settings_bp)

init_auth_socket(socketio)
search_for_user(socketio)

if __name__ == "__main__":
    socketio.run(app=app,ssl_context="adhoc",debug=True)