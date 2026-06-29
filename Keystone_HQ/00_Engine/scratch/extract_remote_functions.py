import json
import sys
import re

json_path = r"C:\Users\Curtis\.gemini\antigravity\brain\c47c6452-cc70-4117-9f16-571f8aabc598\.system_generated\steps\1629\output.txt"
output_php_path = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scratch\remote_functions.php"

# Load the file content
with open(json_path, "r", encoding="utf-8") as f:
    text = f.read()

# Extract the JSON string between ```json and ```
match = re.search(r"```json\n(.*)\n```", text, re.DOTALL)
if match:
    json_str = match.group(1)
else:
    # Try finding the first double quote and the last double quote
    start_q = text.find('"')
    end_q = text.rfind('"')
    if start_q != -1 and end_q != -1:
        json_str = text[start_q:end_q+1]
    else:
        json_str = text

try:
    code = json.loads(json_str)
except Exception as e:
    print(f"Direct JSON load failed: {e}")
    # Fallback to evaluating it
    # Escape control characters like literal newlines or backslashes if needed, or try standard eval-like parsing
    # Let's replace any literal newlines inside the JSON string with \\n if they exist
    # (Since it's in a file, it should be valid JSON)
    try:
        # Try raw unicode_escape
        code = bytes(json_str, "utf-8").decode("unicode_escape")
    except Exception as e2:
        print(f"Unicode escape failed: {e2}")
        code = json_str

# Clean up code string
# If it starts and ends with double quotes, strip them
if code.startswith('"') and code.endswith('"'):
    code = code[1:-1]
    
# Replace escaped characters
code = code.replace('\\"', '"').replace('\\n', '\n').replace('\\t', '\t').replace('\\\\', '\\')

with open(output_php_path, "w", encoding="utf-8") as f:
    f.write(code)

print(f"Successfully extracted full remote functions.php to {output_php_path} (length: {len(code)})")
