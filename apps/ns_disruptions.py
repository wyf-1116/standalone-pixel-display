import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

# Configuration
NS_API_KEY = os.getenv("NS_API_KEY")
NS_STATION_CODE = os.getenv("NS_STATION_CODE", "ALMB") # Uppercase recommended

# Logger
logger = logging.getLogger("AwtrixDispatcher")

def get_disruptions():
    """Fetch disruptions from NS API using the latest endpoint."""
    if not NS_API_KEY or NS_API_KEY == "your_ns_api_key_here":
        logger.warning("NS_API_KEY is not configured.")
        return None

    # New endpoint: /disruptions/v3/station/{stationCode}
    url = f"https://gateway.apiportal.ns.nl/disruptions/v3/station/{NS_STATION_CODE}"
    headers = {"Ocp-Apim-Subscription-Key": NS_API_KEY}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching NS disruptions from {url}: {e}")
        return None

def run():
    """Main entry point for the NS Disruptions app."""
    # Default payload
    payload = {
        "name": "ns_disruptions",
        "icon": 58411
    }

    data = get_disruptions()
    
    if data is None:
        # Fallback or error state
        payload["text"] = "NS ERROR"
        payload["color"] = "#FF0000"
        return payload

    # The API returns a list of disruptions if successful
    # Based on docs: successfully returned a list of disruptions
    try:
        if isinstance(data, list):
            disruption_count = len(data)
        elif isinstance(data, dict) and "disruptions" in data:
            disruption_count = len(data["disruptions"])
        else:
            # Check if it's a single object or something else
            disruption_count = 0
    except:
        disruption_count = 0

    if disruption_count > 0:
        payload["text"] = f"{disruption_count} DSRP"
        payload["color"] = "#FF0000" # Red
    else:
        payload["text"] = "GOEDE REIS"
        payload["color"] = "#00FF00" # Green

    return payload

if __name__ == "__main__":
    # Test locally
    print(run())
