from typing import List, Dict
from core.normaliser import min_max_normalise
from core.config import WEIGHT_SALARY, WEIGHT_DEMAND_GROWTH, WEIGHT_HIRING_VOLUME

class RankingEngine:
    def __init__(self):
        self.w_salary = WEIGHT_SALARY
        self.w_growth = WEIGHT_DEMAND_GROWTH
        self.w_hiring = WEIGHT_HIRING_VOLUME

    def rank_degrees(self, enriched_records: List[Dict]) -> List[Dict]:
        """
        Calculates Market Value Score and sorts degrees.
        Score = (0.5 * NormSalary) + (0.3 * NormGrowth) + (0.2 * NormHiring)
        """
        if not enriched_records:
            return []

        # 1. Extract values for normalisation
        salaries = [r.get('median_salary_lpa', 0.0) for r in enriched_records]
        growths = [r.get('demand_growth_percent', 0.0) for r in enriched_records]
        volumes = [r.get('hiring_volume_score', 0.0) for r in enriched_records]

        # 2. Normalise
        norm_salaries = min_max_normalise(salaries)
        norm_growths = min_max_normalise(growths)
        norm_volumes = min_max_normalise(volumes)

        # 3. Calculate scores
        for i, record in enumerate(enriched_records):
            score = (
                (norm_salaries[i] * self.w_salary) +
                (norm_growths[i] * self.w_growth) +
                (norm_volumes[i] * self.w_hiring)
            )
            record['market_value_score'] = round(score, 2)

        # 4. Sort by Score descending, then by Salary (tie-breaker)
        ranked_list = sorted(
            enriched_records,
            key=lambda x: (x['market_value_score'], x['median_salary_lpa']),
            reverse=True
        )

        return ranked_list
