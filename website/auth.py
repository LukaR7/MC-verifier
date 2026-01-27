from flask import Blueprint, render_template, request, redirect, url_for
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
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
    return render_template("login.html", user=current_user)

@auth.route('/login-lec', methods=['GET', 'POST'])
def login_lec():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email, is_lecturer=True).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for('views.lecturer_dashboard'))
    return render_template("loginlec.html", user=current_user)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        
        new_user = User(email=email, name=name, 
                        password=generate_password_hash(password, method='pbkdf2:sha256'), 
                        is_lecturer=False)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        return redirect(url_for('views.upload'))
    return render_template("sign_up.html", user=current_user)

@auth.route('/signup-lec', methods=['GET', 'POST'])
def signup_lec():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        random_code = str(random.randint(1000, 9999))
        while User.query.filter_by(lecturer_code=random_code).first():
            random_code = str(random.randint(1000, 9999))

        new_user = User(email=email, name=name, 
                        password=generate_password_hash(password, method='pbkdf2:sha256'),
                        is_lecturer=True, lecturer_code=random_code)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        return redirect(url_for('views.lecturer_dashboard'))
    return render_template("sign_uplec.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))