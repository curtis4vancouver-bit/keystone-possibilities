import os
import sys
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

def test_token(path):
    print(f"\n--- Testing token file: {path} ---")
    if not os.path.exists(path):
        print("File does not exist.")
        return
        
    with open(path, "r") as f:
        creds_data = json.load(f)
        
    creds = Credentials(
        token=creds_data.get("token"),
        refresh_token=creds_data.get("refresh_token"),
        token_uri=creds_data.get("token_uri"),
        client_id=creds_data.get("client_id"),
        client_secret=creds_data.get("client_secret"),
        scopes=creds_data.get("scopes")
    )
    
    try:
        if creds.expired and creds.refresh_token:
            print("Token expired. Attempting refresh...")
            creds.refresh(Request())
            # Save refreshed token
            with open(path, "w") as token_f:
                token_f.write(creds.to_json())
            print("Token refreshed and saved successfully.")
        elif creds.expired:
            print("Token is expired but has NO refresh token!")
            
        youtube = build("youtube", "v3", credentials=creds)
        channels_response = youtube.channels().list(
            part="snippet,contentDetails",
            mine=True
        ).execute()
        
        if "items" in channels_response and len(channels_response["items"]) > 0:
            channel = channels_response["items"][0]
            print(f"Success!")
            print(f"Channel Title: {channel['snippet']['title']}")
            print(f"Channel ID: {channel['id']}")
            print(f"Custom Handle: {channel['snippet'].get('customUrl')}")
        else:
            print("No channels found for this token.")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    token_files = [
        "youtube_token.json",
        "youtube_token_oac.json",
        "youtube_token_possibilities.json",
        "youtube_token_protocols.json"
    ]
    for filename in token_files:
        test_token(filename)
