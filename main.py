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
        user = users.query.filter_by(email=user_email).first()

        if user is None:
            return 'User not found'
        else:
            if user.password != user_password:
                return 'Incorrect password'
            else:
                unique_locations = resturant_data.query.with_entities(resturant_data.location).distinct().all()
                locations = [loc[0] for loc in unique_locations]
                print(locations)
                return render_template("home.html", username=user.name, location_data=locations)
            
    return render_template("login.html")

@app.route("/user_signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user_name = request.form['username']
        user_email = request.form['email']
        user_password = request.form['password']
        user_type = request.form['user_type']

        if users.query.filter_by(email=user_email).first():
            return 'Email already exists'
        else:
            if user_type not in ['admin', 'customer', 'resturant']:
                return 'Invalid user type'
            else:
                new_user = users(name=user_name, email=user_email, password=user_password, user_type=user_type)
                db.session.add(new_user)
                db.session.commit()

        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/search_results", methods=["GET", "POST"])
def search_result_page():
    if request.method == "POST":
        if  request.form['form_type'] == "name":
            resturant_name = request.form['resturant_name']
            search_result = resturant_data.query.filter(resturant_data.name.ilike(resturant_name)).first()
            if search_result is None:
                return 'Restaurant not found'
            else:
                return redirect(url_for("resturant_page", resturant_name=search_result.name))
        
        elif request.form['form_type'] == "location":
            resturant_location = request.form['resturant_location']
            search_result = resturant_data.query.filter_by(location=resturant_location).all()
            return render_template("searchResult.html", search_result=search_result)
        
@app.route("/resturant_page/<resturant_name>", methods=["GET", "POST"])
def resturant_page(resturant_name):
    search_result = resturant_data.query.filter(resturant_data.name.ilike(resturant_name)).first()
    return render_template("resturant_page.html", resturant_data=search_result)

       
    
if __name__ == "__main__":
    db.create_all()
    app.debug = True
    app.run(host="0.0.0.0")