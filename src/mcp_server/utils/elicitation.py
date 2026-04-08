"""Elicitation utilities for MCP server."""

from fastmcp import Context

from mcp_server.models.itinerary_models import ItineraryPreferences


async def elicit_trip_extension(
    ctx: Context, start_date: str, current_days: int, min_days: int = 2
) -> tuple[int, str]:
    """
    Elicit user preference to extend trip if below minimum days.

    This function handles the elicitation flow for suggesting minimum trip duration.
    It will:
    1. Check if current days is below minimum
    2. Prompt user to extend the trip if supported by client
    3. Handle cases where elicitation is not supported
    4. Return updated days and optional warning note

    Args:
        ctx: MCP Context for elicitation
        start_date: Trip start date as string
        current_days: Current number of days for the trip
        min_days: Minimum recommended days (default: 2)

    Returns:
        tuple: (updated_days, elicitation_note)
            - updated_days: The number of days after elicitation (extended or original)
            - elicitation_note: Empty string or warning message if elicitation not supported

    Raises:
        ValueError: If user cancels the trip extension

    """
    elicitation_note = ""
    days = current_days

    if current_days >= min_days:
        return days, elicitation_note

    try:
        await ctx.info(f"Elicitation: Suggest minimum {min_days} days for a better itinerary")
        result = await ctx.elicit(
            message=(
                f"Only {current_days} day(s) detected for your itinerary "
                f"starting on {start_date}! "
                f"For a meaningful travel experience, we recommend "
                f"at least {min_days} days. "
                "This allows for varied activities, proper rest, "
                "and a better exploration of the destination. "
                f"Would you like to extend your trip to "
                f"{min_days} or more days?"
            ),
            response_type=ItineraryPreferences,
        )
    except (AttributeError, NotImplementedError):
        await ctx.error(
            f"Note: Elicitation not supported by client. "
            f"Proceeding with {current_days}-day itinerary."
        )
        elicitation_note = (
            f"NOTE: Your MCP client does not support interactive elicitation. "
            f"We recommend at least {min_days} days for a better travel experience. "
            f"Proceeding with {current_days}-day itinerary.\n\n"
        )
        return days, elicitation_note

    if result.action == "accept" and result.data and result.data.extend_trip:
        days = max(result.data.new_days, min_days)
        await ctx.info(f"Trip extended to {days} days")
    elif result.action == "accept" and result.data:
        msg = (
            "[CANCELLED] Itinerary generation cancelled. "
            f"Please plan for at least {min_days} days for a better experience."
        )
        raise ValueError(msg)
    else:
        msg = "[CANCELLED] Itinerary generation cancelled by user."
        raise ValueError(msg)

    return days, elicitation_note
