"""Weather-related resources for Cox's Bazar."""
import requests
import json
from datetime import datetime, timedelta


# Cox's Bazar coordinates
LATITUDE = 21.4272
LONGITUDE = 92.0058
TIMEZONE = "Asia/Dhaka"

WEATHER_CODE_DESCRIPTIONS = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def fetch_weather_data(start_dt: datetime, days: int, params: str) -> dict:
    """
    Public helper function to fetch weather data from Open-Meteo API.
    
    This can be used by both resources and tools to avoid code duplication.
    
    Args:
        start_dt: Start date for the forecast
        days: Number of days to fetch
        params: Additional URL parameters (e.g., "&daily=temperature_2m_max")
    
    Returns:
        Weather data dictionary or None if the API call fails
    """
    end_dt = start_dt + timedelta(days=days - 1)
    
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={LATITUDE}&longitude={LONGITUDE}"
        f"{params}"
        f"&timezone={TIMEZONE}"
        f"&start_date={start_dt.strftime('%Y-%m-%d')}"
        f"&end_date={end_dt.strftime('%Y-%m-%d')}"
    )
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Weather API error: {e}")
        return None


def get_temperature_forecast(start_dt: datetime, days: int) -> list:
    """
    Get temperature forecast for Cox's Bazar.
    
    Public utility function that can be used by tools to get temperature data
    without duplicating API logic.
    
    Args:
        start_dt: Start date for the forecast
        days: Number of days to forecast
    
    Returns:
        List of maximum temperatures in Celsius
    """
    data = fetch_weather_data(
        start_dt,
        days,
        "&daily=temperature_2m_max"
    )
    
    if not data:
        return [30.0] * days
    
    max_temps = data.get("daily", {}).get("temperature_2m_max", [])
    
    # Ensure we have exactly 'days' number of temperatures
    temp_list = []
    for i in range(days):
        if i < len(max_temps):
            temp_list.append(round(max_temps[i], 1))
        else:
            temp_list.append(max_temps[-1] if max_temps else 30.0)
    
    return temp_list


def _get_current_weather_data() -> str:
    """Helper to generate current weather data."""
    start_dt = datetime.today()
    data = fetch_weather_data(
        start_dt, 
        1,
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode"
        "&current=temperature_2m,weathercode,windspeed_10m"
    )
    
    if not data:
        return json.dumps({
            "location": "Cox's Bazar, Bangladesh",
            "date": start_dt.strftime("%Y-%m-%d"),
            "error": "Unable to fetch weather data",
            "current": {"temperature": 30.0, "conditions": "Unknown"},
            "today_forecast": {"max": 30.0, "min": 25.0}
        }, indent=2)
    
    current = data.get("current", {})
    daily = data.get("daily", {})
    
    weather_code = current.get("weathercode", 0)
    conditions = WEATHER_CODE_DESCRIPTIONS.get(weather_code, "Unknown")
    
    result = {
        "location": "Cox's Bazar, Bangladesh",
        "coordinates": {"latitude": LATITUDE, "longitude": LONGITUDE},
        "date": start_dt.strftime("%Y-%m-%d"),
        "current": {
            "temperature": round(current.get("temperature_2m", 30.0), 1),
            "conditions": conditions,
            "wind_speed": round(current.get("windspeed_10m", 0.0), 1),
        },
        "today_forecast": {
            "max_temperature": round(daily.get("temperature_2m_max", [30.0])[0], 1),
            "min_temperature": round(daily.get("temperature_2m_min", [25.0])[0], 1),
            "precipitation": round(daily.get("precipitation_sum", [0.0])[0], 1),
        }
    }
    
    return json.dumps(result, indent=2)


def _get_weather_forecast_data() -> str:
    """Helper to generate weather forecast data."""
    start_dt = datetime.today()
    days = 7
    data = fetch_weather_data(
        start_dt,
        days,
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode,windspeed_10m_max"
    )
    
    if not data:
        dates = [(start_dt + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]
        forecast = []
        for date in dates:
            forecast.append({
                "date": date,
                "max_temp": 30.0,
                "min_temp": 25.0,
                "precipitation": 0.0,
                "conditions": "Unknown",
                "max_wind_speed": 10.0
            })
        
        return json.dumps({
            "location": "Cox's Bazar, Bangladesh",
            "forecast_period": f"{dates[0]} to {dates[-1]}",
            "error": "Unable to fetch complete weather data",
            "forecast": forecast
        }, indent=2)
    
    daily_data = data.get("daily", {})
    dates = daily_data.get("time", [])
    max_temps = daily_data.get("temperature_2m_max", [])
    min_temps = daily_data.get("temperature_2m_min", [])
    precipitation = daily_data.get("precipitation_sum", [])
    weather_codes = daily_data.get("weathercode", [])
    wind_speeds = daily_data.get("windspeed_10m_max", [])
    
    forecast = []
    for i in range(min(len(dates), days)):
        weather_code = weather_codes[i] if i < len(weather_codes) else 0
        conditions = WEATHER_CODE_DESCRIPTIONS.get(weather_code, "Unknown")
        
        forecast.append({
            "date": dates[i],
            "max_temp": round(max_temps[i], 1) if i < len(max_temps) else 30.0,
            "min_temp": round(min_temps[i], 1) if i < len(min_temps) else 25.0,
            "precipitation": round(precipitation[i], 1) if i < len(precipitation) else 0.0,
            "conditions": conditions,
            "max_wind_speed": round(wind_speeds[i], 1) if i < len(wind_speeds) else 10.0
        })
    
    result = {
        "location": "Cox's Bazar, Bangladesh",
        "coordinates": {"latitude": LATITUDE, "longitude": LONGITUDE},
        "forecast_period": f"{dates[0]} to {dates[-1]}" if dates else "Unknown",
        "forecast": forecast
    }
    
    return json.dumps(result, indent=2)


def _get_temperature_summary_data() -> str:
    """Helper to generate temperature summary data."""
    start_dt = datetime.today()
    days = 3
    data = fetch_weather_data(
        start_dt,
        days,
        "&daily=temperature_2m_max,temperature_2m_min"
    )
    
    if not data:
        result = {
            "location": "Cox's Bazar, Bangladesh",
            "summary": "Temperature forecast unavailable",
            "temperatures": [{"day": i+1, "max": 30.0, "min": 25.0} for i in range(days)]
        }
        return json.dumps(result, indent=2)
    
    daily_data = data.get("daily", {})
    dates = daily_data.get("time", [])
    max_temps = daily_data.get("temperature_2m_max", [])
    min_temps = daily_data.get("temperature_2m_min", [])
    
    temperatures = []
    for i in range(min(len(dates), days)):
        temperatures.append({
            "date": dates[i],
            "day": i + 1,
            "max_temp": round(max_temps[i], 1) if i < len(max_temps) else 30.0,
            "min_temp": round(min_temps[i], 1) if i < len(min_temps) else 25.0,
        })
    
    avg_max = sum(t["max_temp"] for t in temperatures) / len(temperatures) if temperatures else 30.0
    avg_min = sum(t["min_temp"] for t in temperatures) / len(temperatures) if temperatures else 25.0
    
    result = {
        "location": "Cox's Bazar, Bangladesh",
        "period": f"Next {days} days",
        "average_max": round(avg_max, 1),
        "average_min": round(avg_min, 1),
        "daily_temperatures": temperatures
    }
    
    return json.dumps(result, indent=2)


def register_weather_resources(mcp):
    """Register weather resources with the MCP server."""

    # Define and register current weather resource
    @mcp.resource("weather://coxsbazar/current")
    def resource_current_weather() -> str:
        """Current weather conditions for Cox's Bazar with today's forecast."""
        return _get_current_weather_data()
    

    # Define and register forecast resource
    @mcp.resource("weather://coxsbazar/forecast")
    def resource_weather_forecast() -> str:
        """Detailed 7-day weather forecast for Cox's Bazar."""
        return _get_weather_forecast_data()
    
    # Define and register temperature summary resource  
    @mcp.resource("weather://coxsbazar/temperature-summary")
    def resource_temperature_summary() -> str:
        """Quick temperature summary for the next 3 days in Cox's Bazar."""
        return _get_temperature_summary_data()
    
    # mcp.resource("weather://coxsbazar/temperature-summary")(resource_temperature_summary)
