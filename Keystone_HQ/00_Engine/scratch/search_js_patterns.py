import glob
import os

def main():
    print("Searching for automation tool calls...")
    keywords = ["evaluate_script", "click", "select_page", "new_page", "ql-editor", "insertText", "send"]
    for f in glob.glob("scratch/*"):
        if os.path.isdir(f) or f.endswith("search_js_patterns.py"):
            continue
        try:
            with open(f, "r", encoding="utf-8", errors="ignore") as file:
                for i, line in enumerate(file, 1):
                    for kw in keywords:
                        if kw in line:
                            print(f"{f}:{i} ({kw}): {line.strip()[:100]}")
                            break
        except Exception as e:
            pass

if __name__ == "__main__":
    main()
