import os
import time
import requests
import importlib
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# Setup Logging
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_file = os.path.join(LOG_DIR, "app.log")

# Console Handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)

# File Handler
file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
file_handler.setFormatter(log_formatter)

logging.basicConfig(level=logging.INFO, handlers=[console_handler, file_handler])
logger = logging.getLogger("AwtrixDispatcher")

# Load environment variables
load_dotenv()

AWTRIX_IP = os.getenv("AWTRIX_IP")
UPDATE_INTERVAL = int(os.getenv("UPDATE_INTERVAL", 600))
APP_SWITCH_INTERVAL = int(os.getenv("APP_SWITCH_INTERVAL", 10))

def send_to_awtrix(payload):
    """Send JSON payload to AWTRIX 3 custom app endpoint."""
    if not AWTRIX_IP:
        logger.error("AWTRIX_IP not set.")
        return
        
    app_name = payload.get("name", "custom")
    url = f"http://{AWTRIX_IP}/api/custom?name={app_name}"
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        logger.info(f"Successfully sent {app_name} to AWTRIX: {response.status_code}")
    except Exception as e:
        logger.error(f"Error sending to AWTRIX: {e}")

def load_apps():
    """Dynamically load apps from the apps directory."""
    apps = []
    apps_dir = os.path.join(os.path.dirname(__file__), "apps")
    
    for filename in os.listdir(apps_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = f"apps.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, "run"):
                    apps.append(module)
                    logger.info(f"Loaded app: {module_name}")
            except Exception as e:
                logger.error(f"Failed to load {module_name}: {e}")
    return apps

def main():
    if not AWTRIX_IP:
        logger.error("AWTRIX_IP must be set in .env file.")
        return

    logger.info("Starting Standalone Pixel Display Dispatcher...")
    
    apps = load_apps()
    if not apps:
        logger.warning("No apps found in apps/ directory.")
        return

    while True:
        for app in apps:
            try:
                payload = app.run()
                if payload:
                    send_to_awtrix(payload)
                else:
                    logger.info(f"App {app.__name__} returned no data.")
            except Exception as e:
                logger.error(f"Error running app {app.__name__}: {e}")
            
            # Use configurable interval between apps
            time.sleep(APP_SWITCH_INTERVAL)
        
        # Wait for the longer update interval before the next cycle
        logger.info(f"Cycle complete. Waiting {UPDATE_INTERVAL}s for next update.")
        time.sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    main()
