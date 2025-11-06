from mcp_server.mcp_instance import mcp

@mcp.resource("weather://coxsbazar/forecast/{start_date}/{days}")
def resource_weather_forecast(start_date: str, days: int):
    return {
        "location": "Cox's Bazar",
        "start_date": start_date,
        "days": days,
        "forecast": [
            {"day": 1, "condition": "Sunny", "temp": 30},
            {"day": 2, "condition": "Cloudy", "temp": 28},
        ],
    }



