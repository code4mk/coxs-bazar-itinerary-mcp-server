"""Pydantic models for itinerary tools."""
from pydantic import BaseModel, Field


class ItineraryPreferences(BaseModel):
    """Schema for collecting user itinerary preferences."""
    extendTrip: bool = Field(
        description="Would you like to extend your trip to the recommended minimum of 2 days?"
    )
    newDays: int = Field(
        default=2,
        description="Number of days for the extended trip (minimum 2)",
    )

