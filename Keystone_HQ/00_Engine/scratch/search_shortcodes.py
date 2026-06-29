with open("scratch/remote_functions.php", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "add_shortcode" in line or "keystone_video" in line:
        print(f"Line {idx+1}: {line.strip()}")
