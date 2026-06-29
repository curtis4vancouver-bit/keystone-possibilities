import json

file_path = r"C:\Users\Curtis\.gemini\antigravity\brain\21cff3a5-5ad8-4efd-832e-b882b33d65f4\.system_generated/logs/transcript.jsonl"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
# Print lines from line 11350 to the end
for idx in range(max(0, len(lines) - 80), len(lines)):
    try:
        data = json.loads(lines[idx])
        step = data.get("step_index")
        source = data.get("source")
        type_ = data.get("type")
        content = data.get("content")
        print(f"Index {idx} | Step {step} | Source: {source} | Type: {type_}")
        if content:
            print(f"  Content: {content[:300]}...")
    except Exception as e:
        print(f"Error parsing line {idx}: {e}")
