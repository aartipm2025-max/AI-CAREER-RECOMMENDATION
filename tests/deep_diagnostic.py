import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pipeline.orchestrator import CareerAdvisorOrchestrator
import traceback

def diagnostic():
    try:
        orchestrator = CareerAdvisorOrchestrator()
        for stream in ['Science', 'Commerce', 'Arts']:
            print(f"\n--- Testing Stream: {stream} ---")
            df = orchestrator.run_pipeline(stream)
            print(f"Columns found: {list(df.columns)}")
            if 'Domain' not in df.columns:
                print(f"❌ ERROR: 'Domain' column missing in {stream} results!")
            else:
                print(f"✅ 'Domain' column present.")
                # Check for any None values in Domain
                if df['Domain'].isnull().any():
                    print(f"⚠️ Warning: Found None values in 'Domain' for {stream}")
                
            # Simulate the UI access
            sample_row = df.iloc[0]
            try:
                # This is what app.py does
                from interface.app import DOMAIN_ICONS
                val = sample_row.get('Domain')
                icon = DOMAIN_ICONS.get(val, "🎓")
                print(f"Sample Domain: {val} -> Icon: {icon}")
            except Exception as e:
                print(f"❌ UI Access Simulation Failed: {e}")
                
    except Exception as e:
        print(f"❌ Orchestrator Failed: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    diagnostic()
