import os

def find_tokens():
    search_dirs = [
        r"C:\Users\Curtis\.gemini",
        r"C:\Users\Curtis\New folder\construction-website"
    ]
    for root_dir in search_dirs:
        print(f"\nSearching in: {root_dir}")
        for dirpath, _, filenames in os.walk(root_dir):
            for f in filenames:
                if "token" in f.lower() and f.endswith(".json"):
                    full_path = os.path.join(dirpath, f)
                    print(f"Found token file: {full_path}")

if __name__ == "__main__":
    find_tokens()
