import os
import re

websites_dir = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\02_Websites"
seo_dir = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\02_Keystone_Possibilities\Local_SEO_Domination"

files1 = [
    "fiduciary-pm-luxury-homes.html",
    "north-vancouver-multiplex-conversions.html",
    "pemberton-luxury-builder.html",
    "squamish-custom-home-builder.html",
    "west-vancouver-luxury-renovations.html",
    "whistler-luxury-builder.html"
]

files2 = [
    "north_vancouver_custom_homes.html",
    "squamish_custom_homes.html",
    "sunshine_coast_custom_homes.html",
    "west_vancouver_custom_homes.html",
    "whistler_custom_homes.html"
]

all_files = []
for fn in files1:
    fpath = os.path.join(websites_dir, fn)
    if os.path.exists(fpath):
        all_files.append(fpath)
for fn in files2:
    fpath = os.path.join(seo_dir, fn)
    if os.path.exists(fpath):
        all_files.append(fpath)

for fpath in all_files:
    content = open(fpath, 'r', encoding='utf-8', errors='ignore').read()
    print(f"\nFile: {os.path.basename(fpath)}")
    # Find all occurrences of addresses
    # Let's search for patterns like "1 Watts", "Squamish, BC", or zip code "V8B" or "V7"
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if any(w in line for w in ["Watts", "V8B", "V7", "V0N", "V0P", "Address", "address"]):
            print(f"  Line {i+1}: {line.strip()}")
