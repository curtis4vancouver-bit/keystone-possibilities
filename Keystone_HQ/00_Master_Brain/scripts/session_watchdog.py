#!/usr/bin/env python3
"""
Keystone OS Agent — Session Watchdog & Auto-Renamer
====================================================
Background daemon that:
  1. Monitors ~/.gemini/antigravity/conversations/ for new .db files (watchdog)
  2. Extracts the UUID from the filename
  3. Auto-labels the session in the annotations .pbtxt file
  4. Logs all intercepted sessions to a local registry

Usage:
    python session_watchdog.py                  # Run in foreground
    python session_watchdog.py --daemon         # Run as background process
    python session_watchdog.py --label "My Label" --uuid <UUID>  # Manual rename

Requirements:
    pip install watchdog
"""

import os
import sys
import re
import time
import json
import signal
import logging
import argparse
from pathlib import Path
from datetime import datetime, timezone

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("ERROR: watchdog not installed. Run: pip install watchdog")
    sys.exit(1)


# ── Paths ──────────────────────────────────────────────────────────────────
ANTIGRAVITY_ROOT = Path.home() / ".gemini" / "antigravity"
CONVERSATIONS_DIR = ANTIGRAVITY_ROOT / "conversations"
ANNOTATIONS_DIR = ANTIGRAVITY_ROOT / "annotations"
BRAIN_DIR = ANTIGRAVITY_ROOT / "brain"
REGISTRY_FILE = ANTIGRAVITY_ROOT / "session_registry.json"

# ── Logging ────────────────────────────────────────────────────────────────
LOG_FILE = ANTIGRAVITY_ROOT / "session_watchdog.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("SessionWatchdog")


# ── Registry ───────────────────────────────────────────────────────────────
def load_registry() -> dict:
    """Load the session registry from disk."""
    if REGISTRY_FILE.exists():
        try:
            return json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            log.warning("Registry file corrupted, starting fresh.")
    return {"sessions": {}, "created": datetime.now(timezone.utc).isoformat()}


def save_registry(registry: dict):
    """Persist the session registry to disk."""
    registry["last_updated"] = datetime.now(timezone.utc).isoformat()
    REGISTRY_FILE.write_text(
        json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def register_session(uuid: str, label: str, source: str = "watchdog"):
    """Add a session to the registry."""
    registry = load_registry()
    registry["sessions"][uuid] = {
        "label": label,
        "detected_at": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "renamed": False,
    }
    save_registry(registry)
    log.info(f"Registered session: {uuid} → '{label}'")


# ── Annotation Writer ──────────────────────────────────────────────────────
def read_current_title(uuid: str) -> str | None:
    """Read the current title from a .pbtxt annotation file."""
    pbtxt_path = ANNOTATIONS_DIR / f"{uuid}.pbtxt"
    if not pbtxt_path.exists():
        return None
    content = pbtxt_path.read_text(encoding="utf-8")
    match = re.search(r'title:"([^"]*)"', content)
    return match.group(1) if match else None


def rename_session(uuid: str, new_title: str) -> bool:
    """
    Rename a session by updating its .pbtxt annotation file.
    This is the file-based path — changes persist but require
    an app reload to reflect in the UI sidebar.
    """
    pbtxt_path = ANNOTATIONS_DIR / f"{uuid}.pbtxt"

    if not pbtxt_path.exists():
        # Create new annotation file
        now_seconds = int(time.time())
        content = f'title:"{new_title}"  last_user_view_time:{{seconds:{now_seconds}  nanos:0}}'
        pbtxt_path.write_text(content, encoding="utf-8")
        log.info(f"Created annotation for {uuid}: '{new_title}'")
        return True

    # Update existing annotation
    content = pbtxt_path.read_text(encoding="utf-8")
    old_title = read_current_title(uuid)

    if old_title == new_title:
        log.info(f"Session {uuid} already has title '{new_title}', skipping.")
        return False

    # Replace the title field
    new_content = re.sub(r'title:"[^"]*"', f'title:"{new_title}"', content)
    pbtxt_path.write_text(new_content, encoding="utf-8")
    log.info(f"Renamed session {uuid}: '{old_title}' → '{new_title}'")

    # Update registry
    registry = load_registry()
    if uuid in registry["sessions"]:
        registry["sessions"][uuid]["renamed"] = True
        registry["sessions"][uuid]["label"] = new_title
        save_registry(registry)

    return True


# ── Auto-Label Logic ───────────────────────────────────────────────────────
def detect_workspace(uuid: str) -> str | None:
    """
    Attempt to detect which workspace a session belongs to
    by checking if a brain directory exists with workspace clues.
    """
    brain_path = BRAIN_DIR / uuid
    if not brain_path.exists():
        return None

    # Check for .system_generated logs for workspace hints
    logs_dir = brain_path / ".system_generated" / "logs"
    if logs_dir.exists():
        # Look at transcript for workspace path
        transcript = logs_dir / "transcript.jsonl"
        if transcript.exists():
            try:
                first_line = transcript.open(encoding="utf-8").readline()
                if "Master_Brain" in first_line:
                    return "Master Brain"
                elif "construction-website" in first_line:
                    return "Keystone HQ"
            except (OSError, UnicodeDecodeError):
                pass

    return None


def generate_auto_label(uuid: str) -> str:
    """Generate an automatic label for a newly detected session."""
    workspace = detect_workspace(uuid)
    timestamp = datetime.now().strftime("%b %d %I:%M%p")

    if workspace:
        return f"⚡ {workspace} — {timestamp}"
    else:
        return f"⚡ Session — {timestamp}"


# ── Watchdog Event Handler ─────────────────────────────────────────────────
class SessionEventHandler(FileSystemEventHandler):
    """Monitors the conversations directory for new session files."""

    UUID_PATTERN = re.compile(
        r"^([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\.db$"
    )

    def __init__(self, auto_label: bool = True):
        super().__init__()
        self.auto_label = auto_label
        self.known_sessions = set()
        self._scan_existing()

    def _scan_existing(self):
        """Scan for existing sessions on startup."""
        if CONVERSATIONS_DIR.exists():
            for f in CONVERSATIONS_DIR.iterdir():
                match = self.UUID_PATTERN.match(f.name)
                if match:
                    self.known_sessions.add(match.group(1))
            log.info(
                f"Loaded {len(self.known_sessions)} existing sessions from disk."
            )

    def on_created(self, event):
        """Called when a new file is created in the conversations directory."""
        if event.is_directory:
            return

        filename = Path(event.src_path).name
        match = self.UUID_PATTERN.match(filename)
        if not match:
            return

        uuid = match.group(1)

        if uuid in self.known_sessions:
            return  # Already tracked

        self.known_sessions.add(uuid)
        log.info(f"[NEW] SESSION DETECTED: {uuid}")

        # Register it
        label = generate_auto_label(uuid)
        register_session(uuid, label)

        # Auto-label if enabled
        if self.auto_label:
            # Wait briefly for the annotation file to be created by the app
            time.sleep(2)
            rename_session(uuid, label)

    def on_modified(self, event):
        """Track modifications to existing sessions (activity tracking)."""
        if event.is_directory:
            return

        filename = Path(event.src_path).name
        match = self.UUID_PATTERN.match(filename)
        if not match:
            return

        uuid = match.group(1)
        if uuid not in self.known_sessions:
            self.known_sessions.add(uuid)
            log.info(f"[NEW] DETECTED ACTIVE SESSION (via modify): {uuid}")
            label = generate_auto_label(uuid)
            register_session(uuid, label, source="modify_event")


# ── Integrity Checker ──────────────────────────────────────────────────────
def run_integrity_check():
    """
    Cross-reference conversations on disk vs. annotations.
    Detect orphaned sessions (data exists but no annotation).
    """
    log.info("Running integrity check...")

    uuid_pattern = re.compile(
        r"^([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\.db$"
    )

    on_disk = set()
    for f in CONVERSATIONS_DIR.iterdir():
        match = uuid_pattern.match(f.name)
        if match:
            on_disk.add(match.group(1))

    annotated = set()
    for f in ANNOTATIONS_DIR.iterdir():
        if f.suffix == ".pbtxt":
            annotated.add(f.stem)

    orphaned = on_disk - annotated
    phantom = annotated - on_disk  # Annotations for deleted conversations

    log.info(f"Sessions on disk:   {len(on_disk)}")
    log.info(f"Annotated sessions: {len(annotated)}")
    log.info(f"Orphaned (no annotation): {len(orphaned)}")
    log.info(f"Phantom (no data file):   {len(phantom)}")

    if orphaned:
        log.warning("Orphaned sessions (may be invisible in UI):")
        for uuid in sorted(orphaned):
            log.warning(f"  [!] {uuid}")
            # Auto-create annotation
            label = generate_auto_label(uuid)
            rename_session(uuid, label)

    return {
        "on_disk": len(on_disk),
        "annotated": len(annotated),
        "orphaned": list(orphaned),
        "phantom": list(phantom),
    }


# ── Main ───────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Keystone Session Watchdog — Monitor & auto-label Antigravity sessions"
    )
    parser.add_argument(
        "--daemon", action="store_true", help="Run as background daemon"
    )
    parser.add_argument(
        "--label", type=str, help="Manually set a session label"
    )
    parser.add_argument(
        "--uuid", type=str, help="Target session UUID for manual operations"
    )
    parser.add_argument(
        "--check", action="store_true", help="Run integrity check and exit"
    )
    parser.add_argument(
        "--list", action="store_true", help="List all tracked sessions"
    )
    parser.add_argument(
        "--no-auto-label",
        action="store_true",
        help="Disable auto-labeling (monitor only)",
    )

    args = parser.parse_args()

    # Manual rename mode
    if args.label and args.uuid:
        rename_session(args.uuid, args.label)
        print(f"✅ Renamed {args.uuid} → '{args.label}'")
        return

    # Integrity check mode
    if args.check:
        result = run_integrity_check()
        print(json.dumps(result, indent=2))
        return

    # List mode
    if args.list:
        registry = load_registry()
        if not registry["sessions"]:
            print("No sessions tracked yet.")
            return
        print(f"\n{'UUID':<40} {'Label':<35} {'Detected At'}")
        print("─" * 100)
        for uuid, info in sorted(
            registry["sessions"].items(),
            key=lambda x: x[1].get("detected_at", ""),
            reverse=True,
        ):
            print(
                f"{uuid:<40} {info['label']:<35} {info.get('detected_at', 'N/A')}"
            )
        return

    # Ensure directories exist
    if not CONVERSATIONS_DIR.exists():
        log.error(f"Conversations directory not found: {CONVERSATIONS_DIR}")
        sys.exit(1)

    # Start watchdog
    log.info("=" * 60)
    log.info("Keystone Session Watchdog starting...")
    log.info(f"Monitoring: {CONVERSATIONS_DIR}")
    log.info(f"Annotations: {ANNOTATIONS_DIR}")
    log.info(f"Auto-label: {not args.no_auto_label}")
    log.info("=" * 60)

    # Run initial integrity check
    run_integrity_check()

    # Set up the observer
    handler = SessionEventHandler(auto_label=not args.no_auto_label)
    observer = Observer()
    observer.schedule(handler, str(CONVERSATIONS_DIR), recursive=False)
    observer.start()

    log.info("[OK] Watchdog active. Listening for new sessions...")

    # Graceful shutdown
    def shutdown(signum, frame):
        log.info("Shutting down watchdog...")
        observer.stop()
        observer.join()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        shutdown(None, None)


if __name__ == "__main__":
    main()
