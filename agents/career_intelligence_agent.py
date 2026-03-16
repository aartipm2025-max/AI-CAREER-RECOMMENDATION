from typing import List, Dict
import pandas as pd

class CareerIntelligenceAgent:
    def __init__(self, skills_df: pd.DataFrame, paths_df: pd.DataFrame):
        self.skills_df = skills_df
        self.paths_df = paths_df

    def enrich_with_intelligence(self, ranked_records: List[Dict]) -> List[Dict]:
        """
        Attaches career skills and long-term paths to ranked degree results.
        
        Input: Ranked degree records.
        Output: Enriched records with job_roles, skills, and career_path stages.
        """
        enriched_results = []
        
        for record in ranked_records:
            degree = record.get("degree")
            
            # Retrieve skills and roles
            skills_row = self.skills_df[self.skills_df['degree'] == degree]
            job_roles = []
            skills = []
            if not skills_row.empty:
                job_roles = [role.strip() for role in skills_row.iloc[0]['top_job_roles'].split(',')]
                skills = [skill.strip() for skill in skills_row.iloc[0]['top_skills'].split(',')]
            
            # Retrieve career path
            path_row = self.paths_df[self.paths_df['degree'] == degree]
            career_path = []
            if not path_row.empty:
                # Store as list for easy consumption by UI
                career_path = [stage.strip() for stage in path_row.iloc[0]['career_path'].split('->')]
            
            # Enrich record
            enriched_record = record.copy()
            enriched_record.update({
                "job_roles": job_roles,
                "skills": skills,
                "career_path": career_path
            })
            enriched_results.append(enriched_record)
            
        return enriched_results
