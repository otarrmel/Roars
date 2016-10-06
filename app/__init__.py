from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1z2x3c*()@localhost/roars'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'S0l3mry$'
db = SQLAlchemy(app)

from app import views
from app import models