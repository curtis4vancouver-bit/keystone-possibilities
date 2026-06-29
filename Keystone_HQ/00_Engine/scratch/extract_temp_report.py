import json
import os
import re

def extract(step_index, filename, conversation_id):
    brain_dir = f"C:\\Users\\Curtis\\.gemini\\antigravity\\brain\\{conversation_id}"
    output_path = os.path.join(brain_dir, ".system_generated", "steps", str(step_index), "output.txt")
    target_dir = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Deep_Research_Results"
    target_path = os.path.join(target_dir, filename)

    if not os.path.exists(output_path):
        print(f"Error: file not found at {output_path}")
        return False

    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the JSON string between the ```json and ``` blocks
    match = re.search(r"```json\s*(.*?)\s*```", content, re.DOTALL)
    if not match:
        print("Error: JSON block not found in output file")
        return False

    json_str = match.group(1).strip()
    try:
        report_text = json.loads(json_str)
    except json.JSONDecodeError as e:
        try:
            report_text = json.loads('"' + json_str + '"')
        except Exception as ex:
            print(f"Error parsing JSON: {e}, backup failed: {ex}")
            return False

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    with open(target_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"Successfully extracted report from step {step_index} and saved to: {target_path}")
    return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python extract_temp_report.py <step_index> <filename> <conversation_id>")
    else:
        extract(int(sys.argv[1]), sys.argv[2], sys.argv[3])
