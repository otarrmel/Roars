from flask import render_template, flash, redirect
from app import app


@app.route('/')
@app.route('/index')
def index():
    page='index'
    return render_template('index.html', page=page)


@app.route('/adduser')
def adduser():
    page='adduser'
    return render_template('adduser.html', page=page)