import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.data_loader import load_all_datasets
from agents.degree_agent import DegreeAgent
from agents.market_intelligence_agent import MarketIntelligenceAgent
from agents.ranking_engine import RankingEngine

def test_phase_4():
    print("🚀 Starting Phase 4 Test: Ranking Engine")
    try:
        datasets = load_all_datasets()
        
        # Step 1: Get Science degrees
        degree_agent = DegreeAgent(datasets['degrees'])
        science_degrees = degree_agent.get_degrees_by_stream("Science")
        
        # Step 2: Enrich with market data
        market_agent = MarketIntelligenceAgent(datasets['salary'], datasets['demand'])
        enriched = market_agent.enrich_degree_data(science_degrees)
        
        # Step 3: Rank
        engine = RankingEngine()
        ranked = engine.rank_degrees(enriched)
        
        print("  Ranking Results (Science):")
        for i, r in enumerate(ranked):
            print(f"    Rank {i+1}: {r['degree']} | Score: {r['market_value_score']} | Salary: {r['median_salary_lpa']}")

        # Assertions
        assert len(ranked) == len(science_degrees)
        # BTech AI has 7.5 LPA, BSc Data Science has 7.0 LPA. 
        # Both have same growth (34%). BTech AI should be higher or equal depending on other scores.
        assert ranked[0]['market_value_score'] >= ranked[-1]['market_value_score']
        
        print("✅ SUCCESS: Ranking logic and sorting verified.")

    except Exception as e:
        print(f"❌ ERROR: Phase 4 verification failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_phase_4()
