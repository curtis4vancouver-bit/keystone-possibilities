# Check block braces inside run_keystone_migration block
php_path = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\02_Websites\keystone-recomposition-child\functions.php"

with open(php_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

block_lines = lines[56:204] # lines 57 to 204 (0-indexed 56 to 203)
block_code = "".join(block_lines)

# Naive strip
import re
def strip_comments_and_strings(code):
    def replacer(match):
        return ' ' * len(match.group(0))
    code = re.sub(r'//.*', replacer, code)
    code = re.sub(r'/\*.*?\*/', replacer, code, flags=re.DOTALL)
    code = re.sub(r"'[^'\\]*(?:\\.[^'\\]*)*'", replacer, code)
    code = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', replacer, code)
    return code

clean_block = strip_comments_and_strings(block_code)

open_count = clean_block.count('{')
close_count = clean_block.count('}')

print(f"Migration block (lines 57-204) - Open braces: {open_count}, Close braces: {close_count}")

# Check lines one by one to see where braces open and close
depth = 0
for idx, line in enumerate(block_lines, 57):
    clean_line = strip_comments_and_strings(line)
    for char in clean_line:
        if char == '{':
            depth += 1
            print(f"Line {idx} opens brace (depth: {depth})")
        elif char == '}':
            depth -= 1
            print(f"Line {idx} closes brace (depth: {depth})")
