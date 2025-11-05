"""Travel-related prompts for AI itinerary generation."""
from datetime import datetime, timedelta
from dateutil import parser

# Store prompt functions for reuse by tools
_prompt_functions = {}

def register_travel_prompts(mcp):
    """Register travel prompts with the MCP server."""
    
    @mcp.prompt(
        title="Cox's Bazar AI Itinerary",
        description="Generate day-by-day itinerary based on number of days, temperature forecast, and start date"
    )
    def generate_itinerary(days: int, temp_list: list, start_date: str) -> str:
        """
        AI prompt for generating itinerary with actual dates and daily temperatures.
        
        Args:
            days: Number of days for the trip
            temp_list: List of daily temperatures in Celsius
            start_date: Start date of the trip
        
        Returns:
            Formatted prompt for AI
        """
        # Parse start date
        try:
            start_dt = parser.parse(start_date)
        except (ValueError, TypeError):
            start_dt = datetime.today()
        
        normalized_start = start_dt.strftime("%d %b %Y")
        
        # Build prompt for AI
        prompt = (
            f"You are a travel expert. Generate a {days}-day itinerary for Cox's Bazar, Bangladesh. "
            f"The trip starts on {normalized_start}. "
            "Include morning, afternoon, and evening activities for each day. "
            "Each day's activities should consider the following temperatures in °C:\n"
        )
        
        for i, temp in enumerate(temp_list):
            date_str = (start_dt + timedelta(days=i)).strftime("%d %b %Y")
            prompt += f"- {date_str}: {temp}°C\n"
        
        prompt += (
            "\nMake the itinerary creative, diverse, enjoyable, and unique for each day. "
            "Suggest beaches, sightseeing, food, and local experiences."
        )
        
        return prompt
    
    # Store prompt function for reuse
    _prompt_functions['generate_itinerary'] = generate_itinerary
    
    @mcp.prompt(
        title="Detailed Cox's Bazar Itinerary",
        description="Generate detailed itinerary with budget and interests"
    )
    def generate_detailed_itinerary(
        days: int,
        temp_list: list,
        start_date: str,
        budget: str = "moderate",
        interests: list = None
    ) -> str:
        """
        Generate a detailed AI prompt with budget and interests.
        
        Args:
            days: Number of days
            temp_list: Daily temperatures
            start_date: Start date
            budget: "budget", "moderate", or "luxury"
            interests: List of interests (e.g., ["adventure", "relaxation", "culture"])
        
        Returns:
            Detailed prompt for AI
        """
        if interests is None:
            interests = ["beaches", "local culture", "food"]
        
        # Parse start date
        try:
            start_dt = parser.parse(start_date)
        except (ValueError, TypeError):
            start_dt = datetime.today()
        
        normalized_start = start_dt.strftime("%d %b %Y")
        
        prompt = (
            f"🌴 CREATE A DETAILED {days}-DAY ITINERARY FOR COX'S BAZAR, BANGLADESH\n\n"
            f"📅 Start Date: {normalized_start}\n"
            f"💰 Budget Level: {budget.upper()}\n"
            f"🎯 Interests: {', '.join(interests)}\n\n"
            f"🌡️ DAILY TEMPERATURES:\n"
        )
        
        for i, temp in enumerate(temp_list):
            date_str = (start_dt + timedelta(days=i)).strftime("%d %b %Y")
            prompt += f"  Day {i+1} ({date_str}): {temp}°C\n"
        
        budget_guidelines = {
            "budget": "Focus on affordable options, local eateries, free activities, budget hotels (1000-2000 BDT/night)",
            "moderate": "Mix of mid-range restaurants, popular attractions, comfortable hotels (3000-5000 BDT/night)",
            "luxury": "Premium experiences, fine dining, luxury resorts (8000+ BDT/night), private tours"
        }
        
        prompt += (
            f"\n💵 BUDGET GUIDELINES:\n{budget_guidelines.get(budget, budget_guidelines['moderate'])}\n\n"
            f"📋 REQUIREMENTS:\n"
            f"For each day, provide:\n"
            f"1. Morning activities (with specific timings)\n"
            f"2. Lunch recommendations (restaurant names & dishes)\n"
            f"3. Afternoon activities\n"
            f"4. Evening activities\n"
            f"5. Dinner recommendations\n"
            f"6. Estimated daily costs in BDT\n"
            f"7. Travel tips and weather considerations\n\n"
            f"🎯 Focus on: {', '.join(interests)}\n"
            f"Make it creative, practical, and tailored to the temperature conditions!"
        )
        
        return prompt
    
    # Store prompt function for reuse
    _prompt_functions['generate_detailed_itinerary'] = generate_detailed_itinerary
    
    @mcp.prompt(
        title="Activity Suggestions",
        description="Suggest activities based on weather conditions"
    )
    def suggest_activities(temperature: float, weather_condition: str = "clear") -> str:
        """
        Generate prompt for activity suggestions based on weather.
        
        Args:
            temperature: Temperature in Celsius
            weather_condition: Weather condition ("clear", "rainy", "cloudy")
        
        Returns:
            Prompt for activity suggestions
        """
        prompt = (
            f"Suggest activities for Cox's Bazar with current conditions:\n"
            f"🌡️ Temperature: {temperature}°C\n"
            f"🌤️ Weather: {weather_condition}\n\n"
            f"Provide:\n"
            f"- 5 suitable activities\n"
            f"- Why each activity is good for these conditions\n"
            f"- Estimated duration and cost in BDT\n"
            f"- Safety tips if needed\n"
        )
        
        return prompt
    
    # Store prompt function for reuse
    _prompt_functions['suggest_activities'] = suggest_activities


def get_prompt(prompt_name: str):
    """
    Get a registered prompt function by name.
    
    Args:
        prompt_name: Name of the prompt function
    
    Returns:
        The prompt function
    
    Raises:
        KeyError: If prompt not found
    """
    return _prompt_functions.get(prompt_name)