import os
import sys
from google.cloud import storage

key_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "gcs_key.json"))
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

bucket_name = "semiotic-ion-458504-e9-brand-brain-bucket"
print(f"Uploading remote MCP deployment files to: gs://{bucket_name}/scratch/cloud_run_mcp/")

try:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    
    src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "cloud_run_mcp"))
    files = ["Dockerfile", "requirements.txt", "server.py"]
    
    for f in files:
        local_path = os.path.join(src_dir, f)
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Source file {local_path} not found.")
            
        gcs_name = f"scratch/cloud_run_mcp/{f}"
        blob = bucket.blob(gcs_name)
        blob.upload_from_filename(local_path)
        print(f"Uploaded {f} -> gs://{bucket_name}/{gcs_name}")
        
    print("SUCCESS: Uploaded all remote MCP deployment files successfully!")
    
except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)
