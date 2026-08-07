from flask import Blueprint,render_template,redirect
import sqlite3
from flask_socketio import emit

notifications_bp = Blueprint("notifications",__name__)

@notifications_bp.route("/notifications/<username>")
def show_notifications(username):
    with sqlite3.connect("data.db") as conn:
        cursor = conn.cursor()
        requests_of_user = cursor.execute("select * from requests where requested_by=? or requested_to=?",(username,username)).fetchall()
        
        follow_requests = []
        rejected_requests = []
        accepted_requests = []
        following = []
        for request in requests_of_user:
            id = request[0]
            if request[-1] != 'True':
                if request[1] == username:
                    if request[3] == 'True':
                        accepted_requests.append((id,request[2]))
                    if request[4] == 'False':
                        rejected_requests.append((id,request[2]))
                else:
                    if request[3] == 'True':
                        following.append((id,request[1]))
                    else:
                        follow_requests.append((id,request[1]))
                    
        all_requests = {
            "accepted_requests": accepted_requests,
            'rejected_requests': rejected_requests,
            'follow_requests': follow_requests,
            'following': following
        }
    return render_template("notifications.html",username=username,all_requests=all_requests)

def notifications_api(socketio):
    @socketio.on("accept_request")
    def accept_request(data):
        accepted_by = data.get("accepted_by")
        accepted_to = data.get('accepted_to')

        with sqlite3.connect('data.db') as conn :
            cursor = conn.cursor()
            cursor.execute("update requests set is_accepted='True' where requested_by=? and requested_to=?",(accepted_to,accepted_by))
            conn.commit()
        emit("reload")
