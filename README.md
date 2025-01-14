# PulseGram
PulseGram is a keylogger integrated with a Telegram bot. It is a monitoring tool that captures keystrokes, clipboard content, and screenshots, sending all the information to a configured Telegram bot. It is designed for use in adversary simulations and security testing contexts.

> **⚠️ Warning:** This project is for educational purposes and security testing in authorized environments only. Unauthorized use of this tool may be illegal and is prohibited.


```
  _____       _           _____                     
 |  __ \     | |         / ____|                    
 | |__) |   _| |___  ___| |  __ _ __ __ _ _ __ ___  
 |  ___/ | | | / __|/ _ \ | |_ | '__/ _` | '_ ` _ \ 
 | |   | |_| | \__ \  __/ |__| | | | (_| | | | | | |
 |_|    \__,_|_|___/\___|\_____|_|  \__,_|_| |_| |_|
                                                                                                        
                 Author: Omar Salazar
                 Version: V.1.0
```


## Features

- **Keystroke capture:** Records keystrokes and sends them to the Telegram bot.
- **Clipboard monitoring:** Sends the copied clipboard content in real-time.
- **Periodic screenshots:** Takes screenshots and sends them to the bot.
- **Error logs:** Logs errors in an `errors_log.txt` file to facilitate debugging.


<p align="center">
  <img src="https://raw.githubusercontent.com/TaurusOmar/pulsegram/master/pulse.gif"/>
</p>

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/TaurusOmar/pulsegram
   cd pulsegram
   ```

2. Install dependencies: Make sure you have Python 3 and pip installed. Then run:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the Telegram bot token:
   Create a bot on Telegram using BotFather.
   Copy your token and paste it into the code in `main.py` where the bot is initialized.

4. Copy yout ChatID `chat_id="131933xxxx"` in `keylogger.py`


## Usage

Run the tool on the target machine with:

```bash
python pulsegram.py
```

## Modules

### pulsegram.py

This is the main file of the tool, which initializes the bot and launches asynchronous tasks to capture and send data.

`Bot(token="...")`: Initializes the Telegram bot with your personal token.<br>
`asyncio.gather(...)`: Launches multiple tasks to execute clipboard monitoring, screenshot capture, and keystroke logging.<br>
`log_error`: In case of errors, logs them in an errors_log.txt file.<br>

### helpers.py  
This module contains auxiliary functions that assist the overall operation of the tool.

`log_error()`: Logs any errors in errors_log.txt with a date and time format.  
`get_clipboard_content()`: Captures the current content of the clipboard.  
`capture_screenshot()`: Takes a screenshot and temporarily saves it to send it to the Telegram bot.


### keylogger.py
This module handles keylogging, clipboard monitoring, and screenshot captures.

`capture_keystrokes(bot)`: Asynchronous function that captures keystrokes and sends the information to the Telegram bot.  
`send_keystrokes_to_telegram(bot)`: This function sends the accumulated keystrokes to the bot.  
`capture_screenshots(bot)`: Periodically captures an image of the screen and sends it to the bot.  
`log_clipboard(bot)`: Sends the contents of the clipboard to the bot.


## Action Configurations

Change the capture and information sending time interval.

```python
async def send_keystrokes_to_telegram(bot):
    global keystroke_buffer
    while True:
        await asyncio.sleep(1)  # Change the key sending interval
```

```python
async def capture_screenshots(bot):
    while True:
        await asyncio.sleep(30)  # Change the screenshot capture interval
        try:
```

```python
async def log_clipboard(bot):
    previous_content = ""
    while True:
        await asyncio.sleep(5)  # Change the interval to check for clipboard changes
        current_content = get_clipboard_content()
```

### Security Warning

This project is for educational purposes only and for security testing in your own environments or with express authorization. Unauthorized use of this tool may violate local laws and privacy policies.

### Contributions

Contributions are welcome. Please ensure to respect the code of conduct when collaborating.

### License

This project is licensed under the MIT License.
