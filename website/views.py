from flask import Blueprint, flash, render_template, request, redirect, url_for
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
    return render_template("index.html", user=current_user)

@views.route('/upload', methods=['GET', 'POST'])
@login_required 
def upload():
    if request.method == 'POST':
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
            info = extract_info(text_data)
        except:
            text_data = "Could not read image"
            info = {"name": "Unknown", "date": "Unknown"}

        new_entry = MedicalRecord(
            student_name=info['name'],
            issue_date=info['date'],
            raw_text=text_data,
            user_id=current_user.id
        )
        db.session.add(new_entry)
        db.session.commit()

        flash(f"Success! Found Name: {info['name']}")
        return redirect(url_for('views.home'))

    return render_template("upload.html", user=current_user)




