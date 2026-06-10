from collections import defaultdict


class SalaryIntelligenceService:

    COUNTRY_CURRENCY = {
        "us": "USD",
        "gb": "GBP",
        "ca": "CAD",
        "au": "AUD",
        "in": "INR",
        "sg": "SGD"
    }

    @staticmethod
    def generate(jobs):

        country_salaries = defaultdict(list)

        for job in jobs:

            if (
                job.salary_min is None and
                job.salary_max is None
            ):
                continue

            if (
                job.salary_min is not None and
                job.salary_max is not None
            ):
                salary = (
                    job.salary_min +
                    job.salary_max
                ) / 2

            elif job.salary_min is not None:
                salary = job.salary_min

            else:
                salary = job.salary_max

            country_salaries[
                job.country or "unknown"
            ].append(salary)

        if not country_salaries:
            return {
                "salary_data_available": False,
                "message": "No salary data available."
            }

        country_breakdown = []

        for country, values in (
            country_salaries.items()
        ):

            avg_salary = round(
                sum(values) / len(values),
                2
            )

            country_breakdown.append({
                "country": country,
                "currency": (
                    SalaryIntelligenceService
                    .COUNTRY_CURRENCY
                    .get(country, "N/A")
                ),
                "average_salary": avg_salary,
                "job_count": len(values)
            })

        country_breakdown.sort(
            key=lambda x: x["average_salary"],
            reverse=True
        )

        return {
            "salary_data_available": True,
            "top_paying_countries":
                country_breakdown[:5],
            "country_breakdown":
                country_breakdown
        }