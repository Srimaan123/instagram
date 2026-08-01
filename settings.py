from flask import Blueprint,render_template,redirect,request
import sqlite3
from flask_socketio import emit

settings_bp = Blueprint("settings",__name__)

@settings_bp.route("/settings/<username>")
def settings(username):
    return render_template("settings.html",username=username)

