from mcp_server.mcp_instance import mcp
from mcp_server.components.prompts.travel_prompts import travel_prompt
from mcp_server.components.resources.weather import resource_weather_forecast

@mcp.tool()
def itinerary_tool(start_date: str, days: int) -> str:
    weather_forecast = resource_weather_forecast(start_date, days)
    
    # extract all temperatures as an array like [30, 28]
    temps = [f["temp"] for f in weather_forecast["forecast"]]

    prompt = travel_prompt(temps)

    # for example, you could include temps in your output or logic
    return f"Temperatures: {temps}\n\nPrompt:\n{prompt}"
