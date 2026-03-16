import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.data_loader import load_all_datasets
from agents.degree_agent import DegreeAgent
from agents.market_intelligence_agent import MarketIntelligenceAgent

def test_phase_3():
    print("🚀 Starting Phase 3 Test: Market Data Integration")
    try:
        datasets = load_all_datasets()
        
        # Step 1: Get Science degrees
        degree_agent = DegreeAgent(datasets['degrees'])
        science_degrees = degree_agent.get_degrees_by_stream("Science")
        
        # Step 2: Enrich with market data
        market_agent = MarketIntelligenceAgent(datasets['salary'], datasets['demand'])
        enriched = market_agent.enrich_degree_data(science_degrees)
        
        # Verify enrichment
        for record in enriched:
            print(f"  Verifying {record['degree']}...")
            assert 'median_salary_lpa' in record
            assert 'demand_growth_percent' in record
            assert 'hiring_volume_score' in record
            assert 'evidence' in record
            print(f"    Salary: {record['median_salary_lpa']} LPA, Growth: {record['demand_growth_percent']}%")

        print("✅ SUCCESS: Market data integration verified for all records.")

    except Exception as e:
        print(f"❌ ERROR: Phase 3 verification failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_phase_3()
