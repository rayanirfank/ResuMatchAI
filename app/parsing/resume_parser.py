import fitz
import spacy
import re
import json

nlp = spacy.load("en_core_web_sm")

SKILLS_MASTER = [
    "python", "sql", "java", "scala", "r", "javascript", "typescript",
    "machine learning", "deep learning", "nlp", "computer vision",
    "data analysis", "data engineering", "data science", "statistics",
    "feature engineering", "model deployment", "etl", "data pipelines",
    "tensorflow", "pytorch", "keras", "scikit-learn", "xgboost",
    "pandas", "numpy", "matplotlib", "seaborn", "plotly",
    "aws", "gcp", "azure", "bigquery", "redshift", "snowflake",
    "spark", "hadoop", "kafka", "airflow", "dbt", "luigi",
    "docker", "kubernetes", "terraform", "git", "ci/cd",
    "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
    "power bi", "tableau", "looker", "excel",
    "communication", "leadership", "teamwork", "problem solving",
    "agile", "scrum", "project management"
]

TOOLS_MASTER = [
    "bigquery", "redshift", "snowflake", "databricks", "spark",
    "airflow", "dbt", "kafka", "luigi", "prefect",
    "docker", "kubernetes", "terraform", "jenkins", "github actions",
    "aws", "gcp", "azure", "s3", "ec2", "lambda",
    "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
    "power bi", "tableau", "looker", "excel", "google sheets",
    "jira", "confluence", "slack", "git", "github", "gitlab"
]

SENIORITY_KEYWORDS = {
    "vp": ["vp", "vice president", "head of", "director"],
    "lead": ["lead", "principal", "staff", "architect", "manager"],
    "senior": ["senior", "sr.", "sr "],
    "mid": ["mid", "intermediate", "associate"],
    "junior": ["junior", "jr.", "jr ", "entry", "graduate", "intern"]
}

def extract_text_from_pdf(file_bytes: bytes) -> str:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()
    return text.strip()

def extract_email(text: str):
    match = re.search(
        r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",
        text
    )
    return match.group(0) if match else None

def extract_phone(text: str):
    match = re.search(
        r"[\+]?[\d][\d\s\-\.\(\)]{7,}[\d]",
        text
    )
    return match.group(0).strip() if match else None

def extract_name(text: str):
    doc = nlp(text[:500])

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text

    return None

def extract_skills(text: str):
    text_lower = text.lower()
    found = []

    for skill in SKILLS_MASTER:
        if skill in text_lower and skill not in found:
            found.append(skill)

    return found

def extract_tools(text: str):
    text_lower = text.lower()
    found = []

    for tool in TOOLS_MASTER:
        if tool in text_lower and tool not in found:
            found.append(tool)

    return found

def extract_years_experience(text: str):
    patterns = [
        r"(\d+)\+?\s*years? of experience",
        r"(\d+)\+?\s*years? experience",
        r"experience of (\d+)\+?\s*years?",
        r"(\d+)\+?\s*yrs? of experience",
    ]

    for pattern in patterns:
        match = re.search(pattern, text.lower())

        if match:
            return int(match.group(1))

    return 0

def extract_seniority(text: str, years: int):
    text_lower = text.lower()

    for level, keywords in SENIORITY_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                return level

    if years >= 12:
        return "vp"
    elif years >= 8:
        return "lead"
    elif years >= 5:
        return "senior"
    elif years >= 2:
        return "mid"
    else:
        return "junior"

def extract_current_title(text: str):
    lines = text.strip().split("\n")

    title_keywords = [
        "engineer", "analyst", "scientist", "developer", "manager",
        "architect", "consultant", "director", "lead", "vp", "head"
    ]

    for line in lines[:15]:
        line_clean = line.strip()

        if 3 < len(line_clean) < 80:
            if any(kw in line_clean.lower() for kw in title_keywords):
                return line_clean

    return None

def extract_certifications(text: str):
    cert_keywords = [
        "aws certified", "google certified", "azure certified",
        "pmp", "cfa", "cissp", "cpa", "gcp certified",
        "tensorflow certificate", "databricks certified",
        "professional certificate", "certification"
    ]

    text_lower = text.lower()
    found = []

    for cert in cert_keywords:
        if cert in text_lower:
            found.append(cert.title())

    return found

def extract_education(text: str):
    edu_keywords = [
        "phd", "ph.d", "doctorate",
        "master", "msc", "mba", "m.s", "m.eng",
        "bachelor", "bsc", "b.s", "b.eng", "b.tech",
        "associate", "diploma"
    ]

    text_lower = text.lower()

    for kw in edu_keywords:
        if kw in text_lower:
            return kw.title()

    return None

def parse_resume_with_ai(raw_text: str) -> dict:
    years = extract_years_experience(raw_text)

    return {
        "full_name": extract_name(raw_text),
        "email": extract_email(raw_text),
        "phone": extract_phone(raw_text),
        "current_title": extract_current_title(raw_text),
        "years_experience": years,
        "seniority_level": extract_seniority(raw_text, years),
        "skills": extract_skills(raw_text),
        "tools": extract_tools(raw_text),
        "certifications": extract_certifications(raw_text),
        "education": extract_education(raw_text)
    }
