import os
from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from flask import request
from flask import session
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


def allowed_file(filename, extensions):
    return filename.rsplit('.')[1].strip() in extensions


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    page='index'

    if request.method == 'POST':
        try:
            inUsername = str(request.form['inputUsername'])
            inPassword = str(request.form['inputPassword'])
            user = User.query.filter_by(username=inUsername).first()
            if inUsername == str(user.username) and User.verify_password(user, inPassword):
                session['userid'] = user.id
                session['username'] = user.username
                session['roleid'] = UserRole.query.filter_by(user_id=user.id).first().role_id
            else:
                flash('Invalid username or password!', 'error')
        except AttributeError:
            flash('Invalid username or password!', 'error')
    return render_template('index.html', page=page, session=session)


@app.route('/logout')
def logout():
    if session:
        session.clear()
        flash('Logout successful!')
    return redirect(url_for('index'))


@app.route('/addUser', methods=['POST', 'GET'])
def addUser():
    page = 'adduser'
    try:
        if session['roleid'] == 1:
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
        else:
            return redirect(url_for('index'))
    except KeyError:
        flash('Url not found!')
        return redirect(url_for('index'))


@app.route('/addResolution', methods=['POST', 'GET'])
def addResolution():
    try:
        if session['roleid'] == 1 or session['roleid'] == 2:
            if request.method == 'POST':
                message = ''
                my_file = request.files['uploadedFile']
                res_num = Resolution.query.filter_by(resolution_num=request.form['resNum']).first()
                res_name = Resolution.query.filter_by(resolution_name=request.form['resName']).first()
                uploaded_file = Resolution.query.filter_by(uploaded_file=my_file.filename).first()
                if my_file.filename == '':
                    flash('No file selected!')
                if my_file and allowed_file(my_file.filename, app.config['ALLOWED_EXTENSIONS']):
                    filename = secure_filename(my_file.filename)
                    if res_num:
                        message = "Duplicate resolution number. "
                        flash(message, 'error')
                    if res_name:
                        message = "Duplicate resolution name. "
                        flash(message, 'error')
                    if uploaded_file:
                        message = "Duplicate file name. "
                        flash(message, 'error')
                    if res_num is None and res_name is None and uploaded_file is None:
                        my_file.save(os.path.join(app.config['UPLOAD_FOLDER_RESOLUTIONS'], filename))
                        resolution = Resolution(request.form['resNum'], request.form['resName'], request.form['supervisor'],
                                               request.form['resolveDate'], filename, session['userid'], session['roleid'])
                        db.session.add(resolution)
                        db.session.commit()
                        flash('New resolution document was added.', 'success')
                else:
                    flash('Invalid file type! Here are the valid file types: .doc, .docx, pdf, png, jpg, jpeg.')

            return render_template('addresolution.html')
        else:
            return redirect(url_for('index'))
    except KeyError:
        flash('Url not found!')
        return redirect(url_for('index'))


@app.route('/addOrdinance', methods=['POST', 'GET'])
def addOrdinance():
    try:
        if session['roleid'] == 1 or session['roleid'] == 2:
            if request.method == 'POST':
                message = ''
                my_file = request.files['uploadedFile']
                ord_num = Ordinance.query.filter_by(ordinance_num=request.form['ordNum']).first()
                ord_name = Ordinance.query.filter_by(ordinance_name=request.form['ordName']).first()
                uploaded_file = Ordinance.query.filter_by(uploaded_file=my_file.filename).first()
                if my_file.filename == '':
                    flash('No file selected!')
                if my_file and allowed_file(my_file.filename, app.config['ALLOWED_EXTENSIONS']):
                    filename = secure_filename(my_file.filename)
                    if ord_num:
                        message = "Duplicate ordinance number. "
                        flash(message, 'error')
                    if ord_name:
                        message = "Duplicate ordinance name. "
                        flash(message, 'error')
                    if uploaded_file:
                        message = "Duplicate file name. "
                        flash(message, 'error')
                    if ord_num is None and ord_name is None and uploaded_file is None:
                        my_file.save(os.path.join(app.config['UPLOAD_FOLDER_ORDINANCES'], filename))
                        ordinance = Ordinance(request.form['ordNum'], request.form['ordName'], request.form['description'],
                                               request.form['sessionDate'], filename, session['userid'], session['roleid'])
                        db.session.add(ordinance)
                        db.session.commit()
                        flash('New ordinance document was added.', 'success')
                else:
                    flash('Invalid file type! Here are the valid file types: .doc, .docx, pdf, png, jpg, jpeg.')

            return render_template('addordinance.html')
        else:
            return redirect(url_for('index'))
    except KeyError:
        flash('Url not found!')
        return redirect(url_for('index'))


@app.route('/addReport', methods=['POST', 'GET'])
def addReport():
    try:
        if session['roleid'] == 1 or session['roleid'] == 2:
            if request.method == 'POST':
                message = ''
                my_file = request.files['uploadedFile']
                rep_name = Report.query.filter_by(report_name=request.form['repName']).first()
                uploaded_file = Report.query.filter_by(uploaded_file=my_file.filename).first()
                if my_file.filename == '':
                    flash('No file selected!')
                if my_file and allowed_file(my_file.filename, app.config['ALLOWED_EXTENSIONS_REPORT']):
                    filename = secure_filename(my_file.filename)
                    if rep_name:
                        message = "Duplicate report name. "
                        flash(message, 'error')
                    if uploaded_file:
                        message = "Duplicate file name. "
                        flash(message, 'error')
                    if rep_name is None and uploaded_file is None:
                        my_file.save(os.path.join(app.config['UPLOAD_FOLDER_REPORTS'], filename))
                        report = Report(request.form['repName'], request.form['reporter'],
                                               request.form['reportedDate'], filename, session['userid'], session['roleid'])
                        db.session.add(report)
                        db.session.commit()
                        flash('New report document was added.', 'success')
                else:
                    flash('Invalid file type! Here are the valid file types: .xls, .xlsx, .doc, .docx, .ppt, .pptx, .pdf')

            return render_template('addreport.html')
        else:
            return redirect(url_for('index'))
    except KeyError:
        flash('Url not found!')
        return redirect(url_for('index'))


@app.route('/viewUser', methods=['POST', 'GET'])
def viewUser():
    if session:
        user_roles = UserRole.query.all()

        if len(user_roles):
            x = 0
            users_info = {}

            while x < len(user_roles):
                users_info[x] = {'user': User.query.filter_by(id=user_roles[x].user_id).first(),
                                 'role': Role.query.filter_by(id=user_roles[x].role_id).first().role_name}
                x += 1

            return render_template('viewuser.html', users_info=users_info)

        else:
            flash('No available user yet. Please create user.')
    else:
        flash('Url not found!')
        return redirect(url_for('index'))


@app.route('/editUser', methods=['POST', 'GET'])
def editUser():
    if request.method == 'POST' and session['roleid'] == 1:
        user = User.query.filter_by(id=request.form['inputID']).first()
        user.name = request.form['inputName']
        user.address = request.form['inputAddress']
        user_role = UserRole.query.filter_by(user_id=user.id).first()
        role_id = Role.query.filter_by(role_name=request.form['inputRole']).first().id
        user_role.role_id = role_id
        db.session.commit()
        flash(user.username + '\'s information was updated...')
        return redirect(url_for('viewUser'))
    else:
        flash('Url not found!')
        return redirect(url_for('index'))


@app.route('/deleteUser/<username>', methods=['POST', 'GET'])
def deleteUser(username):
    if session['roleid'] == 1:
        user_role_id = User.query.filter_by(username=username).first().id
        UserRole.query.filter_by(user_id=user_role_id).delete()
        User.query.filter_by(username=username).delete()
        db.session.commit()
        flash(username + 'was deleted in the database...')
        return redirect(url_for('viewUser'))
    else:
        flash('Url not found!')
        return redirect(url_for('index'))


@app.route('/viewResolution')
def viewResolution():
    if session:
        resolutions = Resolution.query.all()

        if len(resolutions):
            x = 0
            resolution_info = {}

            while x < len(resolutions):
                resolution_info[x] = {'id': resolutions[x].id,
                                      'res_num': resolutions[x].resolution_num,
                                      'res_name': resolutions[x].resolution_name,
                                      'supervisor': resolutions[x].supervisor,
                                      'resolve_date': resolutions[x].resolve_date,
                                      'uploaded_file': resolutions[x].uploaded_file,
                                      'uploader': User.query.filter_by(id=resolutions[x].uploader_id).first().username}
                x += 1
            flash(session['roleid'])
            return render_template('viewresolution.html', resolution_info=resolution_info, role_id=session['roleid'])

        else:
            flash('No available more resolutions available!')
        flash(session['roleid'])
        return render_template('viewresolution.html', role_id=session['roleid'])
    else:
        flash('Url not found!')
        return redirect(url_for('index'))


@app.route('/editResolution', methods=['POST', 'GET'])
def editResolution():
    if request.method == 'POST' and session['roleid'] == 1 or session['roleid'] == 2:
        resolution = Resolution.query.filter_by(id=request.form['inputID']).first()
        resolution.resolution_num = request.form['resNum']
        resolution.resolution_name = request.form['resName']
        resolution.supervisor = request.form['supervisor']
        resolution.resolve_date = request.form['resolveDate']
        if request.files['newFile']:
            new_file = request.files['newFile']
            filename = secure_filename(new_file.filename)
            os.remove(os.path.join(app.config['UPLOAD_FOLDER_RESOLUTIONS'], resolution.uploaded_file))
            new_file.save(os.path.join(app.config['UPLOAD_FOLDER_RESOLUTIONS'], filename))
            resolution.uploaded_file = filename
        resolution.uploader_id = User.query.filter_by(username=request.form['uploader']).first().id
        db.session.commit()
        flash(resolution.resolution_name + ' information was updated...')
        return redirect(url_for('viewResolution'))
    else:
        flash('Url not found!')
        return redirect(url_for('index'))


@app.route('/deleteResolution/<id>', methods=['POST', 'GET'])
def deleteResolution(id):
    if session['roleid'] == 1:
        resolution = Resolution.query.filter_by(id=id).first()
        res_name = resolution.resolution_name
        filename = resolution.uploaded_file
        os.remove(os.path.join(app.config['UPLOAD_FOLDER_RESOLUTIONS'], filename))
        Resolution.query.filter_by(id=id).delete()
        db.session.commit()

        flash(res_name + ' was successfully deleted in the database...')
        return redirect(url_for('viewResolution'))
    else:
        flash('Url not found!')
        return redirect(url_for('index'))