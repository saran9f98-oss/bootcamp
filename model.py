from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    user_type = db.Column(db.String(), nullable=False)

class booking_data(db.Model):
    __tablename__ = "booking_data"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    resturant_id = db.Column(db.Integer)
    date = db.Column(db.String())
    table_id = db.Column(db.String())

class resturant_data(db.Model):
    __tablename__ = "resturant_data"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False)
    location = db.Column(db.String(), nullable=False)
    table_id = db.Column(db.Integer, nullable=False)
   