from mcp_server.mcp_instance import mcp
from mcp_server.prompt_templates.travel import get_itinerary_prompt


@mcp.prompt()
async def generate_itinerary_prompt(days: int, start_date: str) -> str:
    """Generate a travel itinerary prompt for the given trip duration and start date."""
    return await get_itinerary_prompt(days, start_date)
