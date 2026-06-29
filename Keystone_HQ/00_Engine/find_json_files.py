import os

def find_json():
    root_dir = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.endswith(".json") and "token" in f.lower():
                print(os.path.join(dirpath, f))

if __name__ == "__main__":
    find_json()
