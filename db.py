from website import create_app, db
from website.models import User
import os

app = create_app()

with app.app_context():
   
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'website', 'db.sqlite3')
    
    print("create database")
    db.create_all()
    
