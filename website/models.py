from . import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    records = db.relationship('MedicalRecord', backref='owner')

class MedicalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(150)) 
    issue_date = db.Column(db.String(100))    
    raw_text = db.Column(db.Text)            
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))