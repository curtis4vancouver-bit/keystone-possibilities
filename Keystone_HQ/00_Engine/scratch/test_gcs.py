import os
import sys
from google.cloud import storage

# Ensure path is absolute and set environment variable
key_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "gcs_key.json"))
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

print(f"Using service account key: {key_path}")

try:
    client = storage.Client()
    print("SUCCESS: Authenticated storage client.")
    
    print("Skipping list_buckets to directly test bucket object actions...")
        
    bucket_name = "semiotic-ion-458504-e9-brand-brain-bucket"
    bucket = client.bucket(bucket_name)
    blob = bucket.blob("test_connection.txt")
    blob.upload_from_string("GCS connection successfully verified from Keystone HQ local daemon!")
    print(f"SUCCESS: Uploaded test object to bucket: {bucket_name}")
    
    # Try reading it back
    content = blob.download_as_text()
    print(f"SUCCESS: Read back test object content: {content}")
    
    # Clean up test object
    blob.delete()
    print("SUCCESS: Cleaned up test object.")
    
except Exception as e:
    print(f"ERROR: {str(e)}", file=sys.stderr)
    sys.exit(1)
