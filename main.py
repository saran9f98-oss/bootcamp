from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route("/", methods=["GET"]) # NOTE: / =  http://192.168.1.42:5000
def login():
    return render_template("login.html")

@app.route("/user_signup", methods=["GET"])
def signup():
    return render_template("signup.html")

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")