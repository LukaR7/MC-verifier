from website import create_app, db
from website.models import User
import os

app = create_app()

with app.app_context():
   
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'website', 'db.sqlite3')
    
    print("Attempting to create database...")
    db.create_all()
    
    if os.path.exists(db_path):
        print(f"✅ SUCCESS! Database created at: {db_path}")
    else:
       
        instance_path = os.path.join(basedir, 'instance', 'db.sqlite3')
        if os.path.exists(instance_path):
            print(f"✅ SUCCESS! Database created in instance folder: {instance_path}")
        else:
            print("❌ Still not working. Check for errors above.")