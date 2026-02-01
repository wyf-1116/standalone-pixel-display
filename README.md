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
Create a `.env` file in the root directory and add your configuration (see `.env.example` for reference).

#### Environment Variables Reference

| Variable | Description | Default |
| :--- | :--- | :--- |
| `AWTRIX_IP` | The IP address of your AWTRIX 3 device. | - |
| `WEATHER_API_KEY` | Your OpenWeatherMap API key. | - |
| `CITY` | City name for weather data. | `London` |
| `COUNTRY_CODE` | ISO 3166-1 alpha-2 country code. | `GB` |
| `APP_SWITCH_INTERVAL` | Seconds to display each app before switching. | `10` |
| `UPDATE_INTERVAL` | Seconds to wait between full refresh cycles. | `300` |
| `NS_API_KEY` | Your NS Railway (Dutch Railways) API key. | - |
| `NS_STATION_CODE` | The station code for disruption monitoring (e.g., `ALMB`). | `ALMB` |
| `LAT` | Latitude for Buienradar rain forecast. | `52.38` |
| `LON` | Longitude for Buienradar rain forecast. | `5.27` |

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
