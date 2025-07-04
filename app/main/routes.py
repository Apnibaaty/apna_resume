import pdfplumber
from flask import Blueprint, render_template, request, redirect, url_for, flash

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/optimize', methods=['POST'])
def optimize():
    resume_text = request.form.get('resume_text')
    resume_file = request.files.get('resume_file')
    extracted_text = ""

    # If a PDF is uploaded
    if resume_file and resume_file.filename.endswith('.pdf'):
        with pdfplumber.open(resume_file) as pdf:
            for page in pdf.pages:
                extracted_text += page.extract_text() + "\n"

    # Use either the typed text or the extracted one
    final_text = resume_text if resume_text else extracted_text

    if not final_text.strip():
        flash("Please enter text or upload a valid resume PDF.")
        return redirect(url_for('main.home'))

    # Very basic mock feedback
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

    return render_template('optimize.html', feedback=feedback_text)
