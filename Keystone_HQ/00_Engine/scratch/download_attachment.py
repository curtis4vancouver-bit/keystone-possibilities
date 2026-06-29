import json
import urllib.request
import urllib.parse
import os
import base64

CREDENTIALS_PATH = r"C:\Users\Curtis\.google_workspace_mcp\credentials\curtis4vancouver@gmail.com.json"
OUTPUT_PDF = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scratch\CURTIS_Resume_old.pdf"

# Message and attachment info
MESSAGE_ID = "19e48d18665a2679"
ATTACHMENT_ID = "ANGjdJ_yYi3b33SiGl7jXwEvyIOvYCbuAkCZrzPHxyJQPJ2QmIQfiqPa7B0rvCdgfvCoC79ybXIJjRgsEYkGvErtvJ8Y9mhLGrDXrSTedOh73GSk1ASqtuK9zCFTTmzBbgE7M3KL6RpzD_kJfC6H4x77BC5Qt1L1LMNR9DoOZrjhinyVE0h_dqkmU5XGEX9Ua5TcjkrZOvOQo7kij03eU7wCD_zsDP2Aa4Z784z0joATZ99Uxn86gUPFdg28MtTUaFoxVpEokL8ecRTaRYEbvz6jV8Grp0EbKp6bUXm5yjRezjr-nROSX2_-yo73A5A"

def refresh_token(creds):
    data = urllib.parse.urlencode({
        "client_id": creds["client_id"],
        "client_secret": creds["client_secret"],
        "refresh_token": creds["refresh_token"],
        "grant_type": "refresh_token"
    }).encode("utf-8")
    
    req = urllib.request.Request(
        creds["token_uri"],
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read().decode("utf-8"))
        access_token = res_data["access_token"]
        creds["token"] = access_token
        with open(CREDENTIALS_PATH, "w", encoding="utf-8") as f:
            json.dump(creds, f, indent=2)
        return access_token

def main():
    with open(CREDENTIALS_PATH, "r", encoding="utf-8") as f:
        creds = json.load(f)
        
    access_token = refresh_token(creds)
    
    url = f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{MESSAGE_ID}/attachments/{ATTACHMENT_ID}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {access_token}")
    req.add_header("Accept", "application/json")
    
    print("Downloading attachment from Gmail API...")
    with urllib.request.urlopen(req) as response:
        att_data = json.loads(response.read().decode("utf-8"))
        
    data_b64 = att_data["data"]
    # Decode base64url to bytes
    pdf_bytes = base64.urlsafe_b64decode(data_b64.encode("UTF-8"))
    
    with open(OUTPUT_PDF, "wb") as f:
        f.write(pdf_bytes)
        
    print(f"Successfully downloaded attachment to {OUTPUT_PDF}!")

if __name__ == "__main__":
    main()
