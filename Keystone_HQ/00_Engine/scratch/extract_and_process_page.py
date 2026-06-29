import json
import re
import os
import subprocess
import sys

PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"

def main():
    if len(sys.argv) < 5:
        print("Usage: python extract_and_process_page.py <step_output_path> <page_id> <domain> <topic_name>")
        sys.exit(1)
        
    step_output_path = sys.argv[1]
    page_id = sys.argv[2]
    domain = sys.argv[3]
    topic = sys.argv[4]
    
    if not os.path.exists(step_output_path):
        print(f"Error: Step output file not found at {step_output_path}")
        sys.exit(1)
        
    with open(step_output_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
        
    # Extract the JSON block inside the code fences
    match = re.search(r"```json\s+(.*)\s+```", content, re.DOTALL)
    if not match:
        print("Error: Could not locate JSON block in step output")
        sys.exit(1)
        
    json_str = match.group(1).strip()
    try:
        report_text = json.loads(json_str)
    except Exception as e:
        # Fallback if it's not a JSON string, try to decode it directly
        print(f"Warning: JSON load failed ({e}), using raw string")
        report_text = json_str
        
    # Save the report text to a temporary clean file
    temp_file = os.path.join(PROJECT_ROOT, "scratch", f"temp_report_{page_id}.txt")
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(report_text)
        
    print(f"Wrote clean report of {len(report_text)} characters to {temp_file}")
    
    # Run the process script
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
        print(f"Successfully processed Page {page_id}!")
    else:
        sys.exit(result.returncode)

if __name__ == "__main__":
    main()
