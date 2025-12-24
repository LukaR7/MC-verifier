from flask import Blueprint, render_template

main = Blueprint('main',__name__)

@main.route('/')
def index():
    return render_template("auth.index")

@main.route('/index')
def profile():
    return render_template("index.html")