import json
import urllib.request
from google.oauth2 import service_account
import google.auth.transport.requests

KEY_PATH = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scratch\gcs_key.json"
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
SCOPES = ["https://www.googleapis.com/auth/indexing"]

def get_access_token():
    credentials = service_account.Credentials.from_service_account_file(KEY_PATH, scopes=SCOPES)
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    return credentials.token

def publish_url(url, token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "url": url,
        "type": "URL_UPDATED"
    }
    req_body = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        ENDPOINT,
        data=req_body,
        headers=headers,
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            res_body = response.read().decode('utf-8')
            return response.status, json.loads(res_body)
    except Exception as e:
        print(f"Error publishing {url}: {e}")
        return 500, {'error': str(e)}

def main():
    url = "https://keystonerecomposition.com/2026/06/07/klow-vs-glow-peptide-stacks-science/"
    
    print("Authenticating with Google API...")
    try:
        token = get_access_token()
        print("Authenticated successfully!")
    except Exception as e:
        print(f"Failed to authenticate: {e}")
        return
        
    print(f"Pushing URL {url} to Google Indexing API...")
    status, resp_json = publish_url(url, token)
    if status == 200:
        print(f"SUCCESS: {url}")
    else:
        print(f"ERROR {status} for {url}: {resp_json}")

if __name__ == "__main__":
    main()
