# Created by: Martin Chlebovec (martinius96@gmail.com)
# Script checks actual NASA APoD, sets image as Windows wallpaper
# Compatible with Windows 7, 8, 10, 11 (maybe Vista)

import requests
import ctypes
import os

API_KEY = "DEMO_KEY"
NASA_APOD_URL = "https://api.nasa.gov/planetary/apod"
PICTURES_DIR = os.path.join(os.path.expanduser("~"), "Pictures")
IMAGE_PATH = os.path.join(PICTURES_DIR, "nasa_apod_wallpaper.jpg")

def fetch_apod_url():
    try:
        params = {"api_key": API_KEY}
        response = requests.get(NASA_APOD_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Check if media is an image; skip if it's a video or other type
        if data.get("media_type") == "image":
            # Return HD URL if available, otherwise fallback to standard URL
            return data.get("hdurl", data.get("url"))
        
        return None
    except:
        return None

def download_and_set_wallpaper():
    # Ensure Pictures directory exists
    if not os.path.exists(PICTURES_DIR):
        os.makedirs(PICTURES_DIR)

    image_url = fetch_apod_url()
    if not image_url:
        return

    try:
        # Download image data
        img_data = requests.get(image_url, timeout=20)
        img_data.raise_for_status()
        
        with open(IMAGE_PATH, "wb") as f:
            f.write(img_data.content)
        
        # Apply wallpaper using Win32 API
        # 20: SPI_SETDESKWALLPAPER, 3: Update registry and notify system
        ctypes.windll.user32.SystemParametersInfoW(20, 0, IMAGE_PATH, 3)
    except:
        pass

if __name__ == "__main__":
    download_and_set_wallpaper()
