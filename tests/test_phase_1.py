import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.data_loader import load_all_datasets

def test_phase_1():
    print("🚀 Starting Phase 1 Test: Data Layer")
    try:
        data = load_all_datasets()
        print("✅ SUCCESS: All datasets loaded and validated.")
        
        for name, df in data.items():
            print(f"- {name}: {len(df)} rows")
            print(f"  Columns: {', '.join(df.columns)}")
            
    except Exception as e:
        print(f"❌ ERROR: Phase 1 verification failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_phase_1()
