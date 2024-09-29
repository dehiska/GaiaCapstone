from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, IntegerField, SubmitField, DateTimeLocalField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length



class loginForm(FlaskForm):
    # Assuming userID is the id of the user creating the event, it's not a form field
    email = StringField('Email', validators=[DataRequired(),  Length(max=80)])
    password = StringField('Password', validators=[DataRequired(), Length(max=80)])
    submit = SubmitField('Login')


class registerForm(FlaskForm):
    firstName = StringField(label='First Name', validators=[DataRequired(), Length(max=80)])
    lastName = StringField(label='Last Name', validators=[DataRequired(), Length(max=80)])
    username = StringField(label='Username', validators=[DataRequired(), Length(max=80)])
    email = StringField(label='Email', validators=[DataRequired(), Length(max=80)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(label='Register')
