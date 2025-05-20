
# Import necessary modules and functions
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user  # For session-based auth
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity  # For JWT auth
from models import User, db  # Database models
from forms import LoginForm, RegistrationForm  # Form classes for validation

# Create a Blueprint for authentication routes
# Blueprints allow organizing routes into groups
auth = Blueprint('auth', __name__)

# ----- WEB INTERFACE ROUTES (Session-based Authentication) -----

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    User registration endpoint.
    GET: Display registration form
    POST: Process form submission and create new user
    """
    # Redirect already logged in users to home page
    if current_user.is_authenticated:
        return redirect(url_for('weather.index'))
    
    # Initialize the registration form
    form = RegistrationForm()
    # If form is submitted and validated
    if form.validate_on_submit():
        # Create new user object
        user = User(username=form.username.data, email=form.email.data)
        # Hash the password before storing
        user.set_password(form.password.data)
        # Add user to database
        db.session.add(user)
        db.session.commit()
        # Notify user of successful registration
        flash('Congratulations, you are now registered!', 'success')
        # Redirect to login page
        return redirect(url_for('auth.login'))
    
    # Render registration template for GET requests or invalid form submissions
    return render_template('register.html', title='Register', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    User login endpoint.
    GET: Display login form
    POST: Process login attempt and create user session
    """
    # Redirect already logged in users to home page
    if current_user.is_authenticated:
        return redirect(url_for('weather.index'))
    
    # Initialize login form
    form = LoginForm()
    # If form is submitted and validated
    if form.validate_on_submit():
        # Find user by username
        user = User.query.filter_by(username=form.username.data).first()
        # Verify username exists and password is correct
        if user is None or not user.check_password(form.password.data):
            # Show error for invalid credentials
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        
        # Log user in with Flask-Login (creates session)
        login_user(user, remember=form.remember_me.data)
        # Check if user was redirected from a protected page
        next_page = request.args.get('next')
        # Validate next page or default to home
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('weather.index')
        return redirect(next_page)
    
    # Render login template for GET requests or invalid form submissions
    return render_template('login.html', title='Sign In', form=form)

@auth.route('/logout')
@login_required  # Ensures only logged-in users can access this route
def logout():
    """End the user session and redirect to home page"""
    # Clear user session with Flask-Login
    logout_user()
    # Redirect to home page
    return redirect(url_for('weather.index'))

@auth.route('/profile')
@login_required  # Ensures only logged-in users can access this route
def profile():
    """Display user profile page"""
    # Render profile template (current_user is available in template)
    return render_template('profile.html', title='Profile')

# ----- API ROUTES (JWT Authentication) -----

@auth.route('/api/token', methods=['POST'])
def get_token():
    """
    API endpoint to obtain a JWT token.
    Clients send username/password and receive an access token.
    """
    # Ensure request contains JSON data
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    
    # Extract credentials from JSON
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    # Validate that both fields are provided
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400
    
    # Find user by username
    user = User.query.filter_by(username=username).first()
    # Verify username exists and password is correct
    if user is None or not user.check_password(password):
        # Return error for invalid credentials (401 Unauthorized)
        return jsonify({"msg": "Bad username or password"}), 401
    
    # Generate JWT access token with username as identity
    access_token = create_access_token(identity=username)
    # Return token in JSON response
    return jsonify(access_token=access_token)

@auth.route('/api/profile')
@jwt_required()  # Ensures request contains valid JWT token
def protected():
    """
    Protected API endpoint to retrieve user profile information.
    Requires valid JWT token in Authorization header.
    """
    # Get username from JWT token
    current_user_identity = get_jwt_identity()
    # Find user in database
    user = User.query.filter_by(username=current_user_identity).first()
    # Return user data as JSON
    return jsonify(
        id=user.id,
        username=user.username,
        email=user.email
    )