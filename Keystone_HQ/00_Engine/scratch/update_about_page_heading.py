import json
import urllib.request
import re

# Read the Gutenberg content from the output file
fpath = r"C:\Users\Curtis\.gemini\antigravity\brain\69f4ab04-3dc1-4dfb-9eff-fd3ab39fafcf\.system_generated\steps\325\output.txt"
with open(fpath, "r", encoding="utf-8") as f:
    text = f.read()

# Extract JSON string from output text
# The file has:
# Script ran on page and returned:
# ```json
# {...}
# ```
json_match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
if not json_match:
    print("Failed to find JSON in file.")
    exit(1)

data = json.loads(json_match.group(1))
content = data["content"]

# Print original section for reference
target_old = 'Wayne Stevenson, Founder & Principal'
target_new = 'Wayne Stevenson — Founder & Certified BC Builder (#52603)'

if target_old in content:
    print("Found old heading. Replacing...")
    updated_content = content.replace(target_old, target_new)
else:
    print("Old heading not found. Let's see if it's already updated.")
    # Check if new heading already there
    if target_new in content:
        print("Already updated!")
        exit(0)
    else:
        # Check if there is some other variant
        print("Neither old nor new heading found.")
        print("Excerpt:")
        print(content[content.find("Wayne Stevenson"):content.find("Wayne Stevenson")+100])
        exit(1)

# Now prepare the POST payload
payload = {
    "post_id": 2,
    "content": updated_content,
    "title": "About Us"
}

url = "https://keystonepossibilities.ca/?update_page_sovereign=1"
req_body = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(
    url,
    data=req_body,
    headers={"Content-Type": "application/json"}
)

try:
    with urllib.request.urlopen(req, timeout=30) as response:
        res_body = response.read().decode("utf-8")
        res_data = json.loads(res_body)
        print("Response:", res_data)
except Exception as e:
    print("Error during update request:", e)
