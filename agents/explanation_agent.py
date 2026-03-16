from typing import List, Dict
import os
from groq import Groq
from core.config import GROQ_API_KEY, GROQ_MODEL

class ExplanationAgent:
    def __init__(self):
        self.api_key = GROQ_API_KEY
        self.client = None
        if self.api_key:
            self.client = Groq(api_key=self.api_key)

    def generate_explanations(self, ranked_records: List[Dict]) -> List[Dict]:
        """
        Generates a short explanation for each ranked degree using labour market evidence.
        Uses Groq LLM if available, otherwise falls back to template-based logic.
        """
        for record in ranked_records:
            if self.client:
                try:
                    record['reason'] = self._get_llm_explanation(record)
                except Exception as e:
                    print(f"⚠️ Groq error: {e}. Falling back to template.")
                    record['reason'] = self._get_template_explanation(record)
            else:
                record['reason'] = self._get_template_explanation(record)

        return ranked_records

    def _get_llm_explanation(self, record: Dict) -> str:
        """Calls Groq to generate a concise, data-grounded explanation."""
        prompt = self.get_llm_prompt(record)
        
        response = self.client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You are a career advisor. You must provide a single sentence based ONLY on the provided data. No speculation."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.1
        )
        
        explanation = response.choices[0].message.content.strip()
        # Ensure it's truly a single sentence and not too long
        if not explanation.endswith('.'):
            explanation += '.'
        return explanation

    def _get_template_explanation(self, record: Dict) -> str:
        """Fallback template-based explanation."""
        degree = record.get('degree')
        salary = record.get('median_salary_lpa')
        growth = record.get('demand_growth_percent')
        evidence = record.get('evidence')
        source = record.get('primary_source')
        domain = record.get('domain')
        
        return f"{degree} offers a median salary of ₹{salary} LPA, supported by {growth}% growth in the {domain} domain as noted by {source} ({evidence})."

    def get_llm_prompt(self, record: Dict) -> str:
        """
        Helper to visualize what the prompt to the LLM would look like.
        """
        return f"""
        Review the following labour market data for the degree: {record.get('degree')}
        - Median Salary: ₹{record.get('median_salary_lpa')} LPA
        - Demand Growth: {record.get('demand_growth_percent')}%
        - Hiring Volume Score: {record.get('hiring_volume_score')}/10
        - Evidence: {record.get('evidence')}
        - Source: {record.get('primary_source')}
        
        Task: Write a single, professional sentence explaining why this degree is a strong career choice. 
        MANDATORY: Mention the source ({record.get('primary_source')}) and the key growth/salary figures.
        Focus on the data provided. Do not use outside knowledge. Do not start with "Based on the data".
        """
