"""Unit tests for Pydantic models."""
import pytest
from pydantic import ValidationError
from mcp_server.models.itinerary_models import ItineraryPreferences


@pytest.mark.unit
class TestItineraryPreferences:
    """Test ItineraryPreferences model validation and behavior."""
    
    def test_valid_preferences(self):
        """Test creating valid preferences with all fields."""
        prefs = ItineraryPreferences(extend_trip=True, new_days=3)
        
        assert prefs.extend_trip is True
        assert prefs.new_days == 3
    
    def test_default_values(self):
        """Test that default values are applied correctly."""
        prefs = ItineraryPreferences(extend_trip=False)
        
        assert prefs.extend_trip is False
        assert prefs.new_days == 2  # Default value
    
    def test_custom_days(self):
        """Test setting custom number of days."""
        prefs = ItineraryPreferences(extend_trip=True, new_days=5)
        
        assert prefs.new_days == 5
    
    def test_minimum_days(self):
        """Test that various day values are accepted."""
        prefs = ItineraryPreferences(extend_trip=True, new_days=1)
        assert prefs.new_days == 1
        
        prefs = ItineraryPreferences(extend_trip=True, new_days=10)
        assert prefs.new_days == 10
    
    def test_from_dict(self):
        """Test creating model instance from dictionary."""
        data = {"extend_trip": True, "new_days": 4}
        prefs = ItineraryPreferences(**data)
        
        assert prefs.extend_trip is True
        assert prefs.new_days == 4
    
    def test_to_dict(self):
        """Test serializing model to dictionary."""
        prefs = ItineraryPreferences(extend_trip=True, new_days=3)
        prefs_dict = prefs.model_dump()
        
        assert prefs_dict["extend_trip"] is True
        assert prefs_dict["new_days"] == 3

