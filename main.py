from flask import Flask, render_template , request
import os
from model import *



current_dir = os.path.abspath(os.path.dirname(__file__)) 

app= Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(current_dir, "Database.sqlite3")

db.init_app(app)
app.app_context().push()

@app.route("/", methods=["GET", "POST"]) # NOTE: / =  http://192.168.1.42:5000
def login():
    if request.method == "POST":
        user_email = request.form['email']
        user_password = request.form['password']
        print(user_email)
        print(user_password)
        return render_template("home.html", message=user_email)
    return render_template("login.html")

@app.route("/user_signup", methods=["GET"])
def signup():
    return render_template("signup.html")

if __name__ == "__main__":
    db.create_all()
    app.debug = True
    app.run(host="0.0.0.0")