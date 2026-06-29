with open("scratch/remote_functions.php", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open("scratch/sitemap_filter.txt", "w", encoding="utf-8") as out:
    # Print lines 820 to 920 (0-indexed 819 to 919)
    for i in range(819, min(920, len(lines))):
        out.write(f"{i+1}: {lines[i]}")

print("Saved output directly to scratch/sitemap_filter.txt")
