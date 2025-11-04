"""Itinerary generation tools."""
from datetime import datetime
from dateutil import parser

def register_itinerary_tools(mcp):
    """Register itinerary tools with the MCP server."""
    
    @mcp.tool()
    def cox_ai_itinerary(days: int, start_date: str) -> str:
        """
        Full workflow: fetch daily temperatures + generate AI itinerary.
        Uses the registered MCP prompt 'generate_itinerary' for consistency.
        
        Args:
            days: Number of days for the trip
            start_date: Start date (e.g., "2025-01-15", "15 Jan 2025", "today")
        
        Returns:
            Formatted prompt for AI to generate detailed itinerary
        """
        from mcp_server.resources.weather import get_temperature_forecast
        from mcp_server.prompts.travel_prompts import get_prompt
        
        # Parse start date
        try:
            start_dt = parser.parse(start_date)
        except Exception:
            start_dt = datetime.today()
        
        # Get temperature forecast
        temp_list = get_temperature_forecast(start_dt, days)
        
        # Use the MCP prompt for generating itinerary
        generate_itinerary_prompt = get_prompt('generate_itinerary')
        if generate_itinerary_prompt:
            return generate_itinerary_prompt(days, temp_list, start_date)
        
        # Fallback if prompt not found
        return "Error: Could not load itinerary prompt"
    
    @mcp.tool()
    def get_activity_suggestions(temperature: float, time_of_day: str = "afternoon"):
        """
        Suggest activities based on temperature and time of day.
        
        Args:
            temperature: Temperature in Celsius
            time_of_day: "morning", "afternoon", or "evening"
        
        Returns:
            List of suggested activities
        """
        activities = []
        
        # Temperature-based activities
        if temperature < 25:
            activities.extend([
                "Beach walk and photography",
                "Visit Himchari National Park",
                "Explore local markets",
            ])
        elif temperature < 30:
            activities.extend([
                "Swimming at Inani Beach",
                "Visit Marine Drive",
                "Surfing lessons",
                "Jet skiing",
            ])
        else:  # Hot day
            activities.extend([
                "Visit Aggmeda Khyang (Buddhist monastery)",
                "Indoor shopping at malls",
                "Enjoy fresh coconut water by the beach",
                "Take a boat ride",
            ])
        
        # Time-specific activities
        if time_of_day == "morning":
            activities.extend([
                "Sunrise at Laboni Beach",
                "Fresh seafood breakfast",
                "Bird watching at wetlands",
            ])
        elif time_of_day == "afternoon":
            activities.extend([
                "Lunch at beach restaurants",
                "Visit Ramu Buddhist Temple",
                "Shopping for local handicrafts",
            ])
        else:  # evening
            activities.extend([
                "Sunset at Cox's Bazar beach",
                "Dinner with sea view",
                "Night market exploration",
                "Beach bonfire (if available)",
            ])
        
        return activities