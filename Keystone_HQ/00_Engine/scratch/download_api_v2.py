import os
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
import requests
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

def get_cookies(url_filter):
    key = get_encryption_key()
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "Default", "Network", "Cookies")
    filename = "Cookies_temp.db"
    try:
        shutil.copyfile(db_path, filename)
    except PermissionError:
        print("Cannot copy cookies, Chrome is locking the DB. Please kill Chrome.")
        return {}
    
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    cursor.execute(f"SELECT host_key, name, value, encrypted_value FROM cookies WHERE host_key like '%{url_filter}%'")
    
    cookies = {}
    for host_key, name, value, encrypted_value in cursor.fetchall():
        if not value:
            decrypted_value = decrypt_data(encrypted_value, key)
        else:
            decrypted_value = value
        cookies[name] = decrypted_value
        
    cursor.close()
    db.close()
    os.remove(filename)
    return cookies

def parse_prompts(md_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    prompts = {}
    pattern = re.compile(r'### CLIP A(\d+).*?```(.*?)```', re.DOTALL)
    for match in pattern.finditer(content):
        clip_num = int(match.group(1))
        prompt_text = " ".join(match.group(2).strip().splitlines())
        prompts[clip_num] = prompt_text
    return prompts

def get_clip_urls():
    cookies = get_cookies("google")
    print("Found Google cookies!")
    
    url = "https://labs.google/fx/tools/flow/project/827275bd-d7fa-422b-9c90-b67109344d47"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    
    print(f"Fetching {url}...")
    resp = requests.get(url, cookies=cookies, headers=headers)
    
    if "Sign in" in resp.text or resp.status_code != 200:
        print(f"Failed to authenticate. Status: {resp.status_code}")
        with open("error.html", "w", encoding="utf-8") as f:
            f.write(resp.text)
        return None
        
    soup = BeautifulSoup(resp.text, 'html.parser')
    next_data_script = soup.find('script', id='__NEXT_DATA__')
    if not next_data_script:
        print("Could not find __NEXT_DATA__ in HTML.")
        return None
        
    next_data = json.loads(next_data_script.string)
    
    # Locate the clips in the state
    try:
        dehydrated = next_data["props"]["pageProps"]["trpcState"]["json"]["queries"]
        for query in dehydrated:
            if query["queryKey"][0] == "project" and query["queryKey"][1] == "get":
                project_data = query["state"]["data"]
                return project_data["components"]
    except Exception as e:
        print("Error parsing state:", e)
        return None
        
    return None

def download_video(url, dest_path):
    print(f"Downloading {url} to {dest_path}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    cookies = get_cookies("google")
    r = requests.get(url, cookies=cookies, headers=headers, stream=True)
    if r.status_code == 200:
        with open(dest_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
        print("Download successful!")
        return True
    else:
        print(f"Failed to download: {r.status_code}")
        return False

if __name__ == "__main__":
    components = get_clip_urls()
    if components:
        print(f"Found {len(components)} components in the project!")
        for c in components:
            if "prompt" in c:
                print("Prompt:", c["prompt"]["text"][:50], "...")
                print("Media UUID:", c["media"]["name"])
    else:
        print("Failed to get components.")
