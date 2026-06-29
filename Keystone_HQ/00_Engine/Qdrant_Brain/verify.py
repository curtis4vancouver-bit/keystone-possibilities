import requests
try:
    res = requests.get("http://localhost:6333/collections")
    print(res.json())
except Exception as e:
    print(f"Error: {e}")
