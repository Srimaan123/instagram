from flask import Flask,render_template,redirect,request,Blueprint
import sqlite3
from flask_socketio import emit
auth_bp = Blueprint("auth",__name__)


@auth_bp.route("/",methods=['GET','POST'])
def login():
    if request.method == "POST": 
        username = request.form.get("username")
        password = request.form.get("password")
        with sqlite3.connect('data.db') as conn:
            user = conn.cursor().execute("select * from users where username=? and password=?",(username,password)).fetchone()
        if user:
            return redirect(f"/main/{username}")
        else:
            return "not login"
    else:
        return render_template("login.html")

@auth_bp.route("/create",methods=['GET','POST'])
def create():
    if request.method == "POST":
        pass
    else:
        return render_template("create.html")

def init_auth_socket(socketio):
    @socketio.on("add_account")
    def create_account(data):
        username = data.get("username")
        password = data.get("password")
        mobile_number = data.get("mobile_number")
        with sqlite3.connect("data.db") as conn:
            cursor = conn.cursor()
            user = cursor.execute("select * from users where username=?",(username,)).fetchone()
            if user:
                emit("user_already_exists",{"username": username})
                return
            else:
                cursor.execute("insert into users(username,password,mobile_number,is_private) values(?,?,?,?)",(username,password,mobile_number,'True'))
                conn.commit()
        emit("user_added",{"username": username})