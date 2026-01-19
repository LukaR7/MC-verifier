from flask import Blueprint, current_app, flash, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import pytesseract
from PIL import Image
import re
from .models import MedicalRecord
from . import db                  
views = Blueprint('views', __name__)

def extract_info(text):
    date_pattern = r'(\d{1,2}[/-]\d{1,2}[/-]\d{4})'
    date_found = re.search(date_pattern, text)
    
    name_pattern = r'(?:Name|Patient|Student):\s*([A-Za-z\s]+)'
    name_found = re.search(name_pattern, text, re.IGNORECASE)

    return {
        "date": date_found.group(1) if date_found else "Unknown",
        "name": name_found.group(1).strip() if name_found else "Unknown"
    }



@views.route('/')
def home():
    if current_user.is_authenticated and current_user.is_lecturer:
        return redirect(url_for('views.lecturer_dashboard'))
    return render_template("index.html", user=current_user)

@views.route('/upload', methods=['GET', 'POST'])
@login_required 
def upload():
    if request.method == 'POST':
        form_serial = request.form.get('serial_number')
        form_subject = request.form.get('subject')  #
        manual_name = request.form.get('student_name')
        manual_date = request.form.get('issue_date')
        
        f = request.files.get('file')
        if not f or f.filename == '':
            flash("No file selected!")
            return redirect(request.url)

        folder = os.path.join('website', 'static', 'uploads')
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        file_path = os.path.join(folder, secure_filename(f.filename))
        f.save(file_path)

        try:
            text_data = pytesseract.image_to_string(Image.open(file_path))
            
        except:
            text_data = "Could not read image"

        
        new_entry = MedicalRecord(
            student_name=manual_name,    
            issue_date=manual_date,     
            serial_number=form_serial,  
            subject_name=form_subject,  
            raw_text=text_data,
            user_id=current_user.id
        )
        db.session.add(new_entry)
        db.session.commit()

        flash(f"Success! Record for {form_subject} uploaded.")
        return redirect(url_for('views.student_dashboard'))

    return render_template("upload.html", user=current_user)

@views.route('/lecturer-dashboard')
@login_required
def lecturer_dashboard():
   

    all_records = MedicalRecord.query.all() 
    return render_template("lecture_dashboard.html", user=current_user, records=all_records)

@views.route('/student-dashboard')
@login_required
def student_dashboard():
    user_records = MedicalRecord.query.filter_by(user_id=current_user.id).all()
    return render_template("student_dashboard.html", user=current_user, records=user_records)


