"""Unit tests for itinerary tool handlers."""
import pytest
import sys
from unittest.mock import patch, Mock, AsyncMock


@pytest.fixture
def itinerary_tool_funcs():
    """Patch the mcp decorator and re-import to get raw handler functions."""
    decorator_patcher = patch(
        'mcp_server.mcp_instance.mcp.tool',
        lambda *args, **kwargs: (lambda f: f) if kwargs or args else (lambda f: f)
    )
    decorator_patcher.start()

    try:
        if 'mcp_server.handlers.tools.itinerary' in sys.modules:
            del sys.modules['mcp_server.handlers.tools.itinerary']
        from mcp_server.handlers.tools import itinerary
        yield itinerary
    finally:
        decorator_patcher.stop()
        if 'mcp_server.handlers.tools.itinerary' in sys.modules:
            del sys.modules['mcp_server.handlers.tools.itinerary']


@pytest.mark.unit
class TestGenerateItineraryTool:
    """Test generate_itinerary tool handler."""

    @pytest.mark.asyncio
    async def test_calls_service_and_returns_output(self, itinerary_tool_funcs):
        mod = itinerary_tool_funcs
        mock_ctx = Mock()
        mock_params = Mock()
        mock_params.start_date = "2025-01-15"
        mock_params.days = 3

        with patch.object(mod, "s_generate_itinerary", new_callable=AsyncMock) as mock_svc:
            mock_svc.return_value = "Generated itinerary content"
            result = await mod.generate_itinerary(mock_ctx, mock_params)

        assert result == "Generated itinerary content"
        mock_svc.assert_called_once_with(mock_ctx, "2025-01-15", 3)


@pytest.mark.unit
class TestGetActivitySuggestionsTool:
    """Test get_activity_suggestions tool handler."""

    @pytest.mark.asyncio
    async def test_calls_service_and_returns_list(self, itinerary_tool_funcs):
        mod = itinerary_tool_funcs
        mock_ctx = Mock()
        mock_params = Mock()
        mock_params.temperature = 28.0
        mock_params.time_of_day = "morning"

        with patch.object(mod, "s_get_activity_suggestions", new_callable=AsyncMock) as mock_svc:
            mock_svc.return_value = ["Beach walk", "Swimming"]
            result = await mod.get_activity_suggestions(mock_ctx, mock_params)

        assert result == ["Beach walk", "Swimming"]
        mock_svc.assert_called_once_with(28.0, "morning")
