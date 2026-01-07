import asyncio
import os
import glob
from backend.pipeline import run_pipeline
from dotenv import load_dotenv

# Load env (not strictly needed for API keys anymore, but good for other config)
load_dotenv()

async def run_tests():
    reports_dir = os.path.join("backend", "sample_reports")
    report_files = glob.glob(os.path.join(reports_dir, "*.txt"))

    print(f"Found {len(report_files)} sample reports to test.\n")

    for file_path in report_files:
        filename = os.path.basename(file_path)
        print(f"--- Testing Report: {filename} ---")
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                report_text = f.read()
            
            # Call Pipeline
            print("Running Local AI Pipeline (this may take time on CPU)...")
            result = await run_pipeline(report_text)
            
            # Print Outputs
            print("\n> PATIENT VIEW:")
            print("-" * 20)
            print(result["patient_explanation"])
            
            print("\n> CLINICIAN VIEW:")
            print("-" * 20)
            print(result["clinician_explanation"])
            
            print("\n> CITATIONS FOUND:")
            print(result.get("citations", []))
            
            print("\n" + "="*50 + "\n")
            
        except Exception as e:
            print(f"ERROR processing {filename}: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_tests())
