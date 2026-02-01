import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
CITY = os.getenv("CITY", "London")
COUNTRY_CODE = os.getenv("COUNTRY_CODE", "GB")

def get_weather():
    """Fetch weather data from OpenWeatherMap."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY},{COUNTRY_CODE}&appid={WEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return None

def get_weather_icon(condition_code):
    """
    Map OpenWeatherMap condition codes to specific LaMetric icon IDs.
    """
    icon_map = {
        "01": "17144", # Sun
        "02": "55711", # Partial Sun
        "03": "12246", # Cloud
        "04": "12246", # Cloud
        "09": "72",    # Rain
        "10": "72",    # Rain
        "11": "26337", # Lightning
        "13": "16434", # Snow
        "50": "12196", # Haze
    }
    prefix = condition_code[:2]
    return icon_map.get(prefix, "17144") # Default to Sun

def run():
    """Main entry point for the weather app."""
    print(f"Fetching weather for {CITY}...")
    weather_data = get_weather()
    if weather_data:
        temp = round(weather_data['main']['temp'])
        condition = weather_data['weather'][0]['icon']
        
        return {
            "name": "weather",
            "text": f"{temp}°C",
            "icon": get_weather_icon(condition),
            "color": [255, 255, 255] # White
        }
    return None
