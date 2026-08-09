from flask import render_template,redirect,url_for,request,Blueprint
from flask_socketio import emit
import sqlite3

chats_bp = Blueprint("chat",__name__)

@chats_bp.route("/accounts/<username>",methods=['POST','GET'])
def accounts(username):
    if request.method == 'POST':
        pass
    else:
        with sqlite3.connect("data.db") as conn:
            cur = conn.cursor()
            all_requests = cur.execute("select * from requests where requested_by=? or requested_to=? and is_accepted='True'",(username,username)).fetchall()
            total_accounts = []
            for i in all_requests:
                if i[1] == username:
                    total_accounts.append(i[2])
                if i[2] == username:
                    total_accounts.append(i[1])

        return render_template("accounts.html",username=username,accounts=total_accounts)

@chats_bp.route("/chat/<code>")
def show_chats(code):
    sender,receiver = code.split("-")
    return render_template("chat.html",sender=sender,receiver=receiver)

def chats_api(socketio):
    @socketio.on("search_account")
    def search_account_based_on(data):
        username = data.get("username")
        text = f'%{data.get("text")}%'

        with sqlite3.connect("data.db") as conn:
            cursor = conn.cursor()
            users = cursor.execute("select username from users where username like ?",(text,)).fetchall()
            all_requests = cursor.execute('select * from requests where requested_by=? or requested_to=?',(username,username)).fetchall()
            similar_users = []
            for i in users:
                i = i[0]
                for j in all_requests:
                    if i == j[1]:
                        similar_users.append(j[1])
                    if i == j[2]:
                        similar_users.append(j[2])
            emit("search_account_result",{"users": similar_users})

