from flask import Blueprint,render_template,redirect
import sqlite3


notifications_bp = Blueprint("notifications",__name__)

@notifications_bp.route("/notifications/<username>")
def show_notifications(username):
    with sqlite3.connect("data.db") as conn:
        cursor = conn.cursor()
        requests_of_user = cursor.execute("select * from requests where requested_by=? or requested_to=?",(username,username)).fetchall()
        is_private = cursor.execute("select is_private from users where username=?",(username,)).fetchone()[0]
        follow_requests = []
        rejected_requests = []
        accepted_requests = []
        following = []
        for request in requests_of_user:
            if request[-1] != 'True':
                if request[0] == username:
                    
                    if request[2] == 'True':
                        if is_private == 'False':
                            following.append(request[1])
                        else:
                            follow_requests.append(request[1])
                    elif request[3] == 'True':
                        rejected_requests.append(request[1])
                elif request[1] == username:
                    if request[2] == 'True':
                        accepted_requests.append(request[0])
                    
        all_requests = {
            "accepted_requests": accepted_requests,
            'rejected_requests': rejected_requests,
            'follow_requests': follow_requests,
            'following': following
        }
    return render_template("notifications.html",username=username,all_requests=all_requests)
