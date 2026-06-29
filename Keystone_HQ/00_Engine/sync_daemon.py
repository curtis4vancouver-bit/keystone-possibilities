import os
import sys
import time
import logging
from google.cloud import storage
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configure logging
LOG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "scratch", "sync_daemon.log"))
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

# Configuration
WATCH_DIR = os.path.abspath(os.path.dirname(__file__))
BUCKET_NAME = "semiotic-ion-458504-e9-brand-brain-bucket"
KEY_PATH = os.path.join(WATCH_DIR, "scratch", "gcs_key.json")

# Ensure key exists
if not os.path.exists(KEY_PATH):
    logging.error(f"Service account key not found at {KEY_PATH}. Sync daemon exiting.")
    sys.exit(1)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KEY_PATH

# Ignore rules
IGNORE_DIRS = {".git", "__pycache__", ".system_generated", ".tempmediaStorage", "scratch", "node_modules", ".next", "dist", ".vercel", "build", ".cache", "venv", ".venv", ".learnings"}
IGNORE_EXTENSIONS = {".tmp", ".swp", ".log", ".mov", ".mp4", ".avi", ".mkv", ".mp3", ".wav", ".zip", ".tar", ".gz", ".dmg", ".exe", ".pkg"}
IGNORE_PREFIXES = (".", "~$", "ag-stop-probe")

def should_ignore(path):
    # Get path relative to WATCH_DIR
    rel_path = os.path.relpath(path, WATCH_DIR)
    parts = rel_path.split(os.sep)
    
    # Ignore if any parent directory is in the IGNORE_DIRS set
    for part in parts[:-1]:
        if part in IGNORE_DIRS:
            return True
            
    # Check if the actual file/folder itself is ignored
    name = parts[-1]
    if name in IGNORE_DIRS:
        return True
        
    if os.path.isfile(path):
        if name.startswith(IGNORE_PREFIXES):
            return True
        _, ext = os.path.splitext(name)
        if ext.lower() in IGNORE_EXTENSIONS:
            return True
            
    return False

# Initialize GCS client
try:
    gcs_client = storage.Client()
    bucket = gcs_client.bucket(BUCKET_NAME)
    logging.info("GCS storage client initialized successfully.")
except Exception as e:
    logging.error(f"Failed to initialize GCS storage client: {e}")
    sys.exit(1)

GCS_ENABLED = True

def upload_file(local_path):
    global GCS_ENABLED
    if not GCS_ENABLED:
        return
    if should_ignore(local_path):
        return
    
    rel_path = os.path.relpath(local_path, WATCH_DIR)
    # Standardize path separators for GCS
    gcs_blob_name = rel_path.replace(os.sep, "/")
    
    # Simple retry mechanism for network stability
    for attempt in range(3):
        try:
            blob = bucket.blob(gcs_blob_name)
            blob.upload_from_filename(local_path)
            logging.info(f"SUCCESS: Uploaded '{rel_path}' to GCS as '{gcs_blob_name}'")
            return
        except Exception as e:
            if "403" in str(e) or "denied" in str(e).lower() or "forbidden" in str(e).lower():
                logging.error(
                    f"\n======================================================================\n"
                    f"GCS PERMISSION ERROR DETECTED (403 Forbidden)\n"
                    f"The service account lacks GCS bucket permissions on '{BUCKET_NAME}'.\n"
                    f"To fix this, run this command in your local gcloud terminal:\n\n"
                    f"  gcloud projects add-iam-policy-binding semiotic-ion-458504-e9 \\\n"
                    f"    --member=\"serviceAccount:vertex-express@semiotic-ion-458504-e9.iam.gserviceaccount.com\" \\\n"
                    f"    --role=\"roles/storage.admin\"\n\n"
                    f"Disabling GCS synchronization observers to prevent log flooding.\n"
                    f"======================================================================\n"
                )
                GCS_ENABLED = False
                return
            logging.warning(f"Attempt {attempt+1} failed uploading {rel_path}: {e}")
            time.sleep(2 ** attempt)
            
    logging.error(f"FAILURE: Failed to upload '{rel_path}' after 3 attempts.")

def delete_file(local_path):
    global GCS_ENABLED
    if not GCS_ENABLED:
        return
    # Even if ignored locally, standardise rel_path and try deleting in case ignore list changed
    rel_path = os.path.relpath(local_path, WATCH_DIR)
    gcs_blob_name = rel_path.replace(os.sep, "/")
    
    for attempt in range(3):
        try:
            blob = bucket.blob(gcs_blob_name)
            if blob.exists():
                blob.delete()
                logging.info(f"SUCCESS: Deleted GCS object '{gcs_blob_name}'")
            else:
                logging.info(f"GCS object '{gcs_blob_name}' already deleted or does not exist.")
            return
        except Exception as e:
            if "403" in str(e) or "denied" in str(e).lower() or "forbidden" in str(e).lower():
                logging.error("GCS Permission error during delete. Disabling GCS sync.")
                GCS_ENABLED = False
                return
            logging.warning(f"Attempt {attempt+1} failed deleting {gcs_blob_name}: {e}")
            time.sleep(2 ** attempt)
            
    logging.error(f"FAILURE: Failed to delete '{gcs_blob_name}' after 3 attempts.")

def delete_directory(local_dir_path):
    global GCS_ENABLED
    if not GCS_ENABLED:
        return
    rel_path = os.path.relpath(local_dir_path, WATCH_DIR)
    prefix = rel_path.replace(os.sep, "/") + "/"
    
    try:
        blobs = list(bucket.list_blobs(prefix=prefix))
        if blobs:
            logging.info(f"Deleting GCS prefix '{prefix}' ({len(blobs)} objects)...")
            bucket.delete_blobs(blobs)
            logging.info(f"SUCCESS: Deleted prefix '{prefix}' from GCS.")
        else:
            logging.info(f"No GCS objects found with prefix '{prefix}'.")
    except Exception as e:
        if "403" in str(e) or "denied" in str(e).lower() or "forbidden" in str(e).lower():
            logging.error("GCS Permission error during directory delete. Disabling GCS sync.")
            GCS_ENABLED = False
            return
        logging.error(f"Failed to delete GCS prefix '{prefix}': {e}")

class MasterBrainSyncHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            logging.info(f"Detected creation: {event.src_path}")
            upload_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            logging.info(f"Detected modification: {event.src_path}")
            upload_file(event.src_path)

    def on_deleted(self, event):
        logging.info(f"Detected deletion: {event.src_path}")
        if event.is_directory:
            delete_directory(event.src_path)
        else:
            delete_file(event.src_path)

    def on_moved(self, event):
        logging.info(f"Detected move from {event.src_path} to {event.dest_path}")
        if event.is_directory:
            delete_directory(event.src_path)
            # Recursively upload the new directory structure
            for root, _, files in os.walk(event.dest_path):
                for f in files:
                    full_p = os.path.join(root, f)
                    upload_file(full_p)
        else:
            delete_file(event.src_path)
            upload_file(event.dest_path)

def run_full_sync():
    global GCS_ENABLED
    if not GCS_ENABLED:
        return
    logging.info("Starting initial full synchronization scan...")
    local_files = {}
    
    # 1. Catalog local files
    for root, _, files in os.walk(WATCH_DIR):
        for f in files:
            full_path = os.path.join(root, f)
            if not should_ignore(full_path):
                rel_path = os.path.relpath(full_path, WATCH_DIR)
                gcs_name = rel_path.replace(os.sep, "/")
                local_files[gcs_name] = full_path

    # 2. Upload any local files that are missing or modified in GCS
    try:
        gcs_blobs = list(bucket.list_blobs())
        gcs_files = {b.name: b for b in gcs_blobs}
        
        logging.info(f"Found {len(local_files)} local files to track and {len(gcs_files)} files in GCS.")
        
        for gcs_name, local_path in local_files.items():
            if gcs_name not in gcs_files:
                logging.info(f"Initial sync: upload missing GCS object '{gcs_name}'")
                upload_file(local_path)
            else:
                # Compare mod times or sizes to decide if we need to sync
                gcs_blob = gcs_files[gcs_name]
                local_mtime = os.path.getmtime(local_path)
                # GCS updated time is in UTC datetime, convert local mtime to UTC or just use file sizes & simple sync
                # We can do simple check: if size is different or local file is newer than GCS updated time
                # To keep it robust, let's upload if sizes differ, or if local is newer than the GCS blob updated time
                gcs_updated = gcs_blob.updated.timestamp()
                if local_path.endswith('.json') or os.path.getsize(local_path) != gcs_blob.size or local_mtime > gcs_updated:
                    logging.info(f"Initial sync: upload modified '{gcs_name}' (size/mtime mismatch)")
                    upload_file(local_path)

        # 3. Clean up GCS objects that no longer exist locally
        for gcs_name, gcs_blob in gcs_files.items():
            # Ensure we do not delete objects in GCS that are in our ignore folders
            # relative paths inside ignored dirs will not be in local_files, so we must make sure we do not delete them if they exist in GCS
            parts = gcs_name.split("/")
            is_ignored = False
            for part in parts[:-1]:
                if part in IGNORE_DIRS:
                    is_ignored = True
                    break
            if parts[-1] in IGNORE_DIRS:
                is_ignored = True
            if parts[-1].startswith(IGNORE_PREFIXES):
                is_ignored = True
                
            if not is_ignored and gcs_name not in local_files:
                logging.info(f"Initial sync: deleting orphaned GCS object '{gcs_name}'")
                gcs_blob.delete()
                
        logging.info("Initial full synchronization completed.")
    except Exception as e:
        if "403" in str(e) or "denied" in str(e).lower() or "forbidden" in str(e).lower():
            logging.error(
                f"\n======================================================================\n"
                f"GCS PERMISSION ERROR DETECTED DURING INITIAL SYNC (403 Forbidden)\n"
                f"The service account lacks GCS bucket permissions. Running in GCS-Disabled offline mode.\n"
                f"To fix this, run this command in your local gcloud terminal:\n\n"
                f"  gcloud projects add-iam-policy-binding semiotic-ion-458504-e9 \\\n"
                f"    --member=\"serviceAccount:vertex-express@semiotic-ion-458504-e9.iam.gserviceaccount.com\" \\\n"
                f"    --role=\"roles/storage.admin\"\n"
                f"======================================================================\n"
            )
            GCS_ENABLED = False
        else:
            logging.error(f"Error during initial sync: {e}")

if __name__ == "__main__":
    logging.info(f"Starting Brand Brain watchdog sync daemon on directory: {WATCH_DIR}")
    
    # Run full synchronization on startup
    run_full_sync()
    
    # Set up watchdog observer
    event_handler = MasterBrainSyncHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=True)
    observer.start()
    
    logging.info("Real-time filesystem observer started successfully. Standing by for events...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt received. Stopping observer...")
        observer.stop()
    observer.join()
    logging.info("Sync daemon stopped.")
