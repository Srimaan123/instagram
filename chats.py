from flask import render_template,redirect,url_for,request,Blueprint
from flask_socketio import emit,join_room
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
    with sqlite3.connect("data.db") as conn:
        cur = conn.cursor()
        sender_id = cur.execute("select id from users where username=?",(sender,)).fetchone()[0]
        receiver_id = cur.execute("select id from users where username=?",(receiver,)).fetchone()[0]

    return render_template("chat.html",sender=sender,receiver=receiver,sender_id=sender_id,receiver_id=receiver_id)

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
    @socketio.on("join-room")
    def join_the_room(data):
        print("hiiii")
        sender_id = int(data.get("sender_id"))
        receiver_id = int(data.get("receiver_id"))
        room_code = f'{max(sender_id,receiver_id)}-{min(sender_id,receiver_id)}'
        join_room(room=room_code)
        emit("room_joined",room=room_code)
        print("JOINED THE ROOM")

    @socketio.on("send_message")
    def send_the_message_and_store(data):
        sender = data['sender']
        receiver = data['receiver']
        room_id = data['room_id']
        message = data['message']

        with sqlite3.connect("data.db") as conn:
            cursor = conn.cursor()
            cursor.execute("insert into chats(id,message,sender,receiver,is_seen,is_deleted) values(?,?,?,?,'False','False')",(message,sender,receiver))
            conn.commit()

        emit("receive_message",{
            "message": message,
            "sender": sender,
            "room_id": room_id
        },room=room_id)