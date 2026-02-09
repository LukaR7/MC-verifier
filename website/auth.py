from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from flask_login import current_user, login_required, login_user, logout_user
import random 

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user:
            if user.is_lecturer:
                flash('This is a Lecturer account. Use Lecturer login.', category='error')
            elif check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.student_dashboard'))
            else:
                flash('Incorrect password.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/login-lec', methods=['GET', 'POST'])
def login_lec():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user:
            if not user.is_lecturer:
                flash('This is a Student account. Use Student login.', category='error')
            elif check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.lecturer_dashboard'))
            else:
                flash('Incorrect password.', category='error')
        else:
            flash('Lecturer account not found.', category='error')
    return render_template("loginlec.html", user=current_user)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

    
        if len(email) < 4 or '@' not in email:
            flash('Please enter a valid email address.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif not any(char.isupper() for char in password):
            flash('Password must contain at least one uppercase letter.', category='error')
        elif not any(char.islower() for char in password):
            flash('Password must contain at least one lowercase letter.', category='error')
        elif not any(char.isdigit() for char in password):
            flash('Password must contain at least one number.', category='error')
        elif User.query.filter_by(email=email).first():
            flash('Email already exists.', category='error')
        else:
            new_user = User(
                email=email, name=name, 
                password=generate_password_hash(password, method='pbkdf2:sha256'), 
                is_lecturer=False
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created successfully!', category='success')
            return redirect(url_for('views.student_dashboard'))
            
    return render_template("sign_up.html", user=current_user)

@auth.route('/signup-lec', methods=['GET', 'POST'])
def signup_lec():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        if len(email) < 4 or '@' not in email:
            flash('Please enter a valid email address.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif User.query.filter_by(email=email).first():
            flash('Email already exists.', category='error')
        else:
            code = str(random.randint(1000, 9999))
            new_user = User(
                email=email, name=name, 
                password=generate_password_hash(password, method='pbkdf2:sha256'),
                is_lecturer=True, lecturer_code=code
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash(f'Lecturer account created! Your code is: {code}', category='success')
            return redirect(url_for('views.lecturer_dashboard'))
            
    return render_template("sign_uplec.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    is_lec = current_user.is_lecturer
    logout_user()
    flash('Logged out successfully.', category='info')
    
    if is_lec:
        return redirect(url_for('auth.login_lec'))
    return redirect(url_for('auth.login'))