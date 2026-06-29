import json
import re
import os
import subprocess
import sys

PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
STEP_OUTPUT_PATH = r"C:\Users\Curtis\.gemini\antigravity\brain\dcfb044f-d157-4191-8dd4-486712240c1d\.system_generated\steps\3381\output.txt"

def main():
    if not os.path.exists(STEP_OUTPUT_PATH):
        print(f"Error: Step output not found at {STEP_OUTPUT_PATH}")
        sys.exit(1)
        
    with open(STEP_OUTPUT_PATH, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
        
    # Extract the JSON block inside the code fences
    # The output is formatted like:
    # Script ran on page and returned:
    # ```json
    # "Actual report text..."
    # ```
    match = re.search(r"```json\s+(.*)\s+```", content, re.DOTALL)
    if not match:
        print("Error: Could not locate JSON block in step output")
        sys.exit(1)
        
    json_str = match.group(1).strip()
    try:
        report_text = json.loads(json_str)
    except Exception as e:
        print(f"Error decoding JSON: {e}")
        sys.exit(1)
        
    # Save the report text to a temporary clean file
    temp_file = os.path.join(PROJECT_ROOT, "scratch", "temp_report.txt")
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(report_text)
        
    print(f"Wrote clean report of {len(report_text)} characters to {temp_file}")
    
    # Run the process script
    domain = "AGENT_ARCH"
    topic = "Google Antigravity Agent SDK 2026: What are the most advanced patterns for building self-improving AI agents that can autonomously identify their own weaknesses, generate improvement plans, and implement fixes without human intervention? Cover self-reflection loops, automated skill creation, context window optimization, and memory consolidation. Include specific code patterns, configuration examples, and real-world case studies of agents that successfully self-evolved. Focus on the Gemini ecosystem and MCP (Model Context Protocol) tool orchestration."
    
    process_script = os.path.join(PROJECT_ROOT, "scratch", "process_completed_topic.py")
    result = subprocess.run(
        [sys.executable, process_script, domain, topic, temp_file],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )
    
    print("STDOUT:")
    print(result.stdout)
    print("STDERR:")
    print(result.stderr)
    
    if result.returncode == 0:
        print("Successfully processed Topic 1!")
    else:
        sys.exit(result.returncode)

if __name__ == "__main__":
    main()
