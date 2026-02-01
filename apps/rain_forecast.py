import os
import requests
import datetime
from dotenv import load_dotenv

load_dotenv()

LAT = os.getenv("LAT", "52.38475")
LON = os.getenv("LON", "5.27685")

def get_rain_data():
    """Fetch rain data from Buienradar."""
    url = f"https://gpsgadget.buienradar.nl/data/raintext?lat={LAT}&lon={LON}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching Buienradar data: {e}")
        return None

def parse_rain_data(data):
    """Parse Buienradar raintext format (PPP|HH:mm)."""
    if not data:
        return None
        
    lines = data.strip().split("\n")
    for line in lines:
        if "|" in line:
            ppp_str, time_str = line.split("|")
            try:
                ppp = int(ppp_str)
                if ppp > 0:
                    return ppp, time_str
            except ValueError:
                continue
    return 0, None

def run():
    """Main entry point for the Rain Forecast app."""
    raw_data = get_rain_data()
    ppp, rain_time = parse_rain_data(raw_data)
    
    if ppp > 0:
        # Heaviness mapping
        if ppp < 110:
            icon_id = 63076 # Light
        elif ppp < 140:
            icon_id = 63077 # Medium
        else:
            icon_id = 63078 # Heavy
            
        payload = {
            "name": "rain_forecast",
            "text": rain_time,
            "icon": icon_id
        }
    else:
        payload = {
            "name": "rain_forecast",
            "text": "DRY",
            "icon": 65260
        }
        
    return payload

if __name__ == "__main__":
    # Test locally
    print(run())
