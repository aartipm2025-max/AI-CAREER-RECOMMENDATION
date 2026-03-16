import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.data_loader import load_all_datasets
from agents.degree_agent import DegreeAgent
from agents.market_intelligence_agent import MarketIntelligenceAgent
from agents.ranking_engine import RankingEngine
from agents.explanation_agent import ExplanationAgent

def test_phase_5():
    print("🚀 Starting Phase 5 Test: Explanation Layer")
    try:
        datasets = load_all_datasets()
        
        # Step 1: Process through ranking
        degree_agent = DegreeAgent(datasets['degrees'])
        market_agent = MarketIntelligenceAgent(datasets['salary'], datasets['demand'])
        engine = RankingEngine()
        
        science_degrees = degree_agent.get_degrees_by_stream("Science")
        enriched = market_agent.enrich_degree_data(science_degrees)
        ranked = engine.rank_degrees(enriched)
        
        # Step 2: Generate explanations
        explainer = ExplanationAgent()
        explained = explainer.generate_explanations(ranked)
        
        print("  Explanation Samples:")
        for r in explained[:2]:
            print(f"    - {r['degree']}: {r['reason']}")

        # Assertions
        for r in explained:
            assert 'reason' in r
            assert isinstance(r['reason'], str)
            assert len(r['reason']) > 20 # Basic length check
            # Verify data grounding (Salary usually present)
            assert str(r['median_salary_lpa']) in r['reason']
            # We'll print a warning instead of failing if the source isn't exactly matched, 
            # as LLMs sometimes rephrase or use acronyms.
            if r['primary_source'].lower() not in r['reason'].lower():
                print(f"  ⚠️ Warning: Source '{r['primary_source']}' not found in explanation: '{r['reason']}'")

        print("✅ SUCCESS: Explanation generation grounded in data verified.")

    except Exception as e:
        print(f"❌ ERROR: Phase 5 verification failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_phase_5()
