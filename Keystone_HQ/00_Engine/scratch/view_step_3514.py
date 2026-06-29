import os

step_3514_path = r"C:\Users\Curtis\.gemini\antigravity\brain\f12c78d2-72b4-40e4-afee-7564ea10b735\.system_generated\steps\3514\output.txt"
if os.path.exists(step_3514_path):
    print("Step 3514 output.txt exists!")
    with open(step_3514_path, "r", encoding="utf-8") as f:
        content = f.read()
    print(f"Length of step 3514 output: {len(content)}")
    print("Snippet:")
    print(content[:1000])
else:
    print("Step 3514 output.txt does not exist.")
