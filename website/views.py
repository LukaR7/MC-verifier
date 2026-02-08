from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import easyocr
from .models import MedicalRecord, User 
from . import db

views = Blueprint('views', __name__)
reader = easyocr.Reader(['en'], gpu=False)

@views.route('/')
def index():
    return render_template("index.html", user=current_user)

@views.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        teacher_code = request.form.get('teacher_id')
        manual_name = request.form.get('student_name')
        manual_date = request.form.get('issue_date')
        subject = request.form.get('subject')
        
        target_lec = User.query.filter_by(lecturer_code=teacher_code, is_lecturer=True).first()
        if not target_lec:
            flash('Invalid Lecturer Code!', category='error')
            return redirect(url_for('views.upload'))

        file = request.files.get('file')
        if not file: return redirect(url_for('views.upload'))

        filename = secure_filename(file.filename)
        upload_path = os.path.join(current_app.root_path, 'static', 'uploads', filename)
        file.save(upload_path)

        status = "Under Review"
        ocr_feedback = "OCR Match Found"

        try:
            file.seek(0)
            img_bytes = file.read()
            results = reader.readtext(img_bytes, detail=0)
            full_text = " ".join(results).lower()

            year = manual_date.split('-')[0]
            
            
            mismatches = []
            
            
            if manual_name.lower() not in full_text:
                mismatches.append("Name")
            
            
            if year not in full_text:
                mismatches.append("Year")
                
            
            if mismatches:
                
                ocr_feedback = f"SYSTEM_FLAG: {' and '.join(mismatches)} mismatch."
            
            
        except Exception as e:
            ocr_feedback = "SYSTEM_FLAG: OCR failed to process."

        new_record = MedicalRecord(
            student_name=manual_name,
            issue_date=manual_date,
            subject_name=subject,
            file_name=filename,
            status=status,
            comment=ocr_feedback,
            user_id=current_user.id,
            assigned_teacher_id=target_lec.id
        )
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('views.student_dashboard'))
            
    return render_template("upload.html", user=current_user)


@views.route('/update-status/<int:record_id>', methods=['POST'])
@login_required
def update_status(record_id):
    record = MedicalRecord.query.get(record_id)
    if record and record.assigned_teacher_id == current_user.id:
        record.status = request.form.get('status')
        record.comment = request.form.get('comment')
        db.session.commit()
    return redirect(url_for('views.lecturer_dashboard'))

@views.route('/lecturer-dashboard')
@login_required
def lecturer_dashboard():
    records = MedicalRecord.query.filter_by(assigned_teacher_id=current_user.id).all()
    return render_template("lecture_dashboard.html", user=current_user, records=records)

@views.route('/student-dashboard')
@login_required
def student_dashboard():
    records = MedicalRecord.query.filter_by(user_id=current_user.id).all()
    return render_template("student_dashboard.html", user=current_user, records=records) 