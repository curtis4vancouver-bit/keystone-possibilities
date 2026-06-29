import os
import json
import logging

logging.basicConfig(level=logging.INFO)

VECTOR_DB_PATH = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\local_vector_db\vector_memories.json"
MASTER_DOCS_DIR = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Master_Docs"

def clean_vector_brain():
    if os.path.exists(VECTOR_DB_PATH):
        # We write an empty array to reset the DB
        with open(VECTOR_DB_PATH, 'w', encoding='utf-8') as f:
            json.dump([], f)
        logging.info("Vector brain successfully cleared.")
    else:
        logging.info("Vector brain file not found, creating a new empty one.")
        os.makedirs(os.path.dirname(VECTOR_DB_PATH), exist_ok=True)
        with open(VECTOR_DB_PATH, 'w', encoding='utf-8') as f:
            json.dump([], f)

if __name__ == "__main__":
    clean_vector_brain()
    # Re-ingestion can be handled via the keystone-brain MCP tool later.
    logging.info("Cleanup complete. Ready for fresh ingestion.")
