from collections import Counter


class CareerRecommendationService:

    ROLE_RULES = {
        "Data Analyst": {
            "skills": [
                "sql",
                "excel",
                "power bi",
                "tableau",
                "reporting",
                "data analysis"
            ]
        },

        "Data Engineer": {
            "skills": [
                "python",
                "sql",
                "etl",
                "spark",
                "airflow",
                "kafka",
                "data pipelines"
            ]
        },

        "Machine Learning Engineer": {
            "skills": [
                "python",
                "machine learning",
                "tensorflow",
                "keras",
                "pandas",
                "xgboost",
                "model deployment"
            ]
        },

        "Backend Developer": {
            "skills": [
                "python",
                "java",
                "sql",
                "restful api",
                "docker",
                "git"
            ]
        },

        "Frontend Developer": {
            "skills": [
                "html",
                "css",
                "javascript",
                "react",
                "typescript"
            ]
        }
    }

    @staticmethod
    def generate(candidate_skills, jobs):

        candidate_skills = {
            skill.lower().strip()
            for skill in candidate_skills
            if skill and skill.strip()
        }

        role_counter = Counter()

        for job in jobs:

            title = (
                job.title or ""
            ).lower()

            for role in (
                CareerRecommendationService
                .ROLE_RULES
            ):

                if role.lower() in title:
                    role_counter[role] += 2

            for role, config in (
                CareerRecommendationService
                .ROLE_RULES.items()
            ):

                overlap = len(
                    candidate_skills &
                    set(config["skills"])
                )

                role_counter[role] += overlap

        recommendations = []

        for role, score in (
            role_counter.most_common(3)
        ):

            role_skills = set(
                CareerRecommendationService
                .ROLE_RULES[role]["skills"]
            )

            matching_skills = sorted(
                candidate_skills &
                role_skills
            )

            missing_skills = sorted(
                role_skills -
                candidate_skills
            )

            recommendations.append({
                "role": role,

                "match_reason":
                    f"Strong overlap in {', '.join(matching_skills[:3])}.",

                "matching_skills":
                    matching_skills,

                "missing_skills":
                    missing_skills,

                "relevance_score":
                    score
            })

        return {
            "recommended_roles":
                recommendations
        }