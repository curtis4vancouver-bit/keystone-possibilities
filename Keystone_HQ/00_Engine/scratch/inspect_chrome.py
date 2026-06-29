import json
import os

preferences_paths = [
    r"C:\Users\Curtis\AppData\Local\Google\Chrome\User Data\Default\Secure Preferences",
    r"C:\Users\Curtis\AppData\Local\Google\Chrome\User Data\Profile 1\Secure Preferences",
    r"C:\Users\Curtis\AppData\Local\Google\Chrome\User Data\Default\Preferences",
    r"C:\Users\Curtis\AppData\Local\Google\Chrome\User Data\Profile 1\Preferences"
]

for path in preferences_paths:
    if not os.path.exists(path):
        continue
    print(f"\nAnalyzing: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        extensions = data.get("extensions", {}).get("settings", {})
        print(f"Total extensions: {len(extensions)}")
        for ext_id, ext_info in extensions.items():
            manifest = ext_info.get("manifest", {})
            name = manifest.get("name", "")
            path_str = ext_info.get("path", "")
            location = ext_info.get("location", 0)
            
            if location in [1, 4] or (name and not name.startswith("Chrome") and not name.startswith("Google")):
                print(f"Extension ID: {ext_id}")
                print(f"  Name: {name}")
                print(f"  Path: {path_str}")
                print(f"  Location: {location}")
    except Exception as e:
        print(f"Error reading path {path}: {str(e)}")
