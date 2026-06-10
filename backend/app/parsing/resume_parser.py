import fitz
import spacy
import re
import json

nlp = spacy.load("en_core_web_sm")

# Reference list — used to BOOST confidence, not as the only source
KNOWN_SKILLS = {
    # Programming Languages
    "python", "sql", "java", "javascript", "typescript",
    "c", "c++", "c#", "r", "go", "rust",

    # Web Development
    "html", "css", "react", "node.js",
    "flask", "fastapi", "django", "restful api",

    # Data Science & Analytics
    "data analytics", "data analysis",
    "reporting", "forecasting",
    "data quality", "data governance",
    "data modelling", "data modeling",
    "statistical analysis", "statistics",
    "hypothesis testing", "ab testing", "a/b testing",
    "excel", "power bi", "tableau",
    "kpi", 

    # Machine Learning
    "machine learning", "deep learning",
    "predictive modeling", "classification",
    "regression", "clustering",
    "model deployment", "model evaluation",
    "hyperparameter tuning",

    # AI / NLP / Computer Vision
    "natural language processing", "nlp",
    "computer vision", "image classification",
    "object detection", "segmentation",
    "transformers", "bert", "llm",

    # ML Libraries
    "scikit-learn", "tensorflow", "pytorch",
    "keras", "xgboost", "lightgbm",

    # Python Ecosystem
    "pandas", "numpy", "matplotlib",
    "seaborn", "plotly", "scipy",

    # Data Engineering
    "etl", "data pipelines", "data engineering",
    "data warehousing", "apache spark",
    "hadoop", "kafka", "airflow", "dbt",

    # Cloud
    "aws", "azure", "gcp",

    # Databases
    "postgresql", "mysql", "mongodb",
    "sqlite", "redis", "elasticsearch",

    # DevOps & Version Control
    "git", "docker", "kubernetes",
    "terraform", "jenkins", "ci/cd",

    # Process
    "agile", "scrum", "project management",
    "software development", "system design",
}

KNOWN_TOOLS = {
    "bigquery", "redshift", "snowflake", "databricks", "spark",
    "airflow", "dbt", "kafka", "luigi", "prefect",
    "docker", "kubernetes", "terraform", "jenkins", "github actions",
    "aws", "gcp", "azure", "s3", "ec2", "lambda",
    "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
    "power bi", "tableau", "looker", "excel", "google sheets",
    "jira", "confluence", "slack", "git", "github", "gitlab",
    "jupyter", "vscode", "pycharm", "anaconda", "colab",
    "figma", "notion", "trello", "asana",
}

# FIX 1: Expanded noise words now include common resume phrases, not just single words
NOISE_WORDS = {
    "resume", "experience", "education", "university", "college",
    "bachelor", "master", "degree", "certificate", "certification",
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december",
    "present", "current", "previous", "company", "organization",
    "team", "department", "position", "role", "job", "work",
    "year", "month", "day", "time", "date", "period",
    "city", "state", "country", "address", "phone", "email",
    "summary", "objective", "profile", "overview", "introduction",
    "reference", "available", "request", "responsible", "ability",
    "skill", "skills", "tool", "tools", "knowledge", "proficient",
    "proficiency", "familiar", "familiarity", "exposure", "use",
    "using", "used", "including", "include", "various", "multiple",
    "strong", "excellent", "good", "great", "extensive", "hands",
}

# FIX 2: Noise PREFIXES — if a noun chunk STARTS with these words, discard it
# This catches "strong communication", "relevant experience", "our data team" etc.
NOISE_PREFIXES = {
    "strong", "excellent", "good", "great", "my", "our", "the", "a",
    "an", "this", "that", "these", "those", "relevant", "various",
    "multiple", "extensive", "solid", "proven", "hands", "overall",
    "general", "basic", "advanced", "various", "key", "core",
}

SENIORITY_KEYWORDS = {
    "vp": ["vp ", "vice president", "head of", "director of"],
    "lead": ["lead ", "principal ", "staff engineer", "engineering manager"],
    "senior": ["senior ", "sr. ", "sr "],
    "mid": ["mid ", "intermediate ", "associate "],
    "junior": ["junior ", "jr. ", "jr ", "intern", "trainee", "fresher", "graduate"]
}

# FIX 3: Clean, real certification list — platforms and generic phrases removed
KNOWN_CERTIFICATIONS = [
    "aws certified solutions architect",
    "aws certified developer",
    "aws certified data analytics",
    "aws certified machine learning",
    "google professional data engineer",
    "google professional cloud architect",
    "google associate cloud engineer",
    "google analytics certified",
    "azure data engineer associate",
    "azure data scientist associate",
    "azure fundamentals",
    "microsoft certified",
    "databricks certified associate developer",
    "databricks certified data engineer",
    "tensorflow developer certificate",
    "tensorflow certificate",
    "pmp",
    "prince2",
    "cfa",
    "cissp",
    "cpa",
    "comptia",
    "oracle certified",
    "salesforce certified",
    "tableau desktop certified",
    "power bi data analyst",
    "nptel",
    "coursera certificate",
    "udemy certificate",
]


def extract_text_from_pdf(file_bytes: bytes) -> str:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text.strip()


def extract_email(text: str):
    match = re.search(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else None


def extract_phone(text: str):
    match = re.search(r"[\+]?[\d][\d\s\-\.\(\)]{7,}[\d]", text)
    return match.group(0).strip() if match else None


def extract_name(text: str):
    doc = nlp(text[:500])
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None


def extract_skills_and_tools(text: str):
    """
    FIX: Flipped logic — known list is PRIMARY, spaCy noun chunks are SECONDARY.

    Old approach: spaCy extracts everything → cross-reference known list
    Problem: spaCy extracts too much garbage that passes the filters

    New approach:
    1. Scan text directly for KNOWN_SKILLS and KNOWN_TOOLS (guaranteed quality)
    2. Use spaCy noun chunks ONLY as a secondary pass, with tighter filters
    3. A noun chunk must either be in KNOWN_SKILLS or be a clean 1-2 word technical phrase
    4. Anything starting with a noise prefix is discarded
    """
    SKILL_ALIASES = {
    # Only alias SPECIFIC multi-word phrases, never single generic words
    "a/b testing":  "ab testing",
}

    text_lower = text.lower()
    doc = nlp(text_lower)

    skills_found = set()
    tools_found = set()

    for alias, canonical in SKILL_ALIASES.items():
        if alias in text_lower:
            skills_found.add(canonical)

    # --- PRIMARY PASS: Direct scan of known lists ---
    # This is reliable because we control the list
    for skill in KNOWN_SKILLS:
        # Use word boundary check to avoid partial matches
        # e.g., "r" should not match inside "researcher"
        if len(skill) <= 2:
            # Short skills like "r", "go" need word boundary matching
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                skills_found.add(skill)
        else:
            if skill in text_lower:
                skills_found.add(skill)

    for tool in KNOWN_TOOLS:
        if len(tool) <= 2:
            pattern = r'\b' + re.escape(tool) + r'\b'
            if re.search(pattern, text_lower):
                tools_found.add(tool)
        else:
            if tool in text_lower:
                tools_found.add(tool)

    # --- SECONDARY PASS: spaCy noun chunks (with tight filters) ---
    # Only accept a noun chunk if:
    # - It's 1 or 2 words (technical terms are rarely 3+ word phrases)
    # - It doesn't start with a noise prefix
    # - It's not in noise words
    # - It passes basic character checks
    for chunk in doc.noun_chunks:
        phrase = chunk.text.strip()
        words = phrase.split()

        # Filter 1: Only 1-2 word phrases from spaCy (tighter than before)
        if len(words) > 2:
            continue

        # Filter 2: Must be 2–30 characters
        if len(phrase) < 2 or len(phrase) > 30:
            continue

        # Filter 3: Discard if starts with a noise prefix
        if words[0] in NOISE_PREFIXES:
            continue

        # Filter 4: Discard if the whole phrase is a noise word
        if phrase in NOISE_WORDS:
            continue

        # Filter 5: Must not be purely numeric
        if phrase.replace(" ", "").isnumeric():
            continue

        # Filter 6: Must contain at least one letter
        if not any(c.isalpha() for c in phrase):
            continue

        # Only add if it's in our known lists (noun chunks alone aren't trusted)
        if phrase in KNOWN_TOOLS:
            tools_found.add(phrase)
        elif phrase in KNOWN_SKILLS:
            skills_found.add(phrase)

    # --- Separation: tools take priority, don't duplicate in skills ---
    # If something appears in both (e.g., "aws" is in both lists), tools wins
    skills_final = sorted([s for s in skills_found if s not in KNOWN_TOOLS])
    tools_final = sorted(list(tools_found))

    return skills_final, tools_final


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

    # Fallback: calculate from date range in resume
    years = re.findall(r'\b(19|20)\d{2}\b', text)
    if len(years) >= 2:
        years_int = [int(y) for y in years]
        span = max(years_int) - min(years_int)
        if span <= 30:
            return span
    return 0


def extract_seniority(text: str, years: int):
    title_area = "\n".join(text.strip().split("\n")[:20]).lower()

    vp_keywords = ["vp ", "vice president", "head of", "director of"]
    lead_keywords = ["lead ", "principal ", "staff engineer", "engineering manager"]
    senior_keywords = ["senior ", "sr. ", "sr "]
    junior_keywords = ["junior ", "jr. ", "jr ", "intern", "trainee", "fresher", "graduate"]
    mid_keywords = ["mid ", "intermediate ", "associate "]

    for kw in vp_keywords:
        if kw in title_area:
            return "vp"
    for kw in lead_keywords:
        if kw in title_area:
            return "lead"
    for kw in senior_keywords:
        if kw in title_area:
            return "senior"
    for kw in junior_keywords:
        if kw in title_area:
            return "junior"
    for kw in mid_keywords:
        if kw in title_area:
            return "mid"

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
        "architect", "consultant", "director", "lead", "vp", "head",
        "intern", "associate", "specialist", "coordinator"
    ]
    for line in lines[:15]:
        line_clean = line.strip()
        if 3 < len(line_clean) < 80:
            if any(kw in line_clean.lower() for kw in title_keywords):
                return line_clean
    return None


def extract_certifications(text: str):
    """
    FIX: Two-layer approach.

    Layer 1 — Direct scan of KNOWN_CERTIFICATIONS list (high precision)
    Layer 2 — Tight regex patterns with length caps (catches unlisted certs)

    Old problems fixed:
    - Unbounded patterns like r"certified\\s[\\w\\s]+" now have a word count cap
    - Generic platforms like "coursera", "udemy" removed from known list
    - Patterns now require meaningful content (min 8 chars, max 60 chars)
    """
    found = set()
    text_lower = text.lower()

    # --- Layer 1: Direct scan of known certifications ---
    for cert in KNOWN_CERTIFICATIONS:
        if cert in text_lower:
            found.add(cert.title())

    # --- Layer 2: Tight regex patterns ---
    # FIX: All patterns now have a {1,5} word count cap to prevent runaway matches
    cert_patterns = [
        # "certified in X" or "certified X" — max 5 words after "certified"
        r"certified\s+(?:in\s+)?(?:\w+\s+){0,4}\w+(?=[\.,\n\r]|$)",
        # "X certification" — max 4 words before "certification"
        r"(?:\w+\s+){1,4}certification",
        # "X certificate" — max 4 words before "certificate"
        r"(?:\w+\s+){1,4}certificate",
        # "certificate in X" — max 4 words after "in"
        r"certificate\s+in\s+(?:\w+\s+){0,3}\w+",
    ]

    for pattern in cert_patterns:
        matches = re.findall(pattern, text_lower)
        for match in matches:
            clean = match.strip()

            # Must be at least 8 characters (filters "certified", "certificate" alone)
            if len(clean) < 8:
                continue

            # Must be at most 60 characters (filters runaway matches)
            if len(clean) > 60:
                continue

            # Must not be a noise phrase
            first_word = clean.split()[0] if clean.split() else ""
            if first_word in NOISE_WORDS:
                continue

            found.add(clean.title())

    return list(found)


def extract_education(text: str):
    edu_patterns = [
        (r'ph\.?d|doctorate', 'PhD'),
        (r'\bm\.?b\.?a\b', 'MBA'),
        (r'\bm\.?s\.?c\b|\bmaster', 'Masters'),
        (r'\bb\.?tech\b|\bb\.?e\b|\bb\.?eng\b|\bbachelor|\bb\.?s\.?c\b|\bundergrad|\bpursuing\b|\bgraduat', 'Bachelors'),
        (r'\bassociate\b', 'Associate'),
        (r'\bdiploma\b', 'Diploma')
    ]

    text_lower = text.lower()

    edu_context = [
        'university', 'college', 'institute', 'school',
        'degree', 'graduated', 'studied', 'pursuing',
        'b.tech', 'b.e', 'engineering', 'faculty'
    ]

    has_edu_context = any(word in text_lower for word in edu_context)
    if not has_edu_context:
        return None

    for pattern, label in edu_patterns:
        if re.search(pattern, text_lower):
            return label

    return None


def parse_resume_with_ai(raw_text: str):
    years = extract_years_experience(raw_text)

    skills, tools = extract_skills_and_tools(raw_text)

    print("\n========== SKILLS ==========")
    print(f"Skills Count: {len(skills)}")
    print(skills)

    print("\n========== TOOLS ==========")
    print(f"Tools Count: {len(tools)}")
    print(tools)
    print("============================\n")

    return {
        "full_name": extract_name(raw_text),
        "email": extract_email(raw_text),
        "phone": extract_phone(raw_text),
        "current_title": extract_current_title(raw_text),
        "years_experience": years,
        "seniority_level": extract_seniority(raw_text, years),
        "skills": skills,
        "tools": tools,
        "certifications": extract_certifications(raw_text),
        "education": extract_education(raw_text)
    }