"""Weather forecast utility using Open-Meteo API."""

import logging
from datetime import UTC, datetime, timedelta
from typing import Any

from dateutil import parser

from mcp_server.utils.http import open_meteo_client

logger = logging.getLogger(__name__)

COX_BAZAR_LAT = 21.4272
COX_BAZAR_LON = 92.0058

TEMP_THRESHOLD_MORNING = 28
TEMP_THRESHOLD_AFTERNOON = 30
FALLBACK_BASE_TEMP = 28


def get_weather_forecast(start_date: str, days: int) -> dict[str, Any]:
    """
    Fetch weather forecast from Open-Meteo API for Cox's Bazar.

    Args:
        start_date: Start date in various formats (e.g., "2025-01-15", "15 Jan 2025", "today")
        days: Number of days to fetch forecast for (1-16)

    Returns:
        Dictionary containing location, start_date, days, and detailed forecast

    Raises:
        httpx.HTTPStatusError: If API request fails

    """
    start_dt = (
        datetime.now(tz=UTC) if start_date.lower() == "today" else _parse_date_or_now(start_date)
    )

    end_dt = start_dt + timedelta(days=days - 1)

    start_date_str = start_dt.strftime("%Y-%m-%d")
    end_date_str = end_dt.strftime("%Y-%m-%d")

    params = {
        "latitude": COX_BAZAR_LAT,
        "longitude": COX_BAZAR_LON,
        "daily": (
            "temperature_2m_max,temperature_2m_min,"
            "precipitation_sum,weathercode,"
            "windspeed_10m_max,sunrise,sunset"
        ),
        "timezone": "Asia/Dhaka",
        "start_date": start_date_str,
        "end_date": end_date_str,
    }

    try:
        response = open_meteo_client.get("/v1/forecast", params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        logger.warning("Open-Meteo API error: %s. Using fallback data.", e)
        return get_fallback_forecast(start_date_str, end_date_str, days)

    if "error" in data:
        logger.warning(
            "Open-Meteo API error: %s. Using fallback data.",
            data.get("reason", "Unknown error"),
        )
        return get_fallback_forecast(start_date_str, end_date_str, days)

    forecast = _parse_forecast_data(data)

    return {
        "location": "Cox's Bazar, Bangladesh",
        "coordinates": {"latitude": COX_BAZAR_LAT, "longitude": COX_BAZAR_LON},
        "start_date": start_date_str,
        "end_date": end_date_str,
        "days": days,
        "timezone": "Asia/Dhaka",
        "forecast": forecast,
    }


def _parse_date_or_now(date_str: str) -> datetime:
    """Parse a date string, falling back to current UTC time on failure."""
    try:
        return parser.parse(date_str)
    except ValueError:
        return datetime.now(tz=UTC)


def _parse_forecast_data(data: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract and structure daily forecast entries from API response."""
    daily = data.get("daily", {})
    dates = daily.get("time", [])
    temp_max = daily.get("temperature_2m_max", [])
    temp_min = daily.get("temperature_2m_min", [])
    precipitation = daily.get("precipitation_sum", [])
    weathercodes = daily.get("weathercode", [])
    windspeed = daily.get("windspeed_10m_max", [])
    sunrise = daily.get("sunrise", [])
    sunset = daily.get("sunset", [])

    forecast = []
    for i in range(len(dates)):
        weather_desc = get_weather_description(weathercodes[i] if i < len(weathercodes) else 0)
        forecast.append(
            {
                "day": i + 1,
                "date": dates[i],
                "temp_max": round(temp_max[i], 1) if i < len(temp_max) else None,
                "temp_min": round(temp_min[i], 1) if i < len(temp_min) else None,
                "temp_avg": (
                    round((temp_max[i] + temp_min[i]) / 2, 1)
                    if i < len(temp_max) and i < len(temp_min)
                    else None
                ),
                "precipitation": (round(precipitation[i], 1) if i < len(precipitation) else 0),
                "weather": weather_desc,
                "weathercode": weathercodes[i] if i < len(weathercodes) else 0,
                "windspeed": (round(windspeed[i], 1) if i < len(windspeed) else None),
                "sunrise": (sunrise[i].split("T")[1] if i < len(sunrise) else None),
                "sunset": (sunset[i].split("T")[1] if i < len(sunset) else None),
            }
        )
    return forecast


def get_weather_description(weathercode: int) -> str:
    """
    Convert WMO weather code to human-readable description.

    Args:
        weathercode: WMO weather code

    Returns:
        Human-readable weather description

    """
    weather_codes = {
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
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }
    return weather_codes.get(weathercode, "Unknown")


def get_fallback_forecast(start_date: str, end_date: str, days: int) -> dict[str, Any]:
    """
    Provide fallback forecast data when API is unavailable.

    Args:
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)
        days: Number of days

    Returns:
        Mock forecast data

    """
    forecast = []

    start_dt = datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=UTC)

    for i in range(days):
        current_date = start_dt + timedelta(days=i)
        temp_variation = (i % 3) - 1
        temp_max = FALLBACK_BASE_TEMP + 2 + temp_variation
        temp_min = FALLBACK_BASE_TEMP - 3 + temp_variation

        forecast.append(
            {
                "day": i + 1,
                "date": current_date.strftime("%Y-%m-%d"),
                "temp_max": temp_max,
                "temp_min": temp_min,
                "temp_avg": round((temp_max + temp_min) / 2, 1),
                "precipitation": 0,
                "weather": "Partly cloudy",
                "weathercode": 2,
                "windspeed": 15.0,
                "sunrise": "06:00",
                "sunset": "18:00",
            }
        )

    return {
        "location": "Cox's Bazar, Bangladesh",
        "coordinates": {"latitude": COX_BAZAR_LAT, "longitude": COX_BAZAR_LON},
        "start_date": start_date,
        "end_date": end_date,
        "days": days,
        "timezone": "Asia/Dhaka",
        "forecast": forecast,
        "note": "Fallback data - API unavailable",
    }


def get_activity_suggestions(temperature: float, time_of_day: str = "afternoon") -> list[str]:
    """
    Suggest activities based on temperature and time of day.

    Args:
        temperature: Temperature in Celsius
        time_of_day: "morning", "afternoon", or "evening"

    Returns:
        List of suggested activities

    """
    if time_of_day == "morning":
        if temperature < TEMP_THRESHOLD_MORNING:
            return [
                "Beach walk and photography",
                "Visit Himchari National Park",
                "Sunrise at Laboni Beach",
                "Morning yoga on the beach",
            ]
        return [
            "Early morning swim",
            "Sunrise boat ride",
            "Visit Inani Beach",
            "Morning market exploration",
        ]

    if time_of_day == "afternoon":
        if temperature < TEMP_THRESHOLD_AFTERNOON:
            return [
                "Visit Aggameda Khyang monastery",
                "Explore Ramu Buddhist Village",
                "Maheshkhali Island tour",
                "Marine Drive scenic route",
            ]
        return [
            "Indoor activities - shopping at local markets",
            "Visit Bangabandhu Safari Park",
            "Relax at beach resorts",
            "Water sports activities",
        ]

    return [
        "Sunset at Sugandha Beach",
        "Seafood dinner at local restaurants",
        "Beach bonfire",
        "Night market shopping",
        "Cultural performances",
    ]
