from flask import render_template,redirect,url_for,request,Blueprint
from flask_socketio import emit

chats_bp = Blueprint("chat",__name__)

@chats_bp.route("/accounts/<username>",methods=['POST','GET'])
def accounts(username):
    if request.method == 'POST':
        pass
    else:
        return render_template("accounts.html")