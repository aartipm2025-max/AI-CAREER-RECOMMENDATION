import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.data_loader import load_all_datasets
from agents.degree_agent import DegreeAgent
from agents.market_intelligence_agent import MarketIntelligenceAgent
from agents.ranking_engine import RankingEngine
from agents.explanation_agent import ExplanationAgent
from agents.response_agent import ResponseAgent

def test_phase_6():
    print("🚀 Starting Phase 6 Test: Response Formatting")
    try:
        datasets = load_all_datasets()
        
        # Step 1: Process through explanations
        degree_agent = DegreeAgent(datasets['degrees'])
        market_agent = MarketIntelligenceAgent(datasets['salary'], datasets['demand'])
        engine = RankingEngine()
        explainer = ExplanationAgent()
        
        science_degrees = degree_agent.get_degrees_by_stream("Science")
        enriched = market_agent.enrich_degree_data(science_degrees)
        ranked = engine.rank_degrees(enriched)
        explained = explainer.generate_explanations(ranked)
        
        # Step 2: Format Response
        responder = ResponseAgent()
        df = responder.format_output(explained)
        
        print("  Formatted Table Preview:")
        print(df.head(2).to_string(index=False))

        # Assertions
        assert len(df) == len(explained)
        assert list(df.columns) == ["Rank", "Degree", "Median Salary", "Reason", "Source"]
        assert df.iloc[0]["Rank"] == 1
        assert df.iloc[-1]["Rank"] == len(df)

        print("✅ SUCCESS: Final table formatting verified.")

    except Exception as e:
        print(f"❌ ERROR: Phase 6 verification failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_phase_6()
