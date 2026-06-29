import json

path = r"C:\Users\Curtis\.gemini\antigravity\brain\3cd8f571-5b38-4846-b151-e04865f46f19\.system_generated\steps\3750\output.txt"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split("\n")
for line in lines:
    if "3000" in line or "localhost" in line:
        print(line)
