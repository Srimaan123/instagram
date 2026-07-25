from flask import Blueprint,render_template,redirect,request
from flask_socketio import emit
import sqlite3
search_bp = Blueprint("search",__name__)

@search_bp.route("/search/<username>")
def search_for(username):
    return render_template("search.html",username=username)

def search_for_user(socketio):
    @socketio.on("search")
    def search(data):
        text = f'%{data.get("text")}%'
        username = data.get("username")
        with sqlite3.connect("data.db") as conn:
            cursor = conn.cursor()
            users = cursor.execute("select username from users where username like ?",(text,)).fetchall()
            request_from_user = cursor.execute("select * from requests where requested_by=?",(username,)).fetchall()
            is_requested = []
            for i in request_from_user:
                if i[1] in users:
                    is_requested.append('True')
                else:
                    is_requested.append('False')
            
            if users:
                emit("search_result",{"users": users,"is_requested": is_requested})
