import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Make `scripts/` importable so we can import `scripts/graph.py` as `graph`.
SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from graph import compiled_workflow

load_dotenv()

def run_pipeline(user_query: str):
    # Initialize the input
    inputs = {
        "query": user_query,
        "context": "",
        "structured_data": {},
        "metrics": {}
    }
    
    print(f"🔍 Searching for: {user_query}")
    
    # Run the graph and stream the updates
    #.stream() allows us to get intermediate outputs as each node completes, which is great for debugging and understanding the flow.
    # can use .invoke() instead to run the whole graphas final output without streaming intermediate results.
    for output in compiled_workflow.stream(inputs):
        for key, value in output.items():
            print(f"\n✅ Node '{key}' completed.")
            if key == "extract":
                structured = value.get("structured_data", {})
                summary = structured.get("summary")
                if summary:
                    print(f"Extracted summary: {summary}")
                else:
                    print(f"Extracted structured_data: {structured}")

            if key == "grade":
                metrics = value.get("metrics", {})
                accuracy = metrics.get("accuracy")
                faithfulness = metrics.get("faithfulness")
                if accuracy is not None and faithfulness is not None:
                    print(f"Scores: accuracy={accuracy} faithfulness={faithfulness}")
                else:
                    print(f"Metrics: {metrics}")

if __name__ == "__main__":
    # Test Use Case A: Search by drug and condition
    query = "Find a patient on Prednisone for Bronchitis"
    run_pipeline(query)