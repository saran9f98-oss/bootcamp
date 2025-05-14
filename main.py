from flask import Flask
import os

app = Flask(__name__)

@app.route("/", methods=["GET"]) # NOTE: / =  http://192.168.1.42:5000
def home():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(host="0.0.0.0")