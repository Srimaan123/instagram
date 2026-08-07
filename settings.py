from flask import Blueprint,render_template,redirect,request
import sqlite3
from flask_socketio import emit

settings_bp = Blueprint("settings",__name__)

@settings_bp.route("/settings/<username>")
def settings(username):
    with sqlite3.connect("data.db") as conn:
        cursor = conn.cursor()
        is_private = cursor.execute("select is_private from users where username=?",(username,)).fetchone()[0]
        followers = len(cursor.execute("select id from requests where requested_to=? and is_accepted='True'",(username,)).fetchall())
        following = len(cursor.execute("select id from requests where requested_by=? and is_accepted='True'",(username,)).fetchall())
    accountType = []
    if is_private == 'True':
        accountType.append('Private')
        accountType.append('Public')
    else:
        accountType.append('Public')
        accountType.append('Private')
        
    return render_template("settings.html",following=following,username=username,accountType=accountType,followers=followers)

def settings_api(socketio):
    @socketio.on("changeAccountType")
    def changeAccountType(data):
        username = data.get("username")
        account_type = data.get("accType")
        print(account_type)
        if account_type == "Private":
            account_type = 'True'
        else:
            account_type = 'False'

        with sqlite3.connect('data.db') as conn:
            cur = conn.cursor()
            cur.execute("update users set is_private=? where username=?",(account_type,username))
            conn.commit()