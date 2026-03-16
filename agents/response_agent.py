from typing import List, Dict
import pandas as pd

class ResponseAgent:
    def format_output(self, explained_records: List[Dict]) -> pd.DataFrame:
        """
        Formats the final list into a structured table.
        Columns: Rank, Degree, Median Salary, Reason, Source
        """
        output_data = []
        for i, record in enumerate(explained_records):
            output_data.append({
                "Rank": i + 1,
                "Degree": record.get("degree", "Unknown Degree"),
                "Median Salary": f"₹{record.get('median_salary_lpa', 'N/A')} LPA",
                "Demand Growth": f"{record.get('demand_growth_percent', 'N/A')}%",
                "Domain": record.get("domain", "General"),
                "Reason": record.get("reason", "No reason provided."),
                "Source": record.get("primary_source", "Unknown Source"),
                "Job Roles": record.get("job_roles", []),
                "Skills": record.get("skills", []),
                "Career Path": record.get("career_path", [])
            })
        
        return pd.DataFrame(output_data)

    def to_markdown(self, df: pd.DataFrame) -> str:
        """
        Converts the dataframe to a clean markdown table.
        """
        return df.to_markdown(index=False)
