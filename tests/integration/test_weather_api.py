"""Integration tests for weather API interactions."""
import pytest
from unittest.mock import Mock, patch
from mcp_server.utils.get_weather_forecast import get_weather_forecast

WEATHER_MODULE = "mcp_server.utils.get_weather_forecast"


def _mock_http_response(json_data, raise_for_status=None):
    """Build a mock httpx-style response."""
    resp = Mock()
    resp.json.return_value = json_data
    resp.raise_for_status = raise_for_status or Mock()
    return resp


@pytest.mark.integration
class TestWeatherForecastAPI:
    """Test weather forecast API integration and error handling."""
    
    @patch(f"{WEATHER_MODULE}.open_meteo_client")
    def test_successful_forecast(self, mock_client, mock_open_meteo_response):
        """Test successful weather forecast retrieval from API."""
        mock_client.get.return_value = _mock_http_response(mock_open_meteo_response)
        
        result = get_weather_forecast("2025-01-15", 3)
        
        assert result["location"] == "Cox's Bazar, Bangladesh"
        assert result["days"] == 3
        assert len(result["forecast"]) == 3
        assert result["forecast"][0]["day"] == 1
        assert "temp_max" in result["forecast"][0]
        assert "temp_min" in result["forecast"][0]
        assert "temp_avg" in result["forecast"][0]
    
    @patch(f"{WEATHER_MODULE}.open_meteo_client")
    def test_api_error_response(self, mock_client):
        """Test handling of API error responses."""
        mock_client.get.return_value = _mock_http_response({
            "error": True,
            "reason": "Invalid date range"
        })
        
        result = get_weather_forecast("2025-01-15", 3)
        
        assert "note" in result or result["days"] == 3
    
    @patch(f"{WEATHER_MODULE}.open_meteo_client")
    def test_api_request_failure(self, mock_client):
        """Test handling of network failures."""
        mock_client.get.side_effect = Exception("Network error")
        
        result = get_weather_forecast("2025-01-15", 3)
        
        assert result["days"] == 3
        assert len(result["forecast"]) == 3
    
    @patch(f"{WEATHER_MODULE}.open_meteo_client")
    def test_today_date_parsing(self, mock_client):
        """Test parsing 'today' as start date parameter."""
        mock_client.get.return_value = _mock_http_response({
            "daily": {
                "time": ["2025-01-15"],
                "temperature_2m_max": [30.0],
                "temperature_2m_min": [25.0],
                "precipitation_sum": [0.0],
                "weathercode": [0],
                "windspeed_10m_max": [15.0],
                "sunrise": ["2025-01-15T06:00"],
                "sunset": ["2025-01-15T18:00"],
            }
        })
        
        result = get_weather_forecast("today", 1)
        assert result["days"] == 1
    
    @patch(f"{WEATHER_MODULE}.open_meteo_client")
    def test_invalid_date_parsing(self, mock_client):
        """Test handling of invalid date formats."""
        mock_client.get.return_value = _mock_http_response({
            "daily": {
                "time": ["2025-01-15"],
                "temperature_2m_max": [30.0],
                "temperature_2m_min": [25.0],
                "precipitation_sum": [0.0],
                "weathercode": [0],
                "windspeed_10m_max": [15.0],
                "sunrise": ["2025-01-15T06:00"],
                "sunset": ["2025-01-15T18:00"],
            }
        })
        
        result = get_weather_forecast("invalid-date", 1)
        assert result["days"] == 1
    
    @patch(f"{WEATHER_MODULE}.open_meteo_client")
    def test_forecast_date_range(self, mock_client, mock_open_meteo_response):
        """Test forecast retrieval with different date ranges."""
        mock_client.get.return_value = _mock_http_response(mock_open_meteo_response)
        
        result = get_weather_forecast("2025-01-15", 1)
        assert result["days"] == 1
        
        mock_open_meteo_response["daily"]["time"] = [
            f"2025-01-{15+i}" for i in range(7)
        ]
        mock_open_meteo_response["daily"]["temperature_2m_max"] = [30.0] * 7
        mock_open_meteo_response["daily"]["temperature_2m_min"] = [25.0] * 7
        mock_open_meteo_response["daily"]["precipitation_sum"] = [0.0] * 7
        mock_open_meteo_response["daily"]["weathercode"] = [0] * 7
        mock_open_meteo_response["daily"]["windspeed_10m_max"] = [15.0] * 7
        mock_open_meteo_response["daily"]["sunrise"] = [
            f"2025-01-{15+i}T06:00" for i in range(7)
        ]
        mock_open_meteo_response["daily"]["sunset"] = [
            f"2025-01-{15+i}T18:00" for i in range(7)
        ]
        
        result = get_weather_forecast("2025-01-15", 7)
        assert result["days"] == 7
        assert len(result["forecast"]) == 7

