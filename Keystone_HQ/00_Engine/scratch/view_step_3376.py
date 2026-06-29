import json
import os

step_dir = r"C:\Users\Curtis\.gemini\antigravity\brain\f12c78d2-72b4-40e4-afee-7564ea10b735\.system_generated\steps"
# Let's list some steps to see what we have
steps = sorted([int(s) for s in os.listdir(step_dir) if s.isdigit()])
print(f"Total step directories: {len(steps)}")
print(f"Last 10 steps: {steps[-10:]}")

# Check step 3376 specifically
step_3376_path = os.path.join(step_dir, "3376", "output.txt")
if os.path.exists(step_3376_path):
    print("\nStep 3376 output.txt exists!")
    with open(step_3376_path, "r", encoding="utf-8") as f:
        content = f.read()
    print(f"Length of step 3376 output: {len(content)}")
    print("Snippet:")
    print(content[:500])
else:
    print("\nStep 3376 output.txt does not exist.")
