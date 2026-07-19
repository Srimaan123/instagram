from flask import Flask,render_template,redirect,request,Blueprint

auth_bp = Blueprint("auth",__name__)

@auth_bp.route("/",methods=['GET','POST'])
def login():
    if request.method == "POST": 
        pass
    else:
        return render_template("login.html")