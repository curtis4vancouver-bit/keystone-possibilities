with open("scratch/check_php_syntax.py", "r") as f:
    text = f.read()

# Let's add debugging output to see the code context of unclosed braces
debug_code = """
import re

php_path = r"C:\\Users\\Curtis\\New folder\\construction-website\\Keystone_HQ\\02_Websites\\keystone-recomposition-child\\functions.php"

with open(php_path, "r", encoding="utf-8") as f:
    content = f.read()

# Build mapping of index to line number
line_map = []
curr_line = 1
for char in content:
    line_map.append(curr_line)
    if char == '\\n':
        curr_line += 1

def strip_comments_and_strings_keep_len(code):
    def replacer(match):
        # replace everything except newlines with spaces so lines align
        text = match.group(0)
        return ''.join('\\n' if c == '\\n' else ' ' for c in text)

    # Strip single line comments
    code = re.sub(r'//.*', replacer, code)
    # Strip multi line comments
    code = re.sub(r'/\\*.*?\\*/', replacer, code, flags=re.DOTALL)
    # Strip single quoted strings
    code = re.sub(r"'[^'\\\\]*(?:\\\\.[^'\\\\]*)*'", replacer, code)
    # Strip double quoted strings
    code = re.sub(r'"[^"\\\\]*(?:\\\\.[^"\\\\]*)*"', replacer, code)
    return code

clean_code = strip_comments_and_strings_keep_len(content)

braces = []
errors = []

for idx, char in enumerate(clean_code):
    if char == '{':
        braces.append(('{', line_map[idx], idx))
    elif char == '}':
        if not braces:
            errors.append(f"Unmatched closing brace '}}' on line {line_map[idx]}")
        else:
            braces.pop()

if braces:
    for b in braces:
        # Print snippet of original code around the opening brace
        start_char_idx = max(0, b[2] - 50)
        end_char_idx = min(len(content), b[2] + 150)
        snippet = content[start_char_idx:end_char_idx].replace('\\n', ' [NL] ')
        print(f"DEBUG: Brace opened on line {b[1]}: ... {snippet} ...")
        errors.append(f"Unclosed opening brace '{{' opened on line {b[1]}")

print("--- BRACE AUDIT ---")
if not errors:
    print("SUCCESS: Braces are perfectly balanced!")
else:
    print(f"FAILED: Found {len(errors)} error(s):")
    for err in errors:
        print("  ", err)
"""

with open("scratch/check_php_syntax.py", "w") as f:
    f.write(debug_code)
