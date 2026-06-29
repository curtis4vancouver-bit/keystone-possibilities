import os

snapshot_path = r"C:\Users\Curtis\.gemini\antigravity\brain\55ece092-8436-4c83-924a-2121703c17bd\.system_generated\steps\1060\output.txt"

with open(snapshot_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
print("Filtering for buttons, links, or keywords:")
keywords = ["research", "start", "thinking", "done", "generating", "button", "link", "input", "progress"]

for line in lines:
    line_lower = line.lower()
    if any(kw in line_lower for kw in keywords):
        print(line.rstrip())
