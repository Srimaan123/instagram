from flask import render_template,redirect,request,Blueprint
import sqlite3
from flask_socketio import emit

main_bp = Blueprint("main", __name__)

@main_bp.route("/main/<username>",methods=['GET','POST'])
def main(username):
    if request.method == 'POST':
        pass
    else:
        return render_template("main.html",username=username)