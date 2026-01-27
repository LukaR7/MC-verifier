from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from .models import MedicalRecord, User 
from . import db
views = Blueprint('views', __name__)

@views.route('/')
def home():
    if not current_user.is_authenticated:
        return render_template("index.html", user=current_user)
    if current_user.is_lecturer:
        return redirect(url_for('views.lecturer_dashboard'))
    return redirect(url_for('views.student_dashboard'))

@views.route('/student-dashboard')
@login_required
def student_dashboard():
    recs = MedicalRecord.query.filter_by(user_id=current_user.id).all()
    return render_template("student_dashboard.html", user=current_user, records=recs)

@views.route('/lecturer-dashboard')
@login_required
def lecturer_dashboard():
    recs = MedicalRecord.query.filter_by(assigned_teacher_id=current_user.id).all()
    return render_template("lecture_dashboard.html", user=current_user, records=recs)

@views.route('/update-status/<int:record_id>', methods=['POST'])
@login_required
def update_status(record_id):
    record = MedicalRecord.query.get(record_id)
    if record and record.assigned_teacher_id == current_user.id:
        record.status = request.form.get('status')
        db.session.commit()
    return redirect(url_for('views.lecturer_dashboard'))

@views.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        teacher_code = request.form.get('teacher_id')
        target_lec = User.query.filter_by(lecturer_code=teacher_code, is_lecturer=True).first()
        if target_lec:
            f = request.files.get('file')
            filename = secure_filename(f.filename)
            path = os.path.join(os.path.dirname(__file__), 'static/uploads')
            if not os.path.exists(path): os.makedirs(path)
            f.save(os.path.join(path, filename))
            new_rec = MedicalRecord(
                student_name=request.form.get('student_name'),
                issue_date=request.form.get('issue_date'),
                serial_number=request.form.get('serial_number'),
                subject_name=request.form.get('subject'),
                file_name=filename,
                user_id=current_user.id,
                assigned_teacher_id=target_lec.id,
                status="Pending"
            )
            db.session.add(new_rec)
            db.session.commit()
            return redirect(url_for('views.student_dashboard'))
    return render_template("upload.html", user=current_user)