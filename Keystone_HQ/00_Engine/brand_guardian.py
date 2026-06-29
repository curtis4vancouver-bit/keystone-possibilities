"""
Keystone Brand Constitution Guardian v1.0
==========================================
Write-protection layer for the Brand Constitution.
Only the Master Brain (Chronos) can modify brand files.
All other agents must go through this gatekeeper.

Usage:
  python brand_guardian.py --update voice --change "Added new prohibition on age references"
  python brand_guardian.py --update visual --change "Updated thumbnail hex colors to gold"
  python brand_guardian.py --update direction --change "Shifted Protocol to Wolverine Stack S2"
  python brand_guardian.py --check               # Verify integrity of all brand files
  python brand_guardian.py --lock                 # Enforce read-only on all brand files
  python brand_guardian.py --history              # Show change history
"""
import os
import sys
import json
import hashlib
import argparse
import datetime
import shutil

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BRAND_DIR = os.path.join(PROJECT_ROOT, "Brand_Constitution")
GUARDIAN_STATE = os.path.join(BRAND_DIR, ".guardian_state.json")
EVOLUTION_LOG = os.path.join(BRAND_DIR, "BRAND_EVOLUTION_LOG.jsonl")
BACKUP_DIR = os.path.join(BRAND_DIR, ".backups")

# Core brand files that are protected
PROTECTED_FILES = [
    "BRAND_VOICE.md",
    "BRAND_VISUAL.md",
    "CURRENT_DIRECTION.md",
    "possibilities/IDENTITY.md",
    "protocol/IDENTITY.md",
    "music/IDENTITY.md",
    "shared/AVATAR_RULES.md",
    "shared/PLATFORM_STANDARDS.md",
]


def ensure_dirs():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    os.makedirs(BRAND_DIR, exist_ok=True)


def compute_file_hash(filepath: str) -> str:
    """Compute SHA-256 hash of a file."""
    if not os.path.exists(filepath):
        return "MISSING"
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for block in iter(lambda: f.read(8192), b""):
            sha256.update(block)
    return sha256.hexdigest()


def load_guardian_state() -> dict:
    """Load the guardian state (file hashes for integrity checking)."""
    if os.path.exists(GUARDIAN_STATE):
        try:
            with open(GUARDIAN_STATE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"hashes": {}, "last_check": None, "version": 1}


def save_guardian_state(state: dict):
    """Save guardian state."""
    with open(GUARDIAN_STATE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def snapshot_hashes() -> dict:
    """Compute current hashes for all protected files."""
    hashes = {}
    for rel_path in PROTECTED_FILES:
        full_path = os.path.join(BRAND_DIR, rel_path)
        hashes[rel_path] = compute_file_hash(full_path)
    return hashes


# ─── Integrity Check ────────────────────────────────────────────────────

def check_integrity() -> bool:
    """
    Verify that no protected brand files have been modified
    outside of the Brand Guardian.
    """
    print("\n[Guardian] Brand Constitution Integrity Check")
    print("=" * 55)
    
    state = load_guardian_state()
    stored_hashes = state.get("hashes", {})
    current_hashes = snapshot_hashes()
    
    all_good = True
    
    for rel_path in PROTECTED_FILES:
        current = current_hashes.get(rel_path, "MISSING")
        stored = stored_hashes.get(rel_path)
        full_path = os.path.join(BRAND_DIR, rel_path)
        
        if current == "MISSING":
            print(f"  [MISSING]  {rel_path}")
            all_good = False
        elif stored is None:
            print(f"  [NEW]      {rel_path} (first run, registering)")
        elif current != stored:
            print(f"  [CHANGED]  {rel_path}")
            print(f"             Expected: {stored[:16]}...")
            print(f"             Current:  {current[:16]}...")
            all_good = False
        else:
            print(f"  [OK]       {rel_path}")
    
    if all_good:
        print(f"\n  All {len(PROTECTED_FILES)} brand files verified intact.")
    else:
        print(f"\n  WARNING: Brand files have been modified outside the Guardian!")
        print(f"  Run --lock to re-register current state, or restore from backups.")
    
    return all_good


# ─── Authorized Update ──────────────────────────────────────────────────

def authorized_update(target: str, change_description: str, caller: str = "chronos_master"):
    """
    Perform an authorized brand update with full audit trail.
    Only Chronos (Master Brain) should call this.
    """
    ensure_dirs()
    
    # Map target to file
    target_map = {
        "voice": "BRAND_VOICE.md",
        "visual": "BRAND_VISUAL.md",
        "direction": "CURRENT_DIRECTION.md",
        "avatar": "shared/AVATAR_RULES.md",
        "platforms": "shared/PLATFORM_STANDARDS.md",
        "possibilities": "possibilities/IDENTITY.md",
        "protocol": "protocol/IDENTITY.md",
        "music": "music/IDENTITY.md",
    }
    
    target_file = target_map.get(target.lower())
    if not target_file:
        print(f"[Guardian] ERROR: Unknown target '{target}'")
        print(f"  Valid targets: {', '.join(target_map.keys())}")
        return False
    
    full_path = os.path.join(BRAND_DIR, target_file)
    
    # Step 1: Backup current version
    if os.path.exists(full_path):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{target_file.replace('/', '_').replace('.md', '')}_{timestamp}.md"
        backup_path = os.path.join(BACKUP_DIR, backup_name)
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        shutil.copy2(full_path, backup_path)
        print(f"[Guardian] Backed up: {target_file} -> .backups/{backup_name}")
    
    # Step 2: Log the change to evolution log
    log_entry = {
        "date": datetime.datetime.now().isoformat(),
        "target": target_file,
        "change": change_description,
        "authorized_by": caller,
        "pre_hash": compute_file_hash(full_path),
    }
    
    with open(EVOLUTION_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")
    
    print(f"[Guardian] Change logged to BRAND_EVOLUTION_LOG.jsonl")
    print(f"[Guardian] Target file ready for editing: {full_path}")
    print(f"[Guardian] After editing, run --lock to re-register the hash.")
    
    return True


# ─── Lock (Re-register hashes) ──────────────────────────────────────────

def lock_brand():
    """Re-register all file hashes as the new baseline."""
    print("\n[Guardian] Locking Brand Constitution...")
    
    state = load_guardian_state()
    state["hashes"] = snapshot_hashes()
    state["last_check"] = datetime.datetime.now().isoformat()
    save_guardian_state(state)
    
    registered = 0
    for rel_path, hash_val in state["hashes"].items():
        status = "REGISTERED" if hash_val != "MISSING" else "MISSING"
        print(f"  [{status}] {rel_path}")
        if hash_val != "MISSING":
            registered += 1
    
    print(f"\n  Locked {registered}/{len(PROTECTED_FILES)} brand files.")
    print(f"  Guardian state saved to: .guardian_state.json")


# ─── History ─────────────────────────────────────────────────────────────

def show_history():
    """Show brand evolution history."""
    print("\n[Guardian] Brand Evolution History")
    print("=" * 55)
    
    if not os.path.exists(EVOLUTION_LOG):
        print("  No evolution history found.")
        return
    
    entries = []
    with open(EVOLUTION_LOG, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    
    if not entries:
        print("  No evolution entries found.")
        return
    
    for entry in entries[-15:]:  # Show last 15
        date = entry.get("date", "?")[:19]
        change = entry.get("change", "No description")
        target = entry.get("target", "?")
        author = entry.get("authorized_by", "unknown")
        print(f"  [{date}] {target}")
        print(f"    Change: {change}")
        print(f"    Author: {author}")
        print()


# ─── CLI ──────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Keystone Brand Constitution Guardian v1.0")
    parser.add_argument("--check", action="store_true", help="Verify integrity of brand files")
    parser.add_argument("--lock", action="store_true", help="Lock current state as baseline")
    parser.add_argument("--update", help="Target to update (voice/visual/direction/avatar/etc)")
    parser.add_argument("--change", help="Description of the change being made")
    parser.add_argument("--history", action="store_true", help="Show evolution history")
    args = parser.parse_args()
    
    if args.check:
        check_integrity()
    elif args.lock:
        lock_brand()
    elif args.update:
        if not args.change:
            print("[Guardian] ERROR: --change description required with --update")
            sys.exit(1)
        authorized_update(args.update, args.change)
    elif args.history:
        show_history()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
