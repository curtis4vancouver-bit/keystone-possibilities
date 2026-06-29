import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def get_github(url):
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/vnd.github.v3+json'
        }
    )
    try:
        with urllib.request.urlopen(req, context=ctx) as r:
            return json.loads(r.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

print("=== LATEST COMMITS ===")
commits = get_github("https://api.github.com/repos/curtis4vancouver-bit/second-website/commits?per_page=5")
if commits:
    for c in commits:
        sha = c['sha'][:7]
        msg = c['commit']['message'].split('\n')[0]
        date = c['commit']['author']['date']
        print(f"{sha} - {date} - {msg}")

print("\n=== DEPLOYMENTS ===")
deploys = get_github("https://api.github.com/repos/curtis4vancouver-bit/second-website/deployments")
if deploys:
    print(json.dumps(deploys, indent=2))
else:
    print("No deployments found.")
