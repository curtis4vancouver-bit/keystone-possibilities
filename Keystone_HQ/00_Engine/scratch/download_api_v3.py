import os
import requests
import json
import browser_cookie3
from bs4 import BeautifulSoup
import re

def get_clip_urls():
    print("Extracting Chrome cookies...")
    try:
        cj = browser_cookie3.chrome()
        print(f"Extracted {len(cj)} cookies from Chrome!")
    except Exception as e:
        print("Failed to extract cookies:", e)
        return None
        
    url = "https://labs.google/fx/tools/flow/project/827275bd-d7fa-422b-9c90-b67109344d47"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    
    print(f"Fetching {url}...")
    resp = requests.get(url, cookies=cj, headers=headers)
    
    if "Sign in" in resp.text or resp.status_code != 200:
        print(f"Failed to authenticate. Status: {resp.status_code}")
        return None
        
    soup = BeautifulSoup(resp.text, 'html.parser')
    next_data_script = soup.find('script', id='__NEXT_DATA__')
    if not next_data_script:
        print("Could not find __NEXT_DATA__ in HTML.")
        return None
        
    next_data = json.loads(next_data_script.string)
    
    try:
        dehydrated = next_data["props"]["pageProps"]["trpcState"]["json"]["queries"]
        for query in dehydrated:
            if query["queryKey"][0] == "project" and query["queryKey"][1] == "get":
                project_data = query["state"]["data"]
                return project_data["components"], cj
    except Exception as e:
        print("Error parsing state:", e)
        return None
        
    return None

if __name__ == "__main__":
    result = get_clip_urls()
    if result:
        components, cj = result
        print(f"Success! Found {len(components)} components.")
        for c in components:
            if "prompt" in c and "media" in c and c["media"]:
                print("UUID:", c["media"]["name"])
                break
    else:
        print("Failed.")
