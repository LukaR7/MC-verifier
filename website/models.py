from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    is_lecturer = db.Column(db.Boolean, default=False)
    lecturer_code = db.Column(db.String(4), unique=True) 

class MedicalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(150))
    issue_date = db.Column(db.String(150))
    serial_number = db.Column(db.String(150))
    subject_name = db.Column(db.String(150))
    file_name = db.Column(db.String(150))
    status = db.Column(db.String(20), default="Pending") 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    assigned_teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'))