import re
import os
import glob

theme_dir = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\02_Websites\keystone-recomposition-child"

# Naive strip
def strip_comments_and_strings_keep_len(code):
    def replacer(match):
        text = match.group(0)
        return ''.join('\n' if c == '\n' else ' ' for c in text)
    code = re.sub(r'//.*', replacer, code)
    code = re.sub(r'/\*.*?\*/', replacer, code, flags=re.DOTALL)
    code = re.sub(r"'[^'\\]*(?:\\.[^'\\]*)*'", replacer, code)
    code = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', replacer, code)
    return code

php_files = glob.glob(os.path.join(theme_dir, "**/*.php"), recursive=True)

print(f"Scanning {len(php_files)} PHP files in theme directory...")

for php_path in php_files:
    rel_path = os.path.relpath(php_path, theme_dir)
    print(f"\n--- SCANNING {rel_path} ---")
    
    with open(php_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    line_map = []
    curr_line = 1
    for char in content:
        line_map.append(curr_line)
        if char == '\n':
            curr_line += 1
            
    clean_code = strip_comments_and_strings_keep_len(content)
    
    braces = []
    errors = []
    
    for idx, char in enumerate(clean_code):
        if char == '{':
            braces.append(('{', line_map[idx]))
        elif char == '}':
            if not braces:
                errors.append(f"Unmatched closing brace '}}' on line {line_map[idx]}")
            else:
                braces.pop()
                
    if braces:
        for b in braces:
            errors.append(f"Unclosed opening brace '{{' opened on line {b[1]}")
            
    if not errors:
        print("  SUCCESS: Braces are perfectly balanced!")
    else:
        print(f"  FAILED: Found {len(errors)} error(s):")
        for err in errors[:5]:
            print("    ", err)
            
    # Check for duplicate function declarations in this file
    funcs = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', clean_code)
    duplicates = set([f for f in funcs if funcs.count(f) > 1])
    if duplicates:
        print(f"  FAILED: Found duplicate functions: {list(duplicates)}")
