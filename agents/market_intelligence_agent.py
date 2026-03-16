import pandas as pd
from typing import List, Dict
import logging

class MarketIntelligenceAgent:
    def __init__(self, salary_df: pd.DataFrame, demand_df: pd.DataFrame):
        self.salary_df = salary_df
        self.demand_df = demand_df

    def enrich_degree_data(self, degree_records: List[Dict]) -> List[Dict]:
        """
        Attaches salary and demand statistics to each degree record.
        Joins salary on 'degree' and demand on 'domain'.
        """
        enriched_records = []

        for record in degree_records:
            degree_name = record['degree']
            domain_name = record['domain']

            # Find salary match
            salary_match = self.salary_df[self.salary_df['degree'] == degree_name]
            if not salary_match.empty:
                record.update({
                    'median_salary_lpa': float(salary_match.iloc[0]['median_salary_lpa']),
                    'salary_range_lpa': salary_match.iloc[0]['salary_range_lpa'],
                    'salary_source': salary_match.iloc[0]['source']
                })
            else:
                # Defaults if not found
                record.update({
                    'median_salary_lpa': 0.0,
                    'salary_range_lpa': "N/A",
                    'salary_source': "Unknown"
                })

            # Find demand match
            demand_match = self.demand_df[self.demand_df['domain'] == domain_name]
            if not demand_match.empty:
                match = demand_match.iloc[0]
                record.update({
                    'demand_growth_percent': float(match['demand_growth_percent']),
                    'hiring_volume_score': float(match['hiring_volume_score']),
                    'evidence': match['evidence'],
                    'primary_source': match['primary_source']
                })
            else:
                # Defaults if not found
                record.update({
                    'demand_growth_percent': 0.0,
                    'hiring_volume_score': 0.0,
                    'evidence': "No specific demand data available for this domain.",
                    'primary_source': "Internal Database"
                })

            enriched_records.append(record)

        return enriched_records
