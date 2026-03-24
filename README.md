# NASA APoD Wallpaper Automator

![Python](https://img.shields.io/badge/python-3.1+-blue.svg)
![Platform](https://img.shields.io/badge/platform-windows-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A lightweight Python utility designed to automatically fetch the **NASA Astronomy Picture of the Day (APOD)** and set it as your Windows desktop wallpaper.

## 🌟 Features
* **Daily Updates:** Automatically grabs the latest space imagery from NASA's official API.
* **High-Resolution Support:** Prioritizes HD imagery (`hdurl`) with an automatic fallback to standard resolution if HD is unavailable.
* **Fail-safe:** It NASA launches a video as the APoD, it will not be set as Wallpaper, APoD will be ignored.
* **Silent Background Operation:** Runs as a `.pyw` process, meaning no console windows or pop-ups will interrupt your work.
* **Robust Path Handling:** Automatically ensures the destination folder exists, even in complex OneDrive or custom Windows setups.

## 🚀 Installation & Usage

### 1. Prerequisites
Ensure you have Python 3.x installed along with the `requests` library:
* pip install requests

### 2. Compilation to .exe
To use this as a standalone application without needing Python installed on the target machine, compile it using **PyInstaller**:

* pip install pyinstaller
* pyinstaller --noconsole --onefile app.pyw
* or
* python -m PyInstaller --noconsole --onefile app.pyw

*The compiled executable will be located in the `/dist` folder. Based on Python version, you will get x86 (32-bit) or x64 (64-bit) executable. 32-bit can run on 32-bit and on 64-bit OS aswell, 64-bit can run on 64-bit OS only!*

### 3. Setting up Auto-Start
To ensure your wallpaper updates every time you turn on your PC:
1. Press `Win + R` on your keyboard.
2. Type `shell:startup` and press Enter.
3. Move the compiled `.exe` (or a shortcut to it) into this folder.

## 🛠 Technical Details
* **API:** Uses the [NASA Planetary Inventory API](https://api.nasa.gov/).
* **Win32 Integration:** Utilizes `ctypes.windll.user32.SystemParametersInfoW` to communicate directly with the Windows API for instant wallpaper application without a system restart.
* **Storage:** Images are saved locally to your `Pictures` folder as `nasa_apod_wallpaper.jpg`.

## 📄 License
This project is open-source and available under the MIT License.

---
*Created by Martin Chlebovec*
