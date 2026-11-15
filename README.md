# AI-Powered Resume Screening System

A Django portfolio project that extracts text from PDF resumes, identifies technical skills, compares resume content with a job description using TF-IDF and cosine similarity, ranks candidates, and exports results to CSV.

## Features

- Upload multiple PDF resumes.
- Extract text using `pypdf`.
- Identify skills from a configurable starter skill list.
- Compare resume text with a job description using TF-IDF + cosine similarity.
- Display ranked candidates and skill matches.
- Export screening results as CSV.
- Store screening sessions and candidate results in SQLite by default.

> **Important:** This is an educational decision-support demo, not a validated hiring assessment tool. Similarity scores are text similarity signals, not probabilities of job performance or suitability. Do not use the scores as the sole basis for hiring decisions. Review resumes manually and obtain consent before processing personal data.

## Requirements

- Python 3.10 or newer
- VS Code (recommended)
- Internet connection for installing dependencies

## 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
```

Windows Command Prompt:

```bat
py -m venv .venv
.venv\\Scripts\\activate.bat
```

If PowerShell blocks activation, use Command Prompt or follow Microsoft's execution-policy guidance. Do not change system security settings unnecessarily.

## 2. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Create the database

```bash
python manage.py makemigrations
python manage.py migrate
```

## 4. Create an admin account (optional)

```bash
python manage.py createsuperuser
```

## 5. Run the application

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

## How to use

1. Enter a role title and paste the job description.
2. Select one or more PDF resumes.
3. Click **Screen resumes**.
4. Review the ranked results and matched skills.
5. Use **Download CSV** to export the current screening session.

## Project structure

```text
ai_resume_screening_system/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── resume_screener/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── screening/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── services.py
    ├── urls.py
    ├── views.py
    ├── migrations/
    │   └── __init__.py
    ├── templates/
    │   └── screening/
    │       ├── base.html
    │       ├── home.html
    │       └── results.html
    └── static/
        └── screening/
            └── style.css
```

## GitHub upload

Create a **Public** repository named `ai-resume-screening-system`, then run these commands from the project folder:

```bash
git init
git add .
git commit -m "Build AI resume screening system"
git branch -M main
git remote add origin https://github.com/YOUR-GITHUB-USERNAME/ai-resume-screening-system.git
git push -u origin main
```

Replace `YOUR-GITHUB-USERNAME` with your GitHub username. Never commit real resumes, personal data, database files, passwords, or API keys. The `.gitignore` file excludes local media uploads and the SQLite database.

## Before publishing

- Test with sample resumes that you created yourself or have permission to use.
- Add screenshots to the README after running the app.
- Explain the TF-IDF/cosine similarity method accurately in interviews.
- Do not claim the project uses a large language model or deep-learning model; this version uses classical NLP similarity.
- For real deployment, configure a production secret key, `DEBUG=False`, HTTPS, upload limits, access controls, retention/deletion procedures, and privacy notices.
