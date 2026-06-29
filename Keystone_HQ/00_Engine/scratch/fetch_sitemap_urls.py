import requests
import xml.etree.ElementTree as ET

sitemap_url = "https://keystonerecomposition.com/?keystone_video_sitemap=1"
print(f"Fetching sitemap from {sitemap_url}...")
try:
    response = requests.get(sitemap_url, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    print("Sitemap fetched successfully.")
    
    # Parse the XML
    root = ET.fromstring(response.content)
    
    # We need to find all <loc> tags. Since sitemaps typically use namespaces:
    # xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
    # xmlns:video="http://www.google.com/schemas/sitemap-video/1.1"
    namespaces = {
        'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9',
        'video': 'http://www.google.com/schemas/sitemap-video/1.1'
    }
    
    urls = []
    # Try with namespace first
    for url_elem in root.findall('ns:url', namespaces):
        loc = url_elem.find('ns:loc', namespaces)
        if loc is not None:
            urls.append(loc.text)
            
    # Fallback if no namespace matched
    if not urls:
        for loc in root.iter('loc'):
            urls.append(loc.text)
            
    print(f"Found {len(urls)} URLs:")
    for idx, url in enumerate(urls, 1):
        print(f"{idx}: {url}")
        
    with open("scratch/extracted_video_urls.txt", "w") as f:
        for url in urls:
            f.write(url + "\n")
    print("Saved URLs to scratch/extracted_video_urls.txt")
except Exception as e:
    print(f"Error: {e}")
