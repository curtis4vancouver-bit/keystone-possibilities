import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://keystonepossibilities.ca/2026/06/06/bill-44-fourplex-cost/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, context=ctx) as r:
        html = r.read().decode('utf-8')
        print("Searching for VideoObject schema in page source...")
        if "VideoObject" in html:
            print("Found VideoObject in HTML!")
            # Print around the matches
            idx = 0
            while True:
                idx = html.find("VideoObject", idx)
                if idx == -1:
                    break
                start = max(0, idx - 200)
                end = min(len(html), idx + 800)
                print(f"--- MATCH AT INDEX {idx} ---")
                print(html[start:end])
                idx += len("VideoObject")
        else:
            print("VideoObject NOT found in HTML page.")
except Exception as e:
    print("Error:", e)
