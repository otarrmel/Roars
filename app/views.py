import os
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
from app.models import Resolution
from app.models import Ordinance
from app.models import Report
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

userid = 1


def allowed_file(filename, extensions):
    return filename.rsplit('.')[1].strip() in extensions


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
        try:
            inUsername = str(request.form['inputUsername'])
            inPassword = str(request.form['inputPassword'])
            user = User.query.filter_by(username=inUsername).first()
            if inUsername == str(user.username) and User.verify_password(user, inPassword):
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password!', 'error')
        except AttributeError:
            flash('Invalid username or password!', 'error')

    return render_template('login.html')


@app.route('/addResolution', methods=['POST', 'GET'])
def addResolution():
    if request.method == 'POST':
        file = request.files['uploadedFile']
        if file.filename == '':
            flash('No file selected!')
        if file and allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS']):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            resolution = Resolution(request.form['resNum'], request.form['resName'], request.form['supervisor'],
                                   request.form['resolveDate'], filename, userid, 1)
            db.session.add(resolution)
            db.session.commit()
            flash('New resolution document was added.', 'success')
        else:
            flash('Invalid file type! Here are the valid file types: .doc, .docx, pdf, png, jpg, jpeg.')

    return render_template('addresolution.html')


@app.route('/addOrdinance', methods=['POST', 'GET'])
def addOrdinance():
    if request.method == 'POST':
        file = request.files['uploadedFile']
        if file.filename == '':
            flash('No file selected!')
        if file and allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS']):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            ordinance = Ordinance(request.form['ordNum'], request.form['ordName'], request.form['description'],
                                   request.form['sessionDate'], filename, userid, 2)
            db.session.add(ordinance)
            db.session.commit()
            flash('New ordinance document was added.', 'success')
        else:
            flash('Invalid file type! Here are the valid file types: .doc, .docx, pdf, png, jpg, jpeg.')

    return render_template('addordinance.html')


@app.route('/addReport', methods=['POST', 'GET'])
def addReport():
    if request.method == 'POST':
        file = request.files['uploadedFile']
        if file.filename == '':
            flash('No file selected!')
        if file and allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS_REPORT']):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            report = Report(request.form['repName'], request.form['reporter'],
                                   request.form['reportedDate'], filename, userid, 3)
            db.session.add(report)
            db.session.commit()
            flash('New report document was added.', 'success')
        else:
            flash('Invalid file type! Here are the valid file types: .xls, .xlsx, .doc, .docx, .ppt, .pptx, .pdf')

    return render_template('addreport.html')