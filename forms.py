from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import User

class LoginForm(FlaskForm):
    """
    Form for user authentication/login.
    Collects username and password with option to remember the session.
    """
    # Username field - required
    username = StringField('Username', validators=[DataRequired()])
    # Password field - required and hidden input
    password = PasswordField('Password', validators=[DataRequired()])
    # Remember me checkbox - allows longer session duration
    remember_me = BooleanField('Remember Me')
    # Submit button
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    """
    Form for new user registration.
    Includes validation for username uniqueness, email format,
    password strength, and password confirmation.
    """
    # Username field - required, length between 4-25 characters
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    # Email field - required and must be valid email format
    email = StringField('Email', validators=[DataRequired(), Email()])
    # Password field - required and minimum 8 characters for security
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    # Confirm password - must match password field
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    # Submit button
    submit = SubmitField('Register')
    
    # Custom validator to ensure username is not already taken
    def validate_username(self, username):
        """Check if username already exists in the database"""
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    # Custom validator to ensure email is not already registered
    def validate_email(self, email):
        """Check if email already exists in the database"""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class WeatherSearchForm(FlaskForm):
    """
    Form for weather search functionality.
    Simple form with city input field.
    """
    # City name field - required
    city = StringField('City Name', validators=[DataRequired()])
    # Submit button
    submit = SubmitField('Get Weather')