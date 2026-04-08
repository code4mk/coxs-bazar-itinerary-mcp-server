import json
from datetime import UTC, datetime

from dateutil import parser
from fastmcp import Context

from mcp_server.prompt_templates.travel import (
    get_itinerary_prompt,
    get_weather_based_activities_prompt,
)
from mcp_server.utils.elicitation import elicit_trip_extension
from mcp_server.utils.get_weather_forecast import get_activity_suggestions as get_suggestions


async def s_generate_itinerary(ctx: Context, start_date: str, days: int) -> str:
    """Generate a complete itinerary with weather data and activity suggestions."""
    try:
        days, elicitation_note = await elicit_trip_extension(ctx, start_date, days, min_days=2)
    except ValueError as e:
        await ctx.error(f"Error: {e!s}")
        return str(e)

    try:
        start_date = parser.parse(start_date)
    except ValueError:
        start_date = datetime.now(tz=UTC)

    read_weather_forecast = await ctx.read_resource(
        f"weather://coxsbazar/forecast/{start_date}/{days}"
    )
    weather_data = json.loads(read_weather_forecast.contents[0].content)

    # Generate base itinerary prompt
    base_prompt = await get_itinerary_prompt(days, start_date)

    # Generate weather-based activities prompt
    weather_prompt = await get_weather_based_activities_prompt(weather_data)

    # Format output
    output = f"""# Cox's Bazar Itinerary Planning

## Trip Details
- **Location:** {weather_data["location"]}
- **Start Date:** {weather_data["start_date"]}
- **Duration:** {days} day(s)
- **Timezone:** {weather_data["timezone"]}

## Weather Forecast

"""

    # Add detailed forecast
    for day in weather_data["forecast"]:
        output += f"""### Day {day["day"]} - {day["date"]}
- **Weather:** {day["weather"]}
- **Temperature:** {day["temp_min"]}°C - {day["temp_max"]}°C (Average: {day["temp_avg"]}°C)
- **Precipitation:** {day["precipitation"]}mm
- **Wind Speed:** {day["windspeed"]} km/h
- **Sunrise:** {day["sunrise"]} | **Sunset:** {day["sunset"]}

**Activity Suggestions:**
"""

        # Get activity suggestions for different times
        temp_avg = day["temp_avg"]
        morning_activities = get_suggestions(temp_avg - 2, "morning")
        afternoon_activities = get_suggestions(temp_avg, "afternoon")
        evening_activities = get_suggestions(temp_avg, "evening")

        output += f"""
- **Morning:** {", ".join(morning_activities[:2])}
- **Afternoon:** {", ".join(afternoon_activities[:2])}
- **Evening:** {", ".join(evening_activities[:2])}

{elicitation_note}

"""

    output += f"""
---

## AI Itinerary Generation Prompt

{base_prompt}

---

## Weather-Based Activities Prompt

{weather_prompt}

---

**Note:** Use the above prompts with an AI assistant to generate a detailed,
personalized itinerary based on the weather forecast and your preferences.
"""

    return output


async def s_get_activity_suggestions(
    temperature: float, time_of_day: str = "afternoon"
) -> list[str]:
    """Suggest activities based on temperature and time of day."""
    return get_suggestions(temperature, time_of_day)
