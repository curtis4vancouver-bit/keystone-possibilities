import re

output_php_path = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scratch\remote_functions.php"

with open(output_php_path, "r", encoding="utf-8") as f:
    code = f.read()

print(f"Loaded remote functions.php (length: {len(code)})")

# Build mapping of index to line number
line_map = []
curr_line = 1
for char in code:
    line_map.append(curr_line)
    if char == '\n':
        curr_line += 1

def strip_comments_and_strings_keep_len(c):
    def replacer(match):
        text = match.group(0)
        return ''.join('\n' if char == '\n' else ' ' for char in text)

    c = re.sub(r'//.*', replacer, c)
    c = re.sub(r'/\*.*?\*/', replacer, c, flags=re.DOTALL)
    c = re.sub(r"'[^'\\]*(?:\\.[^'\\]*)*'", replacer, c)
    c = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', replacer, c)
    return c

clean_code = strip_comments_and_strings_keep_len(code)

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
        end_char_idx = min(len(code), b[2] + 150)
        snippet = code[start_char_idx:end_char_idx].replace('\n', ' [NL] ')
        print(f"Brace opened on line {b[1]}: ... {snippet} ...")
        errors.append(f"Unclosed opening brace '{{' opened on line {b[1]}")

print("\n--- REMOTE BRACE AUDIT ---")
if not errors:
    print("SUCCESS: Remote braces are perfectly balanced!")
else:
    print(f"FAILED: Found {len(errors)} error(s) in remote code:")
    for err in errors:
        print("  ", err)

# Check for duplicate function declarations
funcs = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', clean_code)
duplicates = set([f for f in funcs if funcs.count(f) > 1])
print("\n--- REMOTE DUPLICATE FUNCTIONS AUDIT ---")
if not duplicates:
    print("SUCCESS: No duplicate function declarations found in remote code!")
else:
    print(f"FAILED: Found duplicate functions in remote code: {list(duplicates)}")
