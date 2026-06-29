import os
import sys
import json
import logging
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
os.chdir(PARENT_DIR)
sys.path.insert(0, PARENT_DIR)

from social_publisher import SocialPublisher

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    publisher = SocialPublisher()
    tokens = publisher.tokens
    
    # Check possibilities meta token
    token_info = tokens.get("possibilities", {}).get("meta", {})
    user_access_token = token_info.get("user_access_token")
    
    if not user_access_token:
        logger.error("No Meta user_access_token found under 'possibilities'.")
        return
        
    logger.info("Querying Meta Graph API for connected pages...")
    pages_url = f"https://graph.facebook.com/v20.0/me/accounts?access_token={user_access_token}"
    
    try:
        req = urllib.request.Request(pages_url)
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode("utf-8"))
            pages = data.get("data", [])
            logger.info(f"Successfully retrieved {len(pages)} Facebook pages:")
            for idx, page in enumerate(pages, 1):
                name = page.get("name")
                page_id = page.get("id")
                logger.info(f"Page {idx}: '{name}' (ID: {page_id})")
                
                # Check for connected Instagram accounts
                try:
                    page_token = page["access_token"]
                    ig_url = f"https://graph.facebook.com/v20.0/{page_id}?fields=instagram_business_account&access_token={page_token}"
                    ig_req = urllib.request.Request(ig_url)
                    with urllib.request.urlopen(ig_req) as ig_res:
                        ig_data = json.loads(ig_res.read().decode("utf-8"))
                        ig_account = ig_data.get("instagram_business_account")
                        if ig_account:
                            logger.info(f"  -> Linked Instagram Account ID: {ig_account.get('id')}")
                        else:
                            logger.info("  -> No linked Instagram Business Account.")
                except Exception as ig_err:
                    logger.warning(f"  -> Failed to check Instagram: {str(ig_err)}")
    except Exception as e:
        logger.error(f"Error calling Meta API: {str(e)}")

if __name__ == "__main__":
    main()
