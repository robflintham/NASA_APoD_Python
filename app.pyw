# Created by: Martin Chlebovec (martinius96@gmail.com)
# Script checks actual NASA APoD, sets image as Windows wallpaper
# Compatible with Windows 7, 8, 10, 11 (maybe Vista)

import requests
import ctypes
import os
import sys
import logging
import tempfile
import time

# API_KEY = "DEMO_KEY"          # Replaced with "get_api_from_file" function below
NASA_APOD_URL = "https://api.nasa.gov/planetary/apod"
PICTURES_DIR = os.path.join(os.path.expanduser("~"), "Pictures")
IMAGE_PATH = os.path.join(PICTURES_DIR, "nasa_apod_wallpaper.jpg")
logger = logging.getLogger(__name__)    

def get_api_from_file():
    """
    Looks for api.dat in the same folder as the executable. If this doesn't exist, falls
    back to the DEMO KEY with its associated (more limited) request limits. api.dat should
    be a plain text file containing the key string itself only.
    """
    # Check whether application is frozen or bring run from pyw file and set
    # application_path accordingly
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    logger.debug("Application path: {}".format(application_path))

    path_to_api = os.path.abspath(os.path.join(application_path,'api.dat'))
    logger.debug("Looking for API in \"{}\"".format(path_to_api))


    user_api = ""
    if os.path.exists(path_to_api):
        with open(path_to_api,'r') as f:
            user_api = f.readline().strip('\n')
        if not user_api == "":
            # Better checks here would be useful! This just looks for anything that
            # isn't a blank string.
            return user_api
        else:
            return "DEMO_KEY"
    
    else:
        # Fall back to demo key if no user API file is present
        return "DEMO_KEY"

def fetch_apod_url():
    # Get the API key from file if it exists
    api_key = get_api_from_file()

    logger.debug("API USED: {}".format(api_key))
    if api_key=="DEMO_KEY":
        logger.warning("No user API found, defaulting to DEMO_KEY")
    else:
        logger.info("Using user API key")

    # Use a while loop to retry on timeout - all other errors will just return None
    # with no retry. Uses an exponentially increasing delay on the retries.
    retry_initial_delay = 1
    max_retries = 10
    attempt = 0
    retry = True
    while retry and attempt < max_retries:
        attempt += 1
        retry = False
        if attempt > 1:
            delay = retry_initial_delay * (2**(attempt-2))
            logger.info("Retrying. Attempt #{}, waiting {} second(s)".format(int(attempt),int(delay)))
            time.sleep(delay)

        try:
            params = {"api_key": api_key}
            logger.info("Polling API for image URL")
            response = requests.get(NASA_APOD_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            logger.debug(data)
            
            # Check if media is an image; skip if it's a video or other type
            if data.get("media_type") == "image":
                logger.info("Media type is image")
                if "hdurl" in data.keys():
                    logger.info("HD URL: {}".format(data.get("hdurl")))
                else:
                    logger.warning("No HD URL detected, fallback to standard URL")
                    logger.info("Standard URL: {}".format(data.get("url")))
                # Return HD URL if available, otherwise fallback to standard URL
                return data.get("hdurl", data.get("url"))
            
            return None
        except requests.exceptions.ReadTimeout as e:
            logger.error("Request timed out")
            retry=True
        except Exception as e:
            logger.error(e)
            return None

def download_and_set_wallpaper():
    # Ensure Pictures directory exists
    if not os.path.exists(PICTURES_DIR):
        os.makedirs(PICTURES_DIR)

    image_url = fetch_apod_url()
    if not image_url:
        return
    
    # Use a while loop to retry on timeout - all other errors will just return None
    # with no retry. Uses an exponentially increasing delay on the retries.
    retry_initial_delay = 1
    max_retries = 10
    attempt = 0
    retry = True
    while retry and attempt < max_retries:
        attempt += 1
        retry = False
        if attempt > 1:
            delay = retry_initial_delay * (2**(attempt-2))
            logger.info("Retrying. Attempt #{}, waiting {} second(s)".format(int(attempt),int(delay)))
            time.sleep(delay)
        try:
            # Download image data
            logger.info("Retrieving image data")
            img_data = requests.get(image_url, timeout=20)
            img_data.raise_for_status()
            
            logger.info("Writing image data to file: {}".format(IMAGE_PATH))
            with open(IMAGE_PATH, "wb") as f:
                f.write(img_data.content)

        except requests.exceptions.ReadTimeout as e:
            logger.error("Request timed out")
            retry=True
        except Exception as e:
            logger.error(e)
            pass
            
    # Apply wallpaper using Win32 API
    # 20: SPI_SETDESKWALLPAPER, 3: Update registry and notify system
    logger.info("Setting desktop wallpaper via SPI_SETDESKWALLPAPER")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, IMAGE_PATH, 3)



if __name__ == "__main__":
    # Set logging level
    if "--debug" in sys.argv:
        loglevel=logging.DEBUG
    else:
        loglevel=logging.INFO
    
    # Create path in temp directorty for log file and clear previous logs
    logpath = os.path.join(tempfile.gettempdir(),'NASA_APoD_Wallpaper.log')
    if os.path.exists(logpath):
        os.remove(logpath)
    
    # Set up logging using Python's logging module
    logging.basicConfig(filename=logpath,
                        format='%(asctime)s - %(levelname)s - %(message)s', 
                        level=loglevel)
    
    # Run the main function
    logger.info("------- PROGRAM STARTED -------")
    download_and_set_wallpaper()
    logger.info("------- PROGRAM COMPLETE -------")
