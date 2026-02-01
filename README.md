# Standalone Pixel Display

A Python-based framework for displaying dynamic information (Weather, NS Disruptions, Rain Forecast, Chinese Calendar) on an AWTRIX 3 / Pixel Display.

## Features

- **Dynamic App Loading**: Automatically loads and cycles through scripts in the `apps/` directory.
- **Weather Integration**: Fetches real-time weather and temperature from OpenWeatherMap.
- **NS Disruptions**: Displays train disruption counts from the Dutch Railways (NS) API.
- **Rain Forecast**: Shows upcoming rain probability using Buienradar.
- **Chinese Calendar**: Displays traditional Chinese calendar dates.
- **Docker Support**: Easy deployment using Docker and Docker Compose.

## Prerequisites

- [AWTRIX 3](https://blueforcer.github.io/awtrix3/) device or compatible.
- Python 3.9+
- API Keys:
  - [OpenWeatherMap](https://openweathermap.org/api) (for weather data)
  - [NS API Portal](https://apiportal.ns.nl/) (for train disruptions)

## setup

### 1. Clone the repository
```bash
git clone git@github.com:wyf-1116/standalone-pixel-display.git
cd standalone-pixel-display
```

### 2. Configuration
Create a `.env` file in the root directory and add your configuration (see `.env.example` for reference):

```bash
# AWTRIX 3 Device IP
AWTRIX_IP=192.168.x.x

# OpenWeatherMap API Key
WEATHER_API_KEY=your_weather_api_key

# NS Railway API Key
NS_API_KEY=your_ns_api_key
```

### 3. Running with Python
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

### 4. Running with Docker
```bash
docker-compose up -d
```

## Project Structure

- `main.py`: The main dispatcher that manages the app cycle and communication with AWTRIX.
- `apps/`: Directory containing individual display applications.
  - `weather.py`: Weather and temperature data.
  - `ns_disruptions.py`: Train disruption alerts.
  - `rain_forecast.py`: Local rain predictions.
  - `chinese_calendar.py`: Chinese calendar information.
- `.env`: (Ignored by git) Local configuration and API keys.

## License

MIT
