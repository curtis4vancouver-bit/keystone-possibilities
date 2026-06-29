import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://keystonepossibilities.ca/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, context=ctx) as r:
        html = r.read().decode('utf-8')
        print("Theme CSS / JS links:")
        for line in html.split("\n"):
            if "wp-content/themes/" in line:
                print(line.strip())
except Exception as e:
    print("Error:", e)
