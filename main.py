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
                if user.user_type == 'customer':
                    unique_locations = resturant_data.query.with_entities(resturant_data.location).distinct().all()
                    locations = [loc[0] for loc in unique_locations]
                    print(locations)
                    return render_template("home.html", user_data=user, location_data=locations)
                
                elif user.user_type == 'resturant':
                    return render_template("resturant_home.html", resturant_data=user)
                
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








@app.route("/resturant_signup", methods=["GET", "POST"])
def resturant_signup():
    if request.method == "POST":
        resturant_name = request.form['username']
        resturant_email = request.form['email']
        resturant_password = request.form['password']
        user_type = request.form['user_type']


        resturant_location = request.form['location']
        resturant_description = request.form['description']


        if users.query.filter_by(email=resturant_password).first():
            return 'Email already exists'
        else:
            if user_type not in ['admin', 'customer', 'resturant']:
                return 'Invalid user type'
            else:
                new_user = users(
                    name=resturant_name, 
                    email=resturant_email,
                    password=resturant_password, 
                    user_type=user_type)
                db.session.add(new_user)
                
                new_resturant = resturant_data(
                    name=resturant_name,
                    location=resturant_location,
                    description=resturant_description)
                db.session.add(new_resturant)


                db.session.commit()

        return redirect(url_for("login"))
    return render_template("resturant_signup.html")








@app.route("/search_results/<customer_id>", methods=["GET", "POST"])
def search_result_page(customer_id):
    if request.method == "POST":
        if  request.form['form_type'] == "name":
            resturant_name = request.form['resturant_name']
            search_result = resturant_data.query.filter(resturant_data.name.ilike(resturant_name)).first()
            if search_result is None:
                return 'Restaurant not found'
            else:
                return redirect(url_for("resturant_page", resturant_name=search_result.name, customer_id=customer_id))
        
        elif request.form['form_type'] == "location":
            resturant_location = request.form['resturant_location']
            search_result = resturant_data.query.filter_by(location=resturant_location).all()
            return render_template("searchResult.html", search_result=search_result, customer_id=customer_id)
        
@app.route("/resturant_page/<resturant_name>/<customer_id>", methods=["GET", "POST"])
def resturant_page(resturant_name, customer_id):
    search_result = resturant_data.query.filter(resturant_data.name.ilike(resturant_name)).first()
    print( search_result.id )
    return render_template("resturant_page.html", resturant_data=search_result, customer_id=customer_id)




@app.route("/table_booking_page/<resturant_ID>/<customer_id>", methods=["GET"])
def table_booking_page(resturant_ID, customer_id):
    user_date = request.args.get('search_date')
    current_booking = booking_data.query.filter_by(resturant_id=resturant_ID, date=user_date).first()
    if current_booking:
        print(current_booking.table_ids)
        rest_data = resturant_data.query.filter_by(id=resturant_ID).first()

        unbooked_tables = [ table for table in rest_data.tables if str(table.id) not in current_booking.table_ids.split(',')]
        return render_template("table_booking_page.html", 
                               resturant_data=rest_data,
                               unbooked_tables=unbooked_tables, 
                               customer_id=customer_id, 
                               date=user_date)
    else:
        rest_data = resturant_data.query.filter_by(id=resturant_ID).first()
        return render_template("table_booking_page.html", 
                               resturant_data=rest_data, 
                               customer_id=customer_id, 
                               date=user_date)





@app.route("/book_table/<table_id>/<resturant_ID>/<customer_id>/<date>", methods=["POST"])
def book_table(table_id, resturant_ID, customer_id, date):
    print(table_id, resturant_ID, customer_id, date)
    new_booking = booking_data(
        table_ids=table_id, 
        resturant_id=resturant_ID, 
        user_id=customer_id, 
        date=date
    )
    db.session.add(new_booking)
    db.session.commit()
    return 'Table Booked Successfully'
    







@app.route("/add_table/<resturant>/", methods=["POST"])
def add_table(resturant):
    resturant_ID = resturant_data.query.filter_by(name=resturant).first().id
    table_code = request.form['table_code']
    capacity = request.form['table_size']
    new_table = resturant_table_data(table_code=table_code, capacity=capacity)
    db.session.add(new_table)
    db.session.commit()

    new_relation = resturant_table_relation(
        resturant_id=resturant_ID, 
        table_id=new_table.id
    )
    db.session.add(new_relation)
    db.session.commit()
    return 'Table added successfully!'






       
    
if __name__ == "__main__":
    db.create_all()
    app.debug = True
    app.run(host="0.0.0.0")