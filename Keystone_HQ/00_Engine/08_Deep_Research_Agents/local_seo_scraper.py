import requests
from bs4 import BeautifulSoup
import json
import datetime

def scrape_local_seo_data(keyword, location):
    print(f"[{datetime.datetime.now()}] Starting Local SEO Audit for: {keyword} in {location}")
    
    # Simulating the search query parameters
    query = f"{keyword} {location}".replace(" ", "+")
    url = f"https://www.google.com/search?q={query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Look for local pack results or standard organic results
            results = soup.find_all('h3')
            
            report = {
                "timestamp": str(datetime.datetime.now()),
                "target_keyword": keyword,
                "location": location,
                "competitors": []
            }
            
            for i, result in enumerate(results[:5], 1):
                title = result.get_text()
                # Finding parent link
                parent = result.find_parent('a')
                link = parent['href'] if parent else "N/A"
                
                report["competitors"].append({
                    "rank": i,
                    "title": title,
                    "url": link
                })
                
            return report
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error during scraping: {e}")
        return None

if __name__ == "__main__":
    # Test execution for Whistler and West Vancouver
    locations = ["Whistler", "West Vancouver", "North Vancouver"]
    keyword = "Construction Project Management"
    
    master_report = {}
    
    for loc in locations:
        data = scrape_local_seo_data(keyword, loc)
        if data:
            master_report[loc] = data
            
    # Save to JSON for analysis
    with open("seo_competitor_audit.json", "w") as f:
        json.dump(master_report, f, indent=4)
        
    print("\n[SUCCESS] Local SEO Competitor Audit completed. Data saved to seo_competitor_audit.json")
