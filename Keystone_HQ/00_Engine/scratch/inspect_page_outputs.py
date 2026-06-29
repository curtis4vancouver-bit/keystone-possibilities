import os
import json

scratch_dir = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scratch"

def main():
    json_files = [f for f in os.listdir(scratch_dir) if f.startswith("page") and f.endswith("_output.json")]
    print(f"Found {len(json_files)} page output files.")
    
    for f in sorted(json_files, key=lambda x: int(x.replace("page", "").replace("_output.json", ""))):
        path = os.path.join(scratch_dir, f)
        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
                report_full = data.get("reportFull", "")
                title = ""
                # Get the first line as title
                if report_full:
                    lines = report_full.strip().split("\n")
                    if lines:
                        title = lines[0]
                print(f"File: {f} -> Size: {len(report_full)} chars -> Title: {title[:80]}")
        except Exception as e:
            print(f"Error reading {f}: {e}")

if __name__ == "__main__":
    main()
