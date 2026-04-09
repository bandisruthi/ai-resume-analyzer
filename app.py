from flask import Flask, request, render_template
from pdfminer.high_level import extract_text
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Role-based skills
ROLE_SKILLS = {
    "software_engineer": [
        "python", "java", "c++", "sql", "git", "oop"
    ],
    "web_developer": [
        "html", "css", "javascript", "bootstrap", "django"
    ],
    "data_analyst": [
        "python", "sql", "excel", "power bi", "pandas"
    ],
    "aiml_engineer": [
        "python", "machine learning", "ai", "deep learning", "nlp"
    ]
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['resume']
        role = request.form['role']

        # Save file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Extract text
        text = extract_text(file_path).lower()

        # Get role skills
        skills_required = ROLE_SKILLS.get(role, [])

        # Find skills
        found_skills = [skill for skill in skills_required if skill in text]

        # Score calculation
        score = int((len(found_skills) / len(skills_required)) * 100) if skills_required else 0

        # Missing skills
        missing_skills = [skill for skill in skills_required if skill not in found_skills]

        return render_template("result.html",
                               skills=found_skills,
                               score=score,
                               missing=missing_skills,
                               role=role)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)