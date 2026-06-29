import os
import json
import time
from datetime import datetime, timedelta
import webbrowser

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/fitness.activity.read',
    'https://www.googleapis.com/auth/fitness.heart_rate.read',
    'https://www.googleapis.com/auth/fitness.sleep.read',
    'https://www.googleapis.com/auth/fitness.body.read'
]

CREDENTIALS_FILE = 'google_health_oauth_client_secret.json'
TOKEN_FILE = 'google_health_token.json'

def authenticate():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            
            # Monkeypatch webbrowser to print the URL for manual auth in the headless browser
            original_open = webbrowser.open
            def custom_open(url, new=0, autoraise=True):
                print(f"Please visit this URL to authorize this application: {url}")
                return original_open(url, new, autoraise)
            webbrowser.open = custom_open
            
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return creds

def get_recent_steps(service):
    # End time is now, start time is 7 days ago
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=7)
    
    # Convert to milliseconds
    end_time_ms = int(time.mktime(end_time.timetuple()) * 1000)
    start_time_ms = int(time.mktime(start_time.timetuple()) * 1000)

    request_body = {
        "aggregateBy": [{
            "dataTypeName": "com.google.step_count.delta"
        }],
        "bucketByTime": { "durationMillis": 86400000 },
        "startTimeMillis": start_time_ms,
        "endTimeMillis": end_time_ms
    }

    print("Fetching aggregated step data for the last 7 days...")
    response = service.users().dataset().aggregate(userId='me', body=request_body).execute()
    
    buckets = response.get('bucket', [])
    found_data = False
    
    for bucket in buckets:
        dataset = bucket.get('dataset', [])
        for ds in dataset:
            points = ds.get('point', [])
            for point in points:
                value = point.get('value', [])
                if value and 'intVal' in value[0]:
                    steps = value[0]['intVal']
                    print(f"Found steps: {steps}")
                    found_data = True
                    
    if not found_data:
        print("No aggregated step data found. The API call succeeded, but the database is empty.")
    else:
        print("Success! Data pulled from Google Fit.")

def main():
    try:
        creds = authenticate()
        print("\n[SUCCESS] Authentication successful!")
        
        service = build('fitness', 'v1', credentials=creds)
        get_recent_steps(service)
        
    except Exception as e:
        print(f"\n[ERROR] An error occurred: {e}")

if __name__ == '__main__':
    main()
