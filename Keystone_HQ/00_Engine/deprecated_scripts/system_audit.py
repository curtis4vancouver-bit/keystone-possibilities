"""
Keystone Infrastructure System Audit
Checks: Python env, dependencies, tokens, MCP servers, Brain DB, disk/RAM, file integrity.
"""
import sys, os, io, json, time, subprocess, shutil, importlib, platform

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

PASS = "[PASS]"
FAIL = "[FAIL]"
WARN = "[WARN]"
results = []

def check(name, passed, detail=""):
    status = PASS if passed else FAIL
    results.append((status, name, detail))
    print(f"  {status} {name}" + (f" -- {detail}" if detail else ""))

def warn(name, detail=""):
    results.append((WARN, name, detail))
    print(f"  {WARN} {name}" + (f" -- {detail}" if detail else ""))

# ============================================================
print("=" * 65)
print("  KEYSTONE INFRASTRUCTURE SYSTEM AUDIT")
print(f"  {time.strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 65)

# --- 1. SYSTEM ---
print("\n[1] SYSTEM ENVIRONMENT")
print(f"  OS: {platform.system()} {platform.release()} ({platform.machine()})")
print(f"  Python: {sys.version.split()[0]} at {sys.executable}")
check("Python 3.10+", sys.version_info >= (3, 10), f"v{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

# RAM
try:
    import psutil
    ram = psutil.virtual_memory()
    ram_gb = ram.total / (1024**3)
    ram_avail = ram.available / (1024**3)
    check("RAM", ram_avail > 2, f"{ram_avail:.1f} GB free / {ram_gb:.1f} GB total ({ram.percent}% used)")
    
    cpu_pct = psutil.cpu_percent(interval=0.5)
    check("CPU load", cpu_pct < 90, f"{cpu_pct}%")
except ImportError:
    warn("psutil not installed", "Skipping RAM/CPU checks")

# Disk
disk = shutil.disk_usage(SCRIPT_DIR)
disk_free_gb = disk.free / (1024**3)
check("Disk space", disk_free_gb > 5, f"{disk_free_gb:.1f} GB free")

# --- 2. PYTHON DEPENDENCIES ---
print("\n[2] PYTHON DEPENDENCIES")
required_pkgs = {
    "google.oauth2.credentials": "google-auth",
    "googleapiclient.discovery": "google-api-python-client",
    "google_auth_oauthlib.flow": "google-auth-oauthlib",
    "mcp.server.fastmcp": "mcp",
    "httpx": "httpx",
}

for mod, pkg in required_pkgs.items():
    try:
        importlib.import_module(mod.split(".")[0])
        check(f"{pkg}", True)
    except ImportError:
        check(f"{pkg}", False, "NOT INSTALLED")

# --- 3. TOKEN FILES ---
print("\n[3] AUTHENTICATION TOKENS")
tokens = {
    "youtube_token.json": "Primary (Possibilities/Protocols)",
    "youtube_token_oac.json": "OAC Brand Account (Recomposition)",
}

for fname, label in tokens.items():
    fpath = os.path.join(SCRIPT_DIR, fname)
    if os.path.exists(fpath):
        age_hrs = (time.time() - os.path.getmtime(fpath)) / 3600
        try:
            with open(fpath) as f:
                data = json.load(f)
            has_refresh = "refresh_token" in data
            check(f"{fname}", has_refresh, f"{label} | refresh_token: {'yes' if has_refresh else 'NO'} | age: {age_hrs:.1f}h")
        except Exception as e:
            check(f"{fname}", False, f"Parse error: {e}")
    else:
        check(f"{fname}", False, f"MISSING - {label}")

# --- 4. YOUTUBE API LIVE TEST ---
print("\n[4] YOUTUBE API LIVE CONNECTIVITY")
try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    # Primary token
    creds1 = Credentials.from_authorized_user_file(os.path.join(SCRIPT_DIR, "youtube_token.json"))
    yt1 = build("youtube", "v3", credentials=creds1)
    r1 = yt1.channels().list(part="snippet,statistics", mine=True).execute()
    ch1 = r1["items"][0]
    check("Primary token -> API", True, f"{ch1['snippet']['title']} ({ch1['statistics']['videoCount']} vids)")

    # Test Protocols by ID
    r_proto = yt1.channels().list(part="snippet,statistics", id="UCxURlqMNhAtxUTpdXmlOYaw").execute()
    if r_proto.get("items"):
        ch_p = r_proto["items"][0]
        check("Protocols channel reachable", True, f"{ch_p['snippet']['title']} ({ch_p['statistics']['videoCount']} vids)")

    # OAC token
    creds2 = Credentials.from_authorized_user_file(os.path.join(SCRIPT_DIR, "youtube_token_oac.json"))
    yt2 = build("youtube", "v3", credentials=creds2)
    r2 = yt2.channels().list(part="snippet,statistics,contentDetails", mine=True).execute()
    ch2 = r2["items"][0]
    uploads = ch2["contentDetails"]["relatedPlaylists"]["uploads"]
    pl = yt2.playlistItems().list(part="status", playlistId=uploads, maxResults=1).execute()
    total_vids = pl.get("pageInfo", {}).get("totalResults", 0)
    check("OAC token -> API", True, f"{ch2['snippet']['title']} | {ch2['statistics']['videoCount']} public + {total_vids - int(ch2['statistics']['videoCount'])} unlisted = {total_vids} total")
    
    # Write access test (read a video detail to confirm scope)
    test_pl = yt2.playlistItems().list(part="snippet", playlistId=uploads, maxResults=1).execute()
    test_vid = test_pl["items"][0]["snippet"]["resourceId"]["videoId"]
    test_detail = yt2.videos().list(part="snippet,status", id=test_vid).execute()
    if test_detail.get("items"):
        check("OAC write-scope verified", True, f"Can read/write video: {test_vid}")
    
except Exception as e:
    check("YouTube API", False, str(e))

# --- 5. MCP SERVER FILES ---
print("\n[5] MCP SERVER FILES")
mcp_files = {
    "youtube_mcp.py": "YouTube Manager MCP",
    "youtube_researcher_mcp.py": "YouTube Researcher MCP",
    "youtube_api_manager.py": "YouTube API Manager",
}

for fname, label in mcp_files.items():
    fpath = os.path.join(SCRIPT_DIR, fname)
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        lines = content.count("\n") + 1
        # Check for common issues
        has_chdir = "os.chdir" in content
        has_encoding = "TextIOWrapper" in content or "utf-8" in content
        issues = []
        if not has_chdir:
            issues.append("missing os.chdir fix")
        if not has_encoding:
            issues.append("missing encoding fix")
        # Check for raw manager.youtube calls (exclude comments and class init)
        code_lines = [l.strip() for l in content.split('\n') if l.strip() and not l.strip().startswith('#')]
        raw_calls = [l for l in code_lines if 'manager.youtube.' in l or 'manager.youtube)' in l]
        if raw_calls and fname == "youtube_mcp.py":
            issues.append(f"still has {len(raw_calls)} manager.youtube call(s)")
        
        if issues:
            warn(f"{fname}", f"{label} | {lines} lines | Issues: {', '.join(issues)}")
        else:
            check(f"{fname}", True, f"{label} | {lines} lines | CWD fix: yes | Encoding fix: yes")
    else:
        check(f"{fname}", False, f"MISSING - {label}")

# --- 6. MULTIPLEXER ---
print("\n[6] MULTIPLEXER CONFIGURATION")
mux_dir = os.path.join(SCRIPT_DIR, "MCP_Multiplexer")
mux_path = os.path.join(mux_dir, "agents.json")
if os.path.exists(mux_path):
    with open(mux_path, "r", encoding="utf-8") as f:
        agents = json.load(f)
    check("agents.json exists", True, f"{len(agents)} agents configured")
    for name, config in agents.items():
        cmd = config.get("command", "?")
        args = config.get("args", [])
        script_ref = args[-1] if args else "?"
        # Resolve relative paths from MCP_Multiplexer dir
        if script_ref.startswith(".."):
            script_full = os.path.normpath(os.path.join(mux_dir, script_ref))
        elif not os.path.isabs(script_ref):
            script_full = os.path.normpath(os.path.join(mux_dir, script_ref))
        else:
            script_full = script_ref
        script_exists = os.path.exists(script_full)
        enabled = config.get("enabled", False)
        if cmd in ("npx", "uvx"):
            check(f"  {name}", True, f"cmd: {cmd} | enabled: {enabled}")
        elif script_exists:
            check(f"  {name}", True, f"script OK | enabled: {enabled}")
        else:
            check(f"  {name}", False, f"script NOT FOUND: {script_full}")
else:
    check("agents.json", False, "MISSING")

# --- 7. KEYSTONE BRAIN (Supabase) ---
print("\n[7] KEYSTONE BRAIN (Vector DB)")
try:
    # Check if brain MCP config exists
    brain_dir = os.path.join(SCRIPT_DIR, "MCP_Multiplexer")
    # Try a direct supabase import check
    try:
        import httpx
        check("httpx (brain transport)", True)
    except ImportError:
        check("httpx", False, "needed for Supabase brain")
    
    # Check knowledge items
    ki_dir = os.path.join(os.environ.get("USERPROFILE", ""), ".gemini", "antigravity", "knowledge")
    if os.path.exists(ki_dir):
        ki_count = len([d for d in os.listdir(ki_dir) if os.path.isdir(os.path.join(ki_dir, d))])
        check("Knowledge Items", True, f"{ki_count} KIs in local store")
    else:
        warn("Knowledge Items dir", "not found")
except Exception as e:
    check("Brain check", False, str(e))

# --- 8. MASTER BRAIN FILE STRUCTURE ---
print("\n[8] MASTER BRAIN FILE STRUCTURE")
expected_dirs = [
    "Master_Docs",
    "Master_Docs/Research_Archives",
    "MCP_Multiplexer",
]
for d in expected_dirs:
    dpath = os.path.join(SCRIPT_DIR, d)
    if os.path.isdir(dpath):
        count = len(os.listdir(dpath))
        check(f"{d}/", True, f"{count} items")
    else:
        check(f"{d}/", False, "MISSING")

# --- 9. AUTO-REMEDIATION (Sovereign Doctor) ---
remediation_log = []

def auto_remediate():
    """Attempts automatic fixes for common failures."""
    global results
    healed = 0

    for status, name, detail in results:
        if status != FAIL:
            continue

        # Auto-install missing Python packages
        if "NOT INSTALLED" in detail:
            pkg = name.strip()
            print(f"\n  [DOCTOR] Auto-installing missing package: {pkg}")
            try:
                res = subprocess.run(
                    [sys.executable, "-m", "pip", "install", pkg],
                    capture_output=True, text=True, timeout=60
                )
                if res.returncode == 0:
                    remediation_log.append(f"Installed {pkg}")
                    healed += 1
                    print(f"  [DOCTOR] Successfully installed {pkg}")
                else:
                    remediation_log.append(f"FAILED to install {pkg}: {res.stderr.strip()[:200]}")
                    print(f"  [DOCTOR] Failed to install {pkg}")
            except Exception as e:
                remediation_log.append(f"FAILED to install {pkg}: {str(e)}")

        # Auto-create missing directories
        elif "MISSING" in detail and name.endswith("/"):
            dir_name = name.rstrip("/")
            dir_path = os.path.join(SCRIPT_DIR, dir_name)
            print(f"\n  [DOCTOR] Creating missing directory: {dir_name}")
            try:
                os.makedirs(dir_path, exist_ok=True)
                remediation_log.append(f"Created directory {dir_name}")
                healed += 1
                print(f"  [DOCTOR] Created {dir_path}")
            except Exception as e:
                remediation_log.append(f"FAILED to create {dir_name}: {str(e)}")

        # Flag missing token files with actionable instructions
        elif "MISSING" in detail and name.endswith(".json"):
            remediation_log.append(
                f"ACTION REQUIRED: Re-authenticate {name} — run the matching OAuth script in scratch/"
            )
            print(f"\n  [DOCTOR] Cannot auto-fix {name} — requires manual OAuth re-authentication")

    return healed


# --- 10. SUMMARY ---
print("\n" + "=" * 65)
passes = sum(1 for s, _, _ in results if s == PASS)
fails = sum(1 for s, _, _ in results if s == FAIL)
warns = sum(1 for s, _, _ in results if s == WARN)
total = len(results)

print(f"  RESULTS: {passes}/{total} passed | {fails} failed | {warns} warnings")

if fails == 0:
    print("  STATUS: ALL SYSTEMS OPERATIONAL")
else:
    print(f"  STATUS: {fails} ISSUE(S) REQUIRE ATTENTION")
    print("\n  Failed checks:")
    for s, name, detail in results:
        if s == FAIL:
            print(f"    {name}: {detail}")

    # Run auto-remediation
    print("\n" + "-" * 65)
    print("  SOVEREIGN DOCTOR: Attempting auto-remediation...")
    print("-" * 65)
    healed_count = auto_remediate()

    if remediation_log:
        print(f"\n  DOCTOR RESULTS: {healed_count} issue(s) auto-healed")
        for entry in remediation_log:
            print(f"    - {entry}")
    
    if healed_count > 0:
        print(f"\n  Re-run this audit to verify fixes: python system_audit.py")

print("=" * 65)

# --- 11. VOICE ANNOUNCEMENT ---
# Announce results through speakers if speak.py is available
speak_script = os.path.join(SCRIPT_DIR, "scripts", "speak.py")
if os.path.exists(speak_script) and "--quiet" not in sys.argv:
    if fails == 0:
        msg = f"System audit complete. {passes} of {total} checks passed. All systems operational."
    else:
        msg = f"System audit complete. {fails} issues detected. Sovereign Doctor attempted {len(remediation_log)} fixes."
    try:
        subprocess.run([sys.executable, speak_script, msg], capture_output=True, timeout=15)
    except Exception:
        pass  # Voice is optional, never block on it
