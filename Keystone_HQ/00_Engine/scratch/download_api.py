import os
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
import requests
import re

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

if __name__ == "__main__":
    cookies = get_cookies("google.com")
    print("Found", len(cookies), "cookies!")
    if "__Secure-1PSID" in cookies:
        print("Successfully found Google Auth Cookie!")
