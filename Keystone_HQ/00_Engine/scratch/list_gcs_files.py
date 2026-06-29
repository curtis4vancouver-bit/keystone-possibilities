import os
import sys
from google.cloud import storage

key_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "gcs_key.json"))
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

bucket_name = "semiotic-ion-458504-e9-brand-brain-bucket"
print(f"Listing all files in GCS bucket: {bucket_name}...\n")

try:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blobs = list(bucket.list_blobs())
    
    print(f"Total files in cloud bucket: {len(blobs)}")
    print("-" * 50)
    for blob in blobs[:40]: # show first 40 files
        print(f"- {blob.name} ({blob.size} bytes)")
    if len(blobs) > 40:
        print(f"... and {len(blobs) - 40} more files.")
except Exception as e:
    print(f"ERROR: {str(e)}", file=sys.stderr)
    sys.exit(1)
