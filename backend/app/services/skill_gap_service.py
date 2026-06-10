from collections import Counter

from app.parsing.resume_parser import (
    extract_skills_and_tools
)


class SkillGapService:
    """
    Analyze candidate skill coverage
    against extracted job requirements.
    """

    @staticmethod
    def analyze(candidate_skills, jobs):

        candidate_skills = {
            skill.strip().lower()
            for skill in candidate_skills
            if skill and skill.strip()
        }

        required_skills = []

        for job in jobs:

            job_text = f"""
            {job.title or ""}
            {job.description or ""}
            """

            job_skills, job_tools = (
                extract_skills_and_tools(job_text)
            )

            all_job_skills = (
                job_skills +
                job_tools
            )

            if not all_job_skills:
                continue

            required_skills.extend(
                skill.lower().strip()
                for skill in all_job_skills
                if skill and skill.strip()
            )

        if not required_skills:
            return {
                "coverage_score": 0,
                "matched_skills": [],
                "missing_skills": [],
                "skill_frequency": {}
            }

        required_unique = set(required_skills)

        matched = sorted(
            candidate_skills.intersection(
                required_unique
            )
        )

        missing = sorted(
            required_unique.difference(
                candidate_skills
            )
        )

        coverage = round(
            (
                len(matched)
                / len(required_unique)
            ) * 100,
            2
        )

        frequency = Counter(required_skills)

        skill_frequency = {
            skill: frequency[skill]
            for skill in missing
        }

        skill_frequency = dict(
            sorted(
                skill_frequency.items(),
                key=lambda x: x[1],
                reverse=True
            )
        )

        return {
            "coverage_score": coverage,
            "matched_skills": matched,
            "missing_skills": missing,
            "skill_frequency": skill_frequency
        }