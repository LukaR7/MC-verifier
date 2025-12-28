from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("index.html", user=current_user)

@views.route('/upload')
def upload():
    return "<h1>Upload Feature - Coming Soon!</h1>"
