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

print(f"Fixing {len(all_files)} files...")

for fpath in all_files:
    content = open(fpath, 'r', encoding='utf-8', errors='ignore').read()
    
    # 1. Replace staging domain
    content = content.replace("staging-a826-keystonepossibilities.wpcomstaging.com", "keystonepossibilities.ca")
    
    # 2. Replace phone numbers
    content = re.sub(r'604[-.\s]??555[-.\s]??0199', '604-848-9688', content)
    
    # 3. Replace schema address fields in JSON-LD
    # Let's target the "address" block:
    # "address": {
    #   "@type": "PostalAddress",
    #   ...
    # }
    # We will use regex to find this block and replace its values to:
    # "streetAddress": "1 Watts Point Road",
    # "addressLocality": "Squamish",
    # "addressRegion": "BC",
    # "postalCode": "V8B 0B1",
    # "addressCountry": "CA"
    
    def address_replacer(match):
        block = match.group(0)
        # Replace streetAddress
        block = re.sub(r'"streetAddress"\s*:\s*"[^"]*"', '"streetAddress": "1 Watts Point Road"', block)
        # Replace addressLocality
        block = re.sub(r'"addressLocality"\s*:\s*"[^"]*"', '"addressLocality": "Squamish"', block)
        # Replace addressRegion
        block = re.sub(r'"addressRegion"\s*:\s*"[^"]*"', '"addressRegion": "BC"', block)
        # Replace postalCode
        block = re.sub(r'"postalCode"\s*:\s*"[^"]*"', '"postalCode": "V8B 0B1"', block)
        return block

    content = re.sub(r'"address"\s*:\s*\{\s*"@type"\s*:\s*"PostalAddress"[^}]*\}', address_replacer, content, flags=re.DOTALL)
    
    # Also replace raw address mentions if any (e.g. street names) in text, while keeping context
    content = content.replace("Sea to Sky Highway, Squamish, BC V8B 0A1", "1 Watts Point Road, Squamish, BC V8B 0B1")
    content = content.replace("Sea to Sky Highway, Squamish, BC, V8B 0A1", "1 Watts Point Road, Squamish, BC V8B 0B1")
    content = content.replace("Lonsdale Ave, North Vancouver, BC V7M 2G2", "1 Watts Point Road, Squamish, BC V8B 0B1")
    content = content.replace("Pemberton Meadows Road, Pemberton, BC V0N 2L0", "1 Watts Point Road, Squamish, BC V8B 0B1")
    content = content.replace("Downtown Squamish, Squamish, BC V8B 0A1", "1 Watts Point Road, Squamish, BC V8B 0B1")
    content = content.replace("Marine Drive, West Vancouver, BC V7V 1J5", "1 Watts Point Road, Squamish, BC V8B 0B1")
    
    # Write back to file
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Local HTML landing pages have been cleaned and updated successfully!")
