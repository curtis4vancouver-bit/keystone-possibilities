import sys

try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    print("SUCCESS: google-auth and google-api-python-client are installed!")
except ImportError as e:
    print(f"FAILED: {e}")
    sys.exit(1)
