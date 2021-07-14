from application import app,db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, DecimalField,IntegerField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError
import string
class UserCheck:
    def __init__(self,banned,message=None):
        self.banned=banned
        if not message:
            message = 'Please choose another username'
        self.message=message
    def __call__(self,form,field):
        if field.data.lower() in (word.lower() for word in self.banned):
            raise ValidationError(self.message)
class SpecialCharacterCheck:
    def __init__(self,banned,message=None):
        if not message: message="Please don's use special characters!"
        self.message=message
        self.banned=banned
    def __call__(self,form,field):
        if field.data.lower() not in (char.lower for char in self.banned):
            raise ValidationError(self.message)

class myForm(FlaskForm):
    username=StringField('Username',validators=[
        DataRequired(),
        UserCheck(message='You cant be an admin',banned=['root','admin','sys']),
        SpecialCharacterCheck(message="You can not use special characters.",banned=string.ascii_lowercase),
        Length(min=2,max=15)
        ])
    submit = SubmitField('Sign up')

class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    description=db.Column(db.String(100),nullable=False)
    complete = db.Column(db.Boolean)

class BasicForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    date = DateField('Date of Birth', format="%Y-%m-%d")
    years = IntegerField()
    height = DecimalField()
    confirm= SelectField('Language', choices=[('English', 'English'), ('Spanish', 'Spanish'), ('English', 'Welsh')])
    submit = SubmitField('Add Name')


class ShowToDoList(FlaskForm):
    name=StringField('Task: ')
    description=StringField('Description')
    status=StringField('Complete: ')
    submit = SubmitField('Confirm')
