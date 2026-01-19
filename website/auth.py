from flask import Blueprint, flash, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.utils import secure_filename

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            print("Login success!")
            return redirect(url_for('views.upload'))
        print("Login failed!")
    return render_template("login.html")

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')

        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            return redirect(url_for('auth.signup'))

        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(email=email, name=name, username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
        
    return render_template("sign_up.html")


@auth.route('/signup-lec', methods=['GET', 'POST'])
def signup_lec():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        is_lec = False
        if "lec" in email.lower():
            is_lec = True

        new_user = User(
            email=email, 
            name=name, 
            password=generate_password_hash(password, method='pbkdf2:sha256'),
            is_lecturer=is_lec
        )
        
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        return redirect(url_for('auth.login_lec'))

    return render_template("sign_uplec.html", user=current_user)

@auth.route('/login-lec', methods=['GET', 'POST'])
def login_lec():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            
            return redirect(url_for('views.lecturer_dashboard'))
        else:
            flash('Login failed.')

    return render_template("loginlec.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
        
