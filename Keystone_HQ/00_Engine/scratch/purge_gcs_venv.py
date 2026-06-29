import os
import sys
from google.cloud import storage

key_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "gcs_key.json"))
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

bucket_name = "semiotic-ion-458504-e9-brand-brain-bucket"
print(f"Purging venv/ and .venv/ files from GCS bucket: {bucket_name}")

try:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blobs = list(bucket.list_blobs())
    
    to_delete = []
    for blob in blobs:
        parts = blob.name.split("/")
        # Check if venv or .venv is in the parts
        if "venv" in parts or ".venv" in parts:
            to_delete.append(blob)
            
    print(f"Found {len(to_delete)} files in venv/ or .venv/ to delete.")
    
    if to_delete:
        # Delete blobs in batches
        print("Starting deletion...")
        # delete_blobs is efficient
        bucket.delete_blobs(to_delete)
        print("SUCCESS: Deleted all venv and .venv blobs from GCS!")
    else:
        print("No venv or .venv blobs found in GCS.")
        
except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)
