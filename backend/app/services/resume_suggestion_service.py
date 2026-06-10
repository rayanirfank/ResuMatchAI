class ResumeSuggestionService:

    SKILL_ACTIONS = {
        "git": "Mention Git branching, commits, pull requests, and collaboration in project descriptions.",
        "react": "Add a React-based project and highlight component design, state management, and API integration.",
        "excel": "Include Excel-based reporting, dashboards, pivot tables, or data analysis work.",
        "typescript": "Demonstrate TypeScript usage in frontend projects and mention type-safe development.",
        "kafka": "Build an event-driven pipeline project and explain message streaming concepts.",
        "aws": "Add cloud-hosted projects and describe the AWS services used.",
        "docker": "Containerize an existing project and include deployment details.",
        "tableau": "Publish dashboards and include measurable business insights.",
        "power bi": "Show business intelligence dashboards and reporting projects.",
        "airflow": "Build automated workflows and scheduled pipelines.",
        "spark": "Work on large-scale data processing projects.",
        "etl": "Create end-to-end ETL pipelines using real datasets."
    }

    @staticmethod
    def _priority(frequency):

        if frequency >= 5:
            return "High"

        if frequency >= 2:
            return "Medium"

        return "Low"

    @staticmethod
    def generate(skill_gap_analysis):

        frequencies = skill_gap_analysis.get(
            "skill_frequency",
            {}
        )

        suggestions = []

        for skill, frequency in list(
            frequencies.items()
        )[:5]:

            suggestions.append({
                "skill": skill,

                "priority":
                    ResumeSuggestionService._priority(
                        frequency
                    ),

                "why":
                    f"Appears in {frequency} of your top matched jobs.",

                "resume_action":
                    ResumeSuggestionService.SKILL_ACTIONS.get(
                        skill,
                        f"Add evidence of {skill} through projects, coursework, certifications, or experience."
                    )
            })

        return {
            "total_suggestions": len(
                suggestions
            ),
            "suggestions": suggestions
        }