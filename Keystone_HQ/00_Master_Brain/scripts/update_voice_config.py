import os
import json
import sys

def main():
    config_path = os.path.join(
        os.path.expanduser("~"), ".gemini", "antigravity", "voice_bridge_config.json"
    )
    
    ls_address = os.environ.get("ANTIGRAVITY_LS_ADDRESS")
    csrf_token = os.environ.get("ANTIGRAVITY_CSRF_TOKEN")
    project_id = os.environ.get("ANTIGRAVITY_PROJECT_ID")
    
    conversation_id = None
    step_index = 0
    source_metadata_str = os.environ.get("ANTIGRAVITY_SOURCE_METADATA")
    if source_metadata_str:
        try:
            meta = json.loads(source_metadata_str)
            conversation_id = meta.get("tool", {}).get("conversationId")
            step_index = meta.get("tool", {}).get("stepIndex", 0)
        except Exception:
            pass
            
    if not conversation_id:
        print("[Voice Config] Could not parse Conversation ID from env.")
        sys.exit(0)
        
    if ls_address and csrf_token:
        config = {}
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    config = json.load(f)
            except Exception:
                config = {}
                
        # Always update conversation_id to match the current executing IDE conversation
        # so AIDA 2.0 stays in sync with this open chat.
        config["conversation_id"] = conversation_id
            
        config["ls_address"] = ls_address
        config["csrf_token"] = csrf_token
        if project_id:
            config["project_id"] = project_id
            
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)

            
        print(f"[Voice Config] Auto-updated configurations:")
        print(f"  Conversation: {conversation_id}")
        print(f"  LS Address:   {ls_address}")
        print(f"  CSRF Token:   {csrf_token}")
    else:
        print("[Voice Config] Required environment variables (LS_ADDRESS, CSRF_TOKEN) are missing.")

if __name__ == "__main__":
    main()
