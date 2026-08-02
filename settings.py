from flask import Blueprint,render_template,redirect,request
import sqlite3
from flask_socketio import emit

settings_bp = Blueprint("settings",__name__)

@settings_bp.route("/settings/<username>")
def settings(username):
    with sqlite3.connect("data.db") as conn:
        cursor = conn.cursor()
        is_private = cursor.execute("select is_private from users where username=?",(username,)).fetchone()
    accountType = []
    if is_private == 'True':
        accountType.append('Private')
        accountType.append('Public')
    else:
        accountType.append('Public')
        accountType.append('Private')
        
    return render_template("settings.html",username=username,accountType=accountType)

