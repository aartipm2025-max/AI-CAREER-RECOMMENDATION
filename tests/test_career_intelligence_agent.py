import sys
import os
import pandas as pd

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.career_intelligence_agent import CareerIntelligenceAgent

def test_career_intelligence():
    # Setup mock data
    skills_df = pd.DataFrame({
        'degree': ['BSc Data Science'],
        'top_job_roles': ['Data Analyst, ML Engineer'],
        'top_skills': ['Python, SQL']
    })
    paths_df = pd.DataFrame({
        'degree': ['BSc Data Science'],
        'career_path': ['Analyst -> Lead -> Director']
    })
    
    agent = CareerIntelligenceAgent(skills_df, paths_df)
    
    records = [{'degree': 'BSc Data Science', 'rank': 1}]
    enriched = agent.enrich_with_intelligence(records)
    
    assert len(enriched) == 1
    assert enriched[0]['job_roles'] == ['Data Analyst', 'ML Engineer']
    assert enriched[0]['skills'] == ['Python', 'SQL']
    assert enriched[0]['career_path'] == ['Analyst', 'Lead', 'Director']
    print("✅ Career Intelligence Agent Test Passed")

if __name__ == "__main__":
    test_career_intelligence()
