from flask_wtf import Form
from wtforms import StringField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import BooleanField
from wtforms import SelectField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import Regexp
from wtforms.validators import EqualTo
from wtforms import ValidationError
from models import User



class UserForm(Form):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
        'Usernames must have only letters, numbers, dots or underscores.')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match.')])
    confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])

