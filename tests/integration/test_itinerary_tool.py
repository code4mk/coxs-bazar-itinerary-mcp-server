"""Integration tests for itinerary tool.

These tests verify the complete flow of itinerary generation including
elicitation, weather data retrieval, and prompt generation.
"""
import pytest
import json
from unittest.mock import AsyncMock, Mock, patch
from mcp_server.services.itenerary_service import s_generate_itinerary

SERVICE_MODULE = "mcp_server.services.itenerary_service"


def _mock_read_resource(weather_data):
    """Build a mock return value matching ctx.read_resource(...).contents[0].content."""
    result = Mock()
    result.contents = [Mock(content=json.dumps(weather_data))]
    return result


@pytest.mark.integration
class TestCoxAiItinerary:
    """Test complete itinerary generation workflow."""
    
    @pytest.mark.asyncio
    async def test_itinerary_generation_success(
        self, mock_context, sample_weather_data
    ):
        """Test successful end-to-end itinerary generation."""
        mock_context.elicit = AsyncMock(side_effect=NotImplementedError())
        mock_context.read_resource = AsyncMock(
            return_value=_mock_read_resource(sample_weather_data)
        )
        
        with patch(f"{SERVICE_MODULE}.get_itinerary_prompt", new_callable=AsyncMock) as mock_prompt, \
             patch(f"{SERVICE_MODULE}.get_weather_based_activities_prompt", new_callable=AsyncMock) as mock_weather_prompt:
            
            mock_prompt.return_value = "Base itinerary prompt"
            mock_weather_prompt.return_value = "Weather-based prompt"
            
            result = await s_generate_itinerary(mock_context, "2025-01-15", 3)
            
            assert isinstance(result, str)
            assert "Cox's Bazar Itinerary Planning" in result
            assert "Trip Details" in result
            assert "Weather Forecast" in result
            assert "3 day(s)" in result
            mock_context.read_resource.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_itinerary_with_elicitation(
        self, mock_context, sample_weather_data
    ):
        """Test itinerary generation with trip extension via elicitation."""
        mock_result = Mock()
        mock_result.action = "accept"
        mock_result.data = Mock()
        mock_result.data.extend_trip = True
        mock_result.data.new_days = 3
        
        mock_context.elicit.return_value = mock_result
        mock_context.read_resource = AsyncMock(
            return_value=_mock_read_resource(sample_weather_data)
        )
        
        with patch(f"{SERVICE_MODULE}.get_itinerary_prompt", new_callable=AsyncMock) as mock_prompt, \
             patch(f"{SERVICE_MODULE}.get_weather_based_activities_prompt", new_callable=AsyncMock) as mock_weather_prompt:
            
            mock_prompt.return_value = "Base prompt"
            mock_weather_prompt.return_value = "Weather prompt"
            
            result = await s_generate_itinerary(mock_context, "2025-01-15", 1)
            
            assert "3 day(s)" in result
            mock_context.elicit.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_itinerary_elicitation_cancelled(
        self, mock_context
    ):
        """Test itinerary generation when user cancels elicitation."""
        mock_result = Mock()
        mock_result.action = "accept"
        mock_result.data = Mock()
        mock_result.data.extend_trip = False
        
        mock_context.elicit.return_value = mock_result
        
        result = await s_generate_itinerary(mock_context, "2025-01-15", 1)
        
        assert "CANCELLED" in result or "Error" in result
        mock_context.error.assert_called()
    
    @pytest.mark.asyncio
    async def test_itinerary_invalid_date(
        self, mock_context, sample_weather_data
    ):
        """Test itinerary generation with invalid date input."""
        mock_context.elicit = AsyncMock(side_effect=NotImplementedError())
        mock_context.read_resource = AsyncMock(
            return_value=_mock_read_resource(sample_weather_data)
        )
        
        with patch(f"{SERVICE_MODULE}.get_itinerary_prompt", new_callable=AsyncMock) as mock_prompt, \
             patch(f"{SERVICE_MODULE}.get_weather_based_activities_prompt", new_callable=AsyncMock) as mock_weather_prompt:
            
            mock_prompt.return_value = "Base prompt"
            mock_weather_prompt.return_value = "Weather prompt"
            
            result = await s_generate_itinerary(mock_context, "invalid-date", 3)
            
            assert isinstance(result, str)
            assert "Cox's Bazar Itinerary Planning" in result
    
    @pytest.mark.asyncio
    async def test_itinerary_weather_forecast_format(
        self, mock_context, sample_weather_data
    ):
        """Test that itinerary includes properly formatted weather data."""
        mock_context.elicit = AsyncMock(side_effect=NotImplementedError())
        mock_context.read_resource = AsyncMock(
            return_value=_mock_read_resource(sample_weather_data)
        )
        
        with patch(f"{SERVICE_MODULE}.get_itinerary_prompt", new_callable=AsyncMock) as mock_prompt, \
             patch(f"{SERVICE_MODULE}.get_weather_based_activities_prompt", new_callable=AsyncMock) as mock_weather_prompt:
            
            mock_prompt.return_value = "Base prompt"
            mock_weather_prompt.return_value = "Weather prompt"
            
            result = await s_generate_itinerary(mock_context, "2025-01-15", 3)
            
            assert "Temperature" in result
            assert "Weather:" in result
            assert "Precipitation:" in result
            assert "Wind Speed:" in result
            assert "Sunrise:" in result
            assert "Sunset:" in result
            assert "Activity Suggestions:" in result
    
    @pytest.mark.asyncio
    async def test_itinerary_activity_suggestions_included(
        self, mock_context, sample_weather_data
    ):
        """Test that activity suggestions are properly integrated."""
        mock_context.elicit = AsyncMock(side_effect=NotImplementedError())
        mock_context.read_resource = AsyncMock(
            return_value=_mock_read_resource(sample_weather_data)
        )
        
        with patch(f"{SERVICE_MODULE}.get_itinerary_prompt", new_callable=AsyncMock) as mock_prompt, \
             patch(f"{SERVICE_MODULE}.get_weather_based_activities_prompt", new_callable=AsyncMock) as mock_weather_prompt:
            
            mock_prompt.return_value = "Base prompt"
            mock_weather_prompt.return_value = "Weather prompt"
            
            result = await s_generate_itinerary(mock_context, "2025-01-15", 3)
            
            assert "Morning:" in result
            assert "Afternoon:" in result
            assert "Evening:" in result


@pytest.mark.integration
class TestGetActivitySuggestions:
    """Test activity suggestions utility function."""
    
    def test_get_activity_suggestions_morning(self):
        """Test morning activity suggestions."""
        from mcp_server.utils.get_weather_forecast import (
            get_activity_suggestions as get_suggestions_impl
        )
        
        result = get_suggestions_impl(25.0, "morning")
        
        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(activity, str) for activity in result)
    
    def test_get_activity_suggestions_afternoon(self):
        """Test afternoon activity suggestions."""
        from mcp_server.utils.get_weather_forecast import (
            get_activity_suggestions as get_suggestions_impl
        )
        
        result = get_suggestions_impl(28.0, "afternoon")
        
        assert isinstance(result, list)
        assert len(result) > 0
    
    def test_get_activity_suggestions_evening(self):
        """Test evening activity suggestions."""
        from mcp_server.utils.get_weather_forecast import (
            get_activity_suggestions as get_suggestions_impl
        )
        
        result = get_suggestions_impl(27.0, "evening")
        
        assert isinstance(result, list)
        assert len(result) > 0

