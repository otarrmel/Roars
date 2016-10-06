from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from flask import request
from app import app
from app import db
from app.models import User
from app.models import UserRole
from app.models import Role
from sqlalchemy.exc import IntegrityError


@app.route('/')
@app.route('/index')
def index():
    page='index'
    return render_template('index.html', page=page)


@app.route('/adduser', methods=['POST', 'GET'])
def adduser():
    page = 'adduser'
    if request.method == 'POST' and request.form['inputPassword'] == request.form['inputConfirm']:
        try:
            user=User(request.form['inputUsername'], request.form['inputPassword'], request.form['inputName'],
                      request.form['inputAddress'])
            db.session.add(user)
            userid = int((User.query.filter_by(username=str(request.form['inputUsername'])).first()).id)
            roleid = int((Role.query.filter_by(role_name=str(request.form['inputRole'])).first().id))
            user_role = UserRole(userid, roleid)
            db.session.add(user_role)
            db.session.commit()
            flash('New user was added.', 'success')
        except IntegrityError:
            flash('Username already exist!', 'error')
    elif request.method == 'POST' and request.form['inputPassword'] != request.form['inputConfirm']:
        flash('Password must match!', 'error')

    return render_template('adduser.html',page=page)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        inUsername = str(request.form['inputUsername'])
        inPassword = str(request.form['inputPassword'])
        user = User.query.filter_by(username=inUsername).first()
        if inUsername == str(user.username) and User.verify_password(user, inPassword):
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password!', 'error')
    return render_template('login.html')