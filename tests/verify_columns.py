import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.orchestrator import CareerAdvisorOrchestrator

def verify_data_columns():
    orchestrator = CareerAdvisorOrchestrator()
    df = orchestrator.run_pipeline("Science")
    print(f"Columns: {list(df.columns)}")
    print(df.head(1).to_dict('records'))
    
    if "Domain" in df.columns:
        print("✅ SUCCESS: 'Domain' column exists.")
    else:
        print("❌ ERROR: 'Domain' column missing!")

if __name__ == "__main__":
    verify_data_columns()
