import os
from pathlib import Path

user_home = Path(os.path.expanduser("~"))
search_paths = [
    user_home / "AppData" / "Roaming",
    user_home / "AppData" / "Local",
    user_home / ".config",
    user_home
]

print("Searching for Google Workspace token/credential files...")
found_files = []

for base_path in search_paths:
    if not base_path.exists():
        continue
    print(f"Scanning: {base_path}")
    # Search recursively for files containing 'token' or 'credential' in their names
    # Limit depth to avoid scanning everything in Local
    try:
        for root, dirs, files in os.walk(base_path):
            # Prune directories to keep search shallow and fast
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('Temp', 'Cache', 'npm', 'yarn', 'Microsoft', 'Package Cache', 'Node')]
            
            # Check depth
            depth = len(Path(root).relative_to(base_path).parts)
            if depth > 4:
                dirs.clear() # don't go deeper
                
            for file in files:
                file_lower = file.lower()
                if ("token" in file_lower or "credential" in file_lower) and file.endswith(".json"):
                    full_path = os.path.join(root, file)
                    found_files.append(full_path)
                    print(f"Found: {full_path}")
    except Exception as e:
        print(f"Error scanning {base_path}: {e}")

print(f"\nDone. Found {len(found_files)} files.")
