import requests
import xml.etree.ElementTree as ET

sitemap_url = "https://keystonepossibilities.ca/?keystone_video_sitemap=1"
print(f"Fetching sitemap from {sitemap_url}...")
try:
    response = requests.get(sitemap_url, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    print("Sitemap fetched successfully.")
    
    root = ET.fromstring(response.content)
    namespaces = {
        'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9',
        'video': 'http://www.google.com/schemas/sitemap-video/1.1'
    }
    
    urls = []
    for url_elem in root.findall('ns:url', namespaces):
        loc = url_elem.find('ns:loc', namespaces)
        if loc is not None:
            urls.append(loc.text)
            
    if not urls:
        for loc in root.iter('loc'):
            urls.append(loc.text)
            
    print(f"Found {len(urls)} URLs on Keystone Possibilities:")
    for idx, url in enumerate(urls, 1):
        print(f"{idx}: {url}")
        
    with open("scratch/extracted_possibilities_video_urls.txt", "w") as f:
        for url in urls:
            f.write(url + "\n")
except Exception as e:
    print(f"Error: {e}")
