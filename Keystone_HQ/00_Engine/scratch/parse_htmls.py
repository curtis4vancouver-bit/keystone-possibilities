import glob
import os
import re

def parse_html(fpath):
    try:
        content = open(fpath, 'r', encoding='utf-8', errors='ignore').read()
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
        # Check for Rank Math title/desc comment or tags as well
        title = title_match.group(1) if title_match else 'No Title'
        desc = desc_match.group(1) if desc_match else 'No Description'
        print(f"{os.path.basename(fpath)} | Title: {title} | Desc: {desc[:60]}...")
    except Exception as e:
        print('Error parsing:', os.path.basename(fpath), e)

print('=== 02_Websites Directory ===')
for f in glob.glob(r'C:\Users\Curtis\New folder\construction-website\Keystone_HQ\02_Websites\*.html'):
    parse_html(f)

print('\n=== Local_SEO_Domination Directory ===')
for f in glob.glob(r'C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\02_Keystone_Possibilities\Local_SEO_Domination\*.html'):
    parse_html(f)
