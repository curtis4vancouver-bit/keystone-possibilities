import os
import json

brain_dir = r"C:\Users\Curtis\.gemini\antigravity\brain"

def main():
    matching_brains = ["62914a3a-e181-4674-8d37-9b9f49e67cf2", "21cff3a5-5ad8-4efd-832e-b882b33d65f4", "06ca4b70-926e-4492-be53-382883740599"]
    for brain in matching_brains:
        t_path = os.path.join(brain_dir, brain, ".system_generated", "logs", "transcript.jsonl")
        if not os.path.exists(t_path):
            continue
        print(f"\nScanning brain {brain}...")
        found = 0
        with open(t_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                if "page24_output.json" in line or "process_sweep" in line or "deep_research_state" in line:
                    data = json.loads(line)
                    print(f"  Step {data.get('step_index')}: {line[:300]}")
                    found += 1
                    if found >= 10:
                        break

if __name__ == "__main__":
    main()
