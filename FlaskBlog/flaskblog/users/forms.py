# All imports 

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User

# RegistrationForm class represents the registration form structure. 
# Using FlaskForm we can write form easily in python using OOP. 
# While running this form gets converted to html forms
class RegistrationForm(FlaskForm):
    
    # Declaring the form fields

    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # Function to validate username for correctness and uniqueness
    
    def validate_username(self, username):
        # filter_by filters the all user data available according to the category passed to it. and .first() returns the first user after the fuser data has been filtered.
        user = User.query.filter_by(username=username.data).first()
        # if user is not None implies that the username is already taken by another user
        if user is not None:
            raise ValidationError('That Username is already taken. Please choose another.')
    
    
    # Function to validate email for correctness and uniqueness

    def validate_email(self, email):
        # filter_by filters the all user data available according to the category passed to it. and .first() returns the first user after the fuser data has been filtered.
        user = User.query.filter_by(email=email.data).first()
        # if user is not None implies that the email is already taken by another user
        if user:
            raise ValidationError('That email is already taken. Please choose another.')



class LoginForm(FlaskForm):
   
    # Declaring the form fields

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):

    # Declaring the form fields

    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')


    # Function to validate username for correctness and uniqueness

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError( 'That Username is already taken. Please choose another.')

    # Function to validate email for correctness and uniqueness

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError( 'That email is already taken. Please choose another.')


class RequestResetForm(FlaskForm):
    
    # Declaring the form fields

    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    # Function to validate email for correctness and uniqueness

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        # if user is forgot password and he is requesting for reset password. But if the no account is available for email provided by him.
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):

    # Declaring the form fields
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
