import json
import os

def extract(json_path, output_filename):
    target_dir = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Deep_Research_Results"
    target_path = os.path.join(target_dir, output_filename)

    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at {json_path}")
        return False

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            report_text = json.load(f)
    except Exception as e:
        print(f"Error parsing JSON file {json_path}: {e}")
        return False

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    with open(target_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"Successfully extracted report from {json_path} and saved to: {target_path}")
    return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        extract(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python extract_from_json.py <json_path> <output_filename>")
