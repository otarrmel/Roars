from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = ['doc', 'docx', 'pdf', 'png', 'jpg', 'jpeg']
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1z2x3c*()@localhost/roars'
app.config['ALLOWED_EXTENSIONS_REPORT'] = ['xls', 'xlsx', 'doc', 'docx', 'ppt', 'pptx', 'pdf']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'S0l3mry$'
db = SQLAlchemy(app)

from app import views
from app import models