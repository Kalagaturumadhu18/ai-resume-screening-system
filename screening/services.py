import re
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Starter vocabulary. Extend this list as the project grows.
SKILLS = [
    "python", "java", "javascript", "typescript", "c", "c++", "c#", "sql",
    "mysql", "postgresql", "sqlite", "django", "flask", "fastapi",
    "html", "css", "react", "node.js", "git", "github", "rest api",
    "machine learning", "deep learning", "natural language processing",
    "nlp", "scikit-learn", "pandas", "numpy", "tensorflow", "pytorch",
    "data analysis", "data visualization", "power bi", "tableau",
    "excel", "aws", "azure", "docker", "linux", "api testing",
    "selenium", "pytest", "data structures", "algorithms"
]

def extract_pdf_text(uploaded_file):
    """Extract selectable text from a PDF. Scanned image-only PDFs need OCR."""
    reader = PdfReader(uploaded_file)
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    text = "\n".join(pages).strip()
    if not text:
        raise ValueError("No selectable text found. This may be a scanned PDF; OCR is not included.")
    return text


def normalize_text(text):
    return re.sub(r"\s+", " ", text.lower()).strip()


def find_skills(text):
    normalized = normalize_text(text)
    found = []
    for skill in SKILLS:
        pattern = r"(?<![a-z0-9+#.])" + re.escape(skill) + r"(?![a-z0-9+#.])"
        if re.search(pattern, normalized):
            found.append(skill)
    return sorted(set(found))


def calculate_similarity(job_description, resume_text):
    """Return a text-similarity percentage using TF-IDF and cosine similarity."""
    documents = [job_description, resume_text]
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(documents)
    score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
    return round(float(score) * 100, 2)


def analyze_resume(job_description, resume_text):
    job_skills = set(find_skills(job_description))
    resume_skills = set(find_skills(resume_text))
    matched = sorted(job_skills & resume_skills)
    missing = sorted(job_skills - resume_skills)

    try:
        score = calculate_similarity(job_description, resume_text)
    except ValueError:
        score = 0.0

    return {
        "score": score,
        "matched_skills": matched,
        "missing_skills": missing,
    }
