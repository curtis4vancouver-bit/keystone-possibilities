import os

keywords = ["pusher", "deploy", "git", "webhook", "token", "github", "secret"]
docs_dir = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Master_Docs"

for file in os.listdir(docs_dir):
    if file.endswith(".md"):
        path = os.path.join(docs_dir, file)
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                for kw in keywords:
                    if kw.lower() in content.lower():
                        # print context around the match
                        for line in content.split("\n"):
                            if kw.lower() in line.lower():
                                print(f"{file}: matched '{kw}': {line.strip()[:120]}")
        except Exception as e:
            pass
