import json


class ATSAnalysisService:

    @staticmethod
    def analyze(candidate):

        score = 0

        skills = candidate.skills or "[]"
        tools = candidate.tools or "[]"
        certifications = candidate.certifications or "[]"

        try:
            skills = json.loads(skills)
        except Exception:
            skills = []

        try:
            tools = json.loads(tools)
        except Exception:
            tools = []

        try:
            certifications = json.loads(certifications)
        except Exception:
            certifications = []

        years_experience = (
            candidate.years_experience or 0
        )

        education = (
            candidate.education or ""
        )

        # Skills (30 points)

        score += min(
            len(skills) * 2,
            30
        )

        # Tools (20 points)

        score += min(
            len(tools) * 2,
            20
        )

        # Certifications (15 points)

        score += min(
            len(certifications) * 5,
            15
        )

        # Experience (20 points)

        score += min(
            years_experience * 4,
            20
        )

        # Education (15 points)

        if education:
            score += 15

        score = min(score, 100)

        if score >= 85:
            status = "Excellent"
            message = "Highly ATS optimized"

        elif score >= 70:
            status = "Good"
            message = "Improve to reach excellent"

        elif score >= 50:
            status = "Average"
            message = "Add more skills and certifications"

        else:
            status = "Needs Improvement"
            message = "Resume lacks ATS signals"

        return {
            "ats_score": score,
            "status": status,
            "message": message
        }