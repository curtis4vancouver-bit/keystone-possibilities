import os
import sys
import json
from google.cloud import storage

key_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "gcs_key.json"))
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

bucket_name = "semiotic-ion-458504-e9-brand-brain-bucket"
print(f"Checking synchronization status for GCS bucket: {bucket_name}...")

try:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    
    files_to_check = [
        "MCP_Multiplexer/agents.json",
        "MCP_Multiplexer/cached_tools.json"
    ]
    
    for gcs_path in files_to_check:
        blob = bucket.blob(gcs_path)
        if not blob.exists():
            print(f"[-] WARNING: '{gcs_path}' DOES NOT EXIST in the cloud bucket!")
        else:
            print(f"[+] '{gcs_path}' exists in GCS.")
            
            # Fetch content and print the enabled agents status if checking agents.json
            if gcs_path.endswith("agents.json"):
                data = json.loads(blob.download_as_text())
                enabled_agents = [k for k, v in data.items() if v.get("enabled") is True]
                print(f"    - Enabled agents in GCS config: {enabled_agents}")
            elif gcs_path.endswith("cached_tools.json"):
                data = json.loads(blob.download_as_text())
                total_tools = 0
                for agent_name, tools in data.items():
                    print(f"    - Agent '{agent_name}': {len(tools)} tools cached in GCS.")
                    total_tools += len(tools)
                print(f"    - Total sub-agent tools cached in GCS: {total_tools}")

except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)
