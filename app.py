from flask import Flask,render_template,url_for,Blueprint
app = Flask(__name__)
from auth import auth_bp

app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(ssl_context="adhoc",debug=True)