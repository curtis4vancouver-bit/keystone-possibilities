import requests
import json

bearer = "ya29.a0AT3oNZ8oXpN-NUt8VD1L6X8A7rNzuPxbkQE9nlRrgasxbr_nQ8RnNFonavXIlgIEmDc81gJ4lpTEhuOjcU1oUvYqP5TLgBuVVu0oU3BR9Cdm3oBr3XEw4dY9wNR8v6hDLHb0ExjCLsQy65iWB4tJsHCASfDNxz8EDNQ9mhmqDWeU1InaNAIq8jgdtKqWi69WIz91TQFhXmTRhblS0dsO3NyMdCmd8MUXqsY1FOzcXS5Iak6P2VjTAhaDlBlvtH2ejpvce8oam1TjJcv_3zAEZagX58EZ_dms0tC9qrtDUpuLAcNklz_DN0x9f6VmbU7j_e-iCNaKA4pNHEs6d8aAFj-C1A66gTx2xesWPdCWUk8aCgYKAX4SARcSFQHGX2MimRwR1oECmwSjAnhyXoxurw0370"

url = "https://labs.google/fx/api/trpc/project.get?batch=1&input=%7B%220%22%3A%7B%22id%22%3A%22827275bd-d7fa-422b-9c90-b67109344d47%22%7D%7D"
headers = {
    "Authorization": f"Bearer {bearer}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
    "Referer": "https://labs.google/fx/tools/flow/project/827275bd-d7fa-422b-9c90-b67109344d47",
    "Accept": "application/json"
}

resp = requests.get(url, headers=headers)
print("Status:", resp.status_code)
if resp.status_code == 200:
    data = resp.json()
    try:
        components = data[0]["result"]["data"]["components"]
        print(f"Got {len(components)} components!")
        for c in components:
            if c.get("type") in ["image", "video"] and c.get("media"):
                print("UUID:", c["id"], "MediaID:", c["media"].get("name") or c["media"].get("id"))
    except Exception as e:
        print("Parse error:", e)
else:
    print(resp.text)
