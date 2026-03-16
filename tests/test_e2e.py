import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.orchestrator import CareerAdvisorOrchestrator

def test_full_application():
    print("🚀 Starting Final End-to-End Test")
    try:
        orchestrator = CareerAdvisorOrchestrator()
        
        streams = ["Science", "Commerce", "Arts"]
        
        for stream in streams:
            print(f"\n--- Testing Stream: {stream} ---")
            results = orchestrator.run_pipeline(stream)
            
            # Basic sanity checks
            assert not results.empty
            assert len(results) == 10
            expected_cols = ["Rank", "Degree", "Median Salary", "Demand Growth", "Domain", "Reason", "Source", "Job Roles", "Skills", "Career Path"]
            assert list(results.columns) == expected_cols
            assert results.iloc[0]["Rank"] == 1
            
            # Print top result
            top_degree = results.iloc[0]["Degree"]
            top_salary = results.iloc[0]["Median Salary"]
            print(f"✅ Success: Top recommendation for {stream} is {top_degree} ({top_salary})")

        print("\n✨ ALL END-TO-END TESTS PASSED!")

    except Exception as e:
        print(f"❌ ERROR: End-to-End test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_full_application()
