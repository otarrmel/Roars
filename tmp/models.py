from app import db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, unique=True)
    password_hash = db.Column(db.String(50), index=True)
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
        return '<Username %r>' % (self.username)


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permission = db.column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.VIEW, True),
            'Editor': (Permission.VIEW | Permission.UPLOAD, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permission = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __init__(self, role_name):
        self.role_name = role_name

    def __repr__(self):
        return '<RoleName %r>' % (self.role_name)


class Permission:
    VIEW = 0x01
    UPLOAD = 0x02
    ADMINISTER = 0x80


class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    def __repr__(self):
        return '<UserRoleID %r>' % (self.id)
