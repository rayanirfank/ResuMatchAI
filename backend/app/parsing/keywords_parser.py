import csv
import io
import json
from typing import List


def parse_keywords_file(file_bytes: bytes, filename: str) -> List[str]:
    """
    Accepts raw file bytes + filename.
    Supports .txt (one keyword per line) and .csv (first column used).
    Returns a cleaned list of keyword strings.
    """
    content = file_bytes.decode("utf-8", errors="ignore")

    if filename.endswith(".csv"):
        keywords = _parse_csv(content)
    else:
        # Default: treat as plain text, one keyword per line
        keywords = _parse_txt(content)

    return _clean(keywords)


def _parse_txt(content: str) -> List[str]:
    """Split by newline, strip whitespace."""
    lines = content.splitlines()
    return [line.strip() for line in lines if line.strip()]


def _parse_csv(content: str) -> List[str]:
    """
    Read the first column of every row.
    Handles both comma-separated and comma+space.
    """
    keywords = []
    reader = csv.reader(io.StringIO(content))
    for row in reader:
        if row:  # skip empty rows
            value = row[0].strip()
            if value:
                keywords.append(value)
    return keywords


def _clean(keywords: List[str]) -> List[str]:
    """
    Normalize: lowercase, strip extra spaces.
    Remove duplicates while preserving order.
    """
    seen = set()
    cleaned = []
    for kw in keywords:
        normalized = kw.lower().strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            cleaned.append(normalized)
    return cleaned


def merge_keywords(resume_keywords: List[str], file_keywords: List[str]) -> List[str]:
    """
    Merge two keyword lists. Deduplicate. Preserve order (resume first, file second).
    Returns unified profile.
    """
    seen = set()
    merged = []
    for kw in resume_keywords + file_keywords:
        normalized = kw.lower().strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            merged.append(normalized)
    return merged