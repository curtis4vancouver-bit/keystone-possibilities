import requests
import json
import xml.etree.ElementTree as ET
from google.oauth2 import service_account
import google.auth.transport.requests

# Path to the service account key
KEY_PATH = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scratch\gcs_key.json"
SITEMAP_URL = "https://keystonepossibilities.ca/post-sitemap.xml"
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
SCOPES = ["https://www.googleapis.com/auth/indexing"]

def get_access_token():
    credentials = service_account.Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES)
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    return credentials.token

def get_urls_from_sitemap(sitemap_url):
    response = requests.get(sitemap_url)
    response.raise_for_status()
    root = ET.fromstring(response.content)
    # The XML uses namespaces, typically: xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = []
    for url_element in root.findall('ns:url', namespace):
        loc = url_element.find('ns:loc', namespace)
        if loc is not None:
            urls.append(loc.text)
    return urls

def publish_url(url, token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "url": url,
        "type": "URL_UPDATED"
    }
    response = requests.post(ENDPOINT, headers=headers, json=payload)
    return response.status_code, response.json()

if __name__ == "__main__":
    print("Fetching sitemap...")
    urls = get_urls_from_sitemap(SITEMAP_URL)
    print(f"Found {len(urls)} URLs to index.")

    print("Authenticating with Google API...")
    try:
        token = get_access_token()
    except Exception as e:
        print(f"Failed to authenticate: {e}")
        exit(1)

    print("Pushing URLs to Google Indexing API...")
    success_count = 0
    for i, url in enumerate(urls):
        status, resp_json = publish_url(url, token)
        if status == 200:
            success_count += 1
            print(f"[{i+1}/{len(urls)}] SUCCESS: {url}")
        else:
            print(f"[{i+1}/{len(urls)}] ERROR {status} for {url}: {resp_json}")
    
    print(f"\nCompleted! Successfully submitted {success_count} out of {len(urls)} URLs.")
