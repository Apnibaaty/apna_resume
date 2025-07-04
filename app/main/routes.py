import pdfplumber
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db, Resume

main = Blueprint('main', __name__)

@main.route('/')
def landing():
    # If user is logged in, redirect to /home
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    return render_template('landing.html')

@main.route('/home')
@login_required
def home():
    return render_template('home.html')

@main.route('/optimize', methods=['POST'])
@login_required
def optimize():
    resume_text = request.form.get('resume_text')
    resume_file = request.files.get('resume_file')
    extracted_text = ""

    if resume_file and resume_file.filename.endswith('.pdf'):
        with pdfplumber.open(resume_file) as pdf:
            for page in pdf.pages:
                extracted_text += page.extract_text() + "\n"

    final_text = resume_text if resume_text else extracted_text

    if not final_text.strip():
        flash("Please enter text or upload a valid resume PDF.")
        return redirect(url_for('main.home'))

    # Mock feedback generation
    feedback = []
    if len(final_text.split()) < 100:
        feedback.append("⚠️ Your resume seems too short.")
    if "teamwork" not in final_text.lower():
        feedback.append("⚠️ Consider adding examples of teamwork.")
    if "skills" not in final_text.lower():
        feedback.append("⚠️ Mention your skills section.")
    if "project" not in final_text.lower():
        feedback.append("⚠️ Add past projects to make your resume stronger.")

    feedback_text = "✅ Looks good!" if not feedback else "<br>".join(feedback)

    # Save to database
    resume_entry = Resume(
        text=final_text,
        feedback=feedback_text,
        user_id=current_user.id
    )
    db.session.add(resume_entry)
    db.session.commit()

    return render_template('optimize.html', feedback=feedback_text)
