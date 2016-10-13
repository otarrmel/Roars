from app import db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, unique=True)
    password_hash = db.Column(db.String(128), index=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(100))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, username, password, name, address):
        self.username = username
        self.password = password
        self.name = name
        self.address = address

    def __repr__(self):
        return "<User(id='%s', username='%s', password_hash='%s', name='%s', address='%s')>" % \
               (self.id, self.username, self.password_hash, self.name, self.address)


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(64), unique=True)


    def __init__(self, role_name):
        self.role_name = role_name

    def __repr__(self):
        return "<Role(id='%s', role_name='%s')>" % (self.id, self.role_name)


class UserRole(db.Model):
    __tablename__ = 'user_role'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id

    def __repr__(self):
        return "<UseRole(id='%s', user_id='%s', role_id='%s')>" % (self.id, self.user_id, self.role_id)


class Document(db.Model):
    __tablename__ = 'document'
    id = db.Column(db.Integer, primary_key=True)
    document_name = db.Column(db.String(64), unique=True)

    def __init__(self, document_name):
        self.document_name = document_name

    def __repr__(self):
        return '<Document Name %r>' % (self.document_name)


class Resolution(db.Model):
    __tablename__ = 'resolution'
    id = db.Column(db.Integer, primary_key=True)
    resolution_num = db.Column(db.String(64), unique=True)
    resolution_name = db.Column(db.String(64), unique=True)
    supervisor = db.Column(db.String(64))
    resolve_date = db.Column(db.Date())
    uploaded_file = db.Column(db.String(256), unique=True)
    uploader_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    DocTypeID = db.Column(db.Integer())

    def __init__(self, resolution_num, resolution_name, supervisor, resolve_date, uploaded_file, uploader_id, DocTypeID):
        self.resolution_num = resolution_num
        self.resolution_name = resolution_name
        self.supervisor = supervisor
        self.resolve_date = resolve_date
        self.uploaded_file = uploaded_file
        self.uploader_id = uploader_id
        self.DocTypeID = DocTypeID

    def __repr__(self):
        return '<Resolution Name %r>' % (self.resolution_name)


class Ordinance(db.Model):
    __tablename__ = 'ordinance'
    id = db.Column(db.Integer, primary_key=True)
    ordinance_num = db.Column(db.String(64), unique=True)
    ordinance_name = db.Column(db.String(64), unique=True)
    description = db.Column(db.Text())
    session_date = db.Column(db.Date())
    uploaded_file = db.Column(db.String(256))
    uploader_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    DocTypeID = db.Column(db.Integer())

    def __init__(self, ordinance_num, ordinance_name, description, session_date, uploaded_file, uploader_id, DocTypeID):
        self.ordinance_num = ordinance_num
        self.ordinance_name = ordinance_name
        self.description = description
        self.session_date = session_date
        self.uploaded_file = uploaded_file
        self.uploader_id = uploader_id
        self.DocTypeID = DocTypeID

    def __repr__(self):
        return '<Ordinance Name %r>' % (self.ordinance_name)


class Report(db.Model):
    __tablename__ = 'report'
    id = db.Column(db.Integer, primary_key=True)
    report_name = db.Column(db.String(64), unique=True)
    reporter = db.Column(db.String(64))
    session_date = db.Column(db.Date())
    uploaded_file = db.Column(db.String(256))
    uploader_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    DocTypeID = db.Column(db.Integer())

    def __init__(self, report_name, reporter, reported_date, uploaded_file, uploader_id, DocTypeID):
        self.report_name = report_name
        self.reporter = reporter
        self.reported_date = reported_date
        self.uploaded_file = uploaded_file
        self.uploader_id = uploader_id
        self.DocTypeID = DocTypeID

    def __repr__(self):
        return '<Report Name %r>' % (self.report_name)
