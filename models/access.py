from app import db
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# app = Flask(__name__)

# app.secret_key = 'secret*key'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'

# db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password


# if __name__ == "__main__":

#     # Run this file directly to create the database tables.
#     print ("Creating database tables...")
#     db.create_all()
#     print ("Done!")