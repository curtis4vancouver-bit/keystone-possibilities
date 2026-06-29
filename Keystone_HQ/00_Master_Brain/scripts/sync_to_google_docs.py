import json
import os
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from config import SCRIPTS_DIR, logger

TOKEN_FILE = Path(r"C:\Users\Curtis\.google_workspace_mcp\credentials\curtis4vancouver@gmail.com.json")


def load_credentials():
    if not TOKEN_FILE.exists():
        logger.warning("Google Workspace credentials file not found: %s", TOKEN_FILE)
        return None
    try:
        with open(TOKEN_FILE, "r") as f:
            tok = json.load(f)
        return Credentials(
            token=tok.get("token") or tok.get("access_token"),
            refresh_token=tok.get("refresh_token"),
            token_uri="https://oauth2.googleapis.com/token",
            client_id=tok.get("client_id"),
            client_secret=tok.get("client_secret")
        )
    except Exception as e:
        logger.error("Error loading credentials: %s", e)
        return None


def append_to_google_doc(docs_service, document_id, text):
    try:
        # Get current document length to append at the end
        doc = docs_service.documents().get(documentId=document_id, fields="body/content").execute()
        content = doc.get("body", {}).get("content", [])
        end_index = content[-1].get("endIndex") - 1 if content else 1
        if end_index < 1:
            end_index = 1
        
        requests = [
            {
                'insertText': {
                    'location': {
                        'segmentId': '',
                        'index': end_index
                    },
                    'text': text
                }
            }
        ]
        docs_service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
        logger.info("Appended text to doc: %s", document_id)
        return True
    except Exception as e:
        logger.error("Error appending to doc %s: %s", document_id, e)
        return False


def sync():
    """Read ops file and execute updates on Google Docs."""
    ops_file = SCRIPTS_DIR / "_sync_operations.json"

    if not ops_file.exists():
        logger.info("No sync operations pending.")
        logger.info("Run 'sync_brain_to_drive.py' first to generate operations.")
        return

    try:
        ops = json.loads(ops_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        logger.error("Could not read ops file: %s", exc)
        return

    logger.info("Found %d sync operations in %s", len(ops), ops_file.name)
    if not ops:
        return

    creds = load_credentials()
    if not creds:
        logger.error("Cannot perform Google Doc sync without active credentials.")
        return

    try:
        docs_service = build("docs", "v1", credentials=creds)
    except Exception as e:
        logger.error("Failed to build Google Docs service: %s", e)
        return

    success_count = 0
    for i, op in enumerate(ops, 1):
        action = op.get("action", "unknown")
        doc_id = op.get("docId", "???")
        text = op.get("text", "")
        
        text_preview = str(text)[:80].replace("\n", " ")
        logger.info("  [%d] Executing: %s -> doc:%s... | %s...", i, action, doc_id[:20], text_preview)
        
        if action == "appendToGoogleDoc":
            if append_to_google_doc(docs_service, doc_id, text):
                success_count += 1
        else:
            logger.warning("Unsupported action: %s", action)
            
    logger.info("Completed %d of %d sync operations successfully.", success_count, len(ops))


if __name__ == "__main__":
    sync()
