from flask import Flask,render_template,redirect,request,Blueprint
import sqlite3
auth_bp = Blueprint("auth",__name__)


@auth_bp.route("/",methods=['GET','POST'])
def login():
    if request.method == "POST": 
        username = request.form.get("username")
        password = request.form.get("password")
        with sqlite3.connect('data.db') as conn:
            user = conn.cursor().execute("select * from users where username=? and password=?",(username,password)).fetchone()
        if user:
            return "login"
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