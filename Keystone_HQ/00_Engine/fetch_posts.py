import urllib.request, json, sys, os
os.environ["PYTHONIOENCODING"] = "utf-8"
sys.stdout.reconfigure(encoding="utf-8")

post_ids = [1149, 1080, 982, 974]

for pid in post_ids:
    url = "https://keystonerecomposition.com/?read_post_full=" + str(pid)
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        with open("post_" + str(pid) + ".json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("=== POST " + str(pid) + " ===")
        print("Title: " + data["title"])
        print("Slug: " + data["slug"])
        print("Content length: " + str(len(data["content"])))
        # Write content preview to file to avoid encoding issues
        with open("post_" + str(pid) + "_preview.txt", "w", encoding="utf-8") as f:
            f.write(data["content"][:5000])
        print("Preview saved to file")
        print("---END---")
        print()
print("ALL DONE")
