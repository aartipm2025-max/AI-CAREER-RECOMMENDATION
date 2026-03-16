import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.data_loader import load_degrees
from agents.input_agent import InputAgent, ValidationError
from agents.degree_agent import DegreeAgent

def test_phase_2():
    print("🚀 Starting Phase 2 Test: Degree Retrieval")
    try:
        # Load data
        degrees_df = load_degrees()
        
        # Initialize agents
        input_agent = InputAgent()
        degree_agent = DegreeAgent(degrees_df)
        
        # Test 1: Valid Science input (casing check)
        print("  Testing: 'science' input...")
        normalised_science = input_agent.validate_stream("science")
        science_degrees = degree_agent.get_degrees_by_stream(normalised_science)
        assert normalised_science == "Science"
        assert len(science_degrees) > 0
        assert all(d['stream'] == 'Science' for d in science_degrees)
        print(f"  ✅ SUCCESS: Retrieved {len(science_degrees)} Science degrees.")

        # Test 2: Valid Commerce input
        print("  Testing: 'Commerce' input...")
        normalised_commerce = input_agent.validate_stream("Commerce")
        commerce_degrees = degree_agent.get_degrees_by_stream(normalised_commerce)
        assert len(commerce_degrees) > 0
        print(f"  ✅ SUCCESS: Retrieved {len(commerce_degrees)} Commerce degrees.")

        # Test 3: Invalid input
        print("  Testing: Invalid 'Engineering' input...")
        try:
            input_agent.validate_stream("Engineering")
            print("  ❌ ERROR: Should have raised ValidationError for 'Engineering'.")
            sys.exit(1)
        except ValidationError as e:
            print(f"  ✅ SUCCESS: Caught expected error: {e}")

    except Exception as e:
        print(f"❌ ERROR: Phase 2 verification failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_phase_2()
