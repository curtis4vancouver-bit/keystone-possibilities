import os

log_path = r"C:\Users\Curtis\.gemini\antigravity\brain\55ece092-8436-4c83-924a-2121703c17bd\.system_generated\logs\transcript.jsonl"
with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    for i, line in enumerate(f):
        if "evaluate_script" in line:
            print(f"Line {i} matches:")
            print(line[:800])
            print("=" * 60)
