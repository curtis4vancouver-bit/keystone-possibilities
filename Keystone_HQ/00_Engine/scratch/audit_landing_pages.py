import os
import glob
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

print(f"Auditing {len(all_files)} files...")

for fpath in all_files:
    content = open(fpath, 'r', encoding='utf-8', errors='ignore').read()
    print(f"\nFile: {os.path.basename(fpath)}")
    
    # 1. Staging URLs
    staging_urls = re.findall(r'https?://[^\s"\']*wpcomstaging\.com[^\s"\']*', content)
    if staging_urls:
        print(f"  Staging URLs found: {len(staging_urls)} (e.g. {staging_urls[0]})")
    else:
        print("  Staging URLs: None")
        
    # 2. Phone Numbers
    phone_nums = re.findall(r'\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b', content)
    # Filter unique phone numbers
    unique_phones = list(set(phone_nums))
    print(f"  Phone numbers found: {unique_phones}")
    
    # 3. Addresses
    # Let's search for typical address patterns or keywords like "Road", "Squamish", "Watts"
    address_keywords = ["Watts", "Squamish", "Point Road", "V8B"]
    found_keywords = [kw for kw in address_keywords if kw.lower() in content.lower()]
    print(f"  Address keywords present: {found_keywords}")
