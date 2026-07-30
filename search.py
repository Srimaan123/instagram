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
            users = cursor.execute("select username from users where username like ?",(text,)).fetchone()
            request_from_user = cursor.execute("select * from requests where requested_by=?",(username,)).fetchall()
            print(request_from_user)
            is_requested = []
            is_followed = []
            is_rejected = []
            for i in users:
                if request_from_user == []:
                    is_requested.append('False')
                for j in request_from_user:
                    if i in j:
                        is_requested.append("True")
                    
                    else:
                        is_requested.append("False")
                    if i == j[0] and j[2] == 'True':
                        is_followed.append('True')
                    else:
                        is_followed.append('False')
                    if i == j[0] and j[3] == 'True':
                        is_rejected.append('True')
                    else:
                        is_rejected.append('False')

            if users:
                
                emit("search_result",{"users": users,
                                      "is_requested": is_requested,
                                      "is_followed": is_followed,
                                      "is_rejected": is_rejected})
    @socketio.on("request")
    def request_or_follow(data):
        requested_by = data.get("requested_by")
        requested_to = data.get("requested_to")
        print(requested_to)
        with sqlite3.connect("data.db") as conn:
            cursor = conn.cursor()
            is_private = cursor.execute("select is_private from users where username=?",(requested_to,)).fetchone()
            if is_private == 'True':
                cursor.execute("insert into requests(requested_by,requested_to,is_accepted,is_rejected,is_seen) values(?,?,'False','False','False')",(requested_by,requested_to))
                socketio.emit("requested",{"requested_to": requested_to})
            else:
                cursor.execute("insert into requests(requested_by,requested_to,is_accepted,is_rejected,is_seen) values(?,?,'True','False','False')",(requested_by,requested_to))
                socketio.emit("followed",{"requested_to": requested_to})
            conn.commit()
    @socketio.on("delete_request")
    def unfollow_delete(data):
        requested_by = data.get("requested_by")
        requested_to = data.get("requested_to")

        with sqlite3.connect("data.db") as c:
            cursor = c.cursor()
            cursor.execute("delete from requests where requested_by=? and requested_to=?",(requested_by,requested_to))
            c.commit()
        socketio.emit("unfollowed",{"unfollowed_to":requested_to})
