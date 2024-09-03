from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, IntegerField, SubmitField, DateTimeLocalField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length



class loginForm(FlaskForm):
    # Assuming userID is the id of the user creating the event, it's not a form field
    email = StringField('Email', validators=[DataRequired(),  Length(max=80)])
    password = StringField('Password', validators=[DataRequired(), Length(max=80)])
    submit = SubmitField('Login')


class registerForm(FlaskForm):
    # Assuming userID is the id of the user creating the event, it's not a form field
    fullName = StringField(label='First Name', validators=[DataRequired(), Length(max=80)])
    username = StringField(label='Username', validators=[DataRequired(), Length(max=80)])
    email = StringField(label='Email', validators=[DataRequired(), Length(max=80)])
    phone = IntegerField(label='Email', validators=[DataRequired(), Length(max=10)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirmPassword = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(label='Register')


## This is for creating a post/event
class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=80)])
    status = StringField('Status', validators=[Length(max=80)]) ## STATUS NOT REQUIRED. ASSUMED EVENT IS ACTIVE UNTILL CANCELD
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=255)])  # Textarea for longer input
    flair = SelectField('Flair', coerce=int, choices=[])
    eventTime = DateTimeLocalField('Event Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])  
    location = StringField('Location', validators=[DataRequired(), Length(max=80)])
    submit = SubmitField('Create Event')

class commentForm(FlaskForm):
    message = TextAreaField('Comment', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField(label='Post!')

