from flask import Flask, render_template , request , redirect, url_for
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
        user = users.query.filter_by(email=user_email, password=user_password).first()
        return render_template("home.html", username=user.name)
    return render_template("login.html")

@app.route("/user_signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user_name = request.form['username']
        user_email = request.form['email']
        user_password = request.form['password']
        user_type = request.form['user_type']

        new_user = users(name=user_name, email=user_email, password=user_password, user_type=user_type)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("signup.html")

if __name__ == "__main__":
    db.create_all()
    app.debug = True
    app.run(host="0.0.0.0")