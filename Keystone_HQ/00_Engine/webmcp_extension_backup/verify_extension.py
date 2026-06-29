import os
import json
import sys

def verify_extension():
    print("=" * 60)
    print(" KEYSTONE WEBMCP CHROME EXTENSION VERIFICATION REPORT")
    print("=" * 60)
    
    ext_dir = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Engine\webmcp_extension"
    
    # 1. Check Directory Existence
    if not os.path.exists(ext_dir):
        print(f"[FAIL] Extension directory does not exist: {ext_dir}")
        sys.exit(1)
    print(f"[OK] Extension directory exists: {ext_dir}")
    
    # 2. Check Required Files
    required_files = [
        "manifest.json",
        "service_worker.js",
        "content_scripts/google_flow.js",
        "content_scripts/isolated_bridge.js",
        "popup.html",
        "popup.js",
        "icons/icon16.png",
        "icons/icon48.png",
        "icons/icon128.png"
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = os.path.join(ext_dir, file_path)
        if not os.path.exists(full_path):
            missing_files.append(file_path)
            print(f"[FAIL] Missing file: {file_path}")
        else:
            size = os.path.getsize(full_path)
            print(f"[OK] File exists: {file_path} ({size} bytes)")
            
    if missing_files:
        print(f"\n[FAIL] Verification failed. Missing {len(missing_files)} file(s).")
        sys.exit(1)
        
    # 3. Validate manifest.json Structure
    manifest_path = os.path.join(ext_dir, "manifest.json")
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
            
        print("[OK] manifest.json parses successfully as valid JSON.")
        
        # Check Manifest Version
        if manifest.get("manifest_version") != 3:
            print("[FAIL] manifest.json is not Manifest V3 (manifest_version must be 3)")
            sys.exit(1)
        print("[OK] Manifest Version is 3 (Manifest V3 compliance).")
        
        # Check Permissions
        permissions = manifest.get("permissions", [])
        required_perms = ["downloads", "storage", "scripting"]
        for perm in required_perms:
            if perm not in permissions:
                print(f"[FAIL] Missing permission: {perm}")
                sys.exit(1)
            print(f"[OK] Permission granted: '{perm}'")
            
        # Check Content Scripts Configuration
        scripts = manifest.get("content_scripts", [])
        if len(scripts) < 2:
            print("[FAIL] Incomplete content script configurations. Need isolated and main worlds.")
            sys.exit(1)
            
        worlds = [s.get("world") for s in scripts]
        if "MAIN" not in worlds or "ISOLATED" not in worlds:
            print(f"[FAIL] Missing execution world definitions. Found: {worlds}")
            sys.exit(1)
        print("[OK] Both MAIN and ISOLATED execution worlds configured.")
        
    except Exception as e:
        print(f"[FAIL] Failed to validate manifest.json: {e}")
        sys.exit(1)
        
    # 4. Check JS File Contents for Key API Elements
    print("\nVerifying Google Flow Content Script APIs...")
    flow_js_path = os.path.join(ext_dir, "content_scripts", "google_flow.js")
    with open(flow_js_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    required_apis = [
        "fillPrompt",
        "uploadReference",
        "clickGenerate",
        "getQueueStatus",
        "getDownloadLinks",
        "getCreditsRemaining",
        "window.keystoneWebMCP"
    ]
    
    for api in required_apis:
        if api not in content:
            print(f"[FAIL] API element '{api}' not found in google_flow.js")
            sys.exit(1)
        print(f"[OK] API element '{api}' is defined in google_flow.js")
        
    print("\n" + "=" * 60)
    print(" ALL VERIFICATION CHECKS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    verify_extension()
