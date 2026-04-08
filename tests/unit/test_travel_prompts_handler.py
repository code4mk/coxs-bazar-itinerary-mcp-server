"""Unit tests for travel prompts handler."""
import pytest
import sys
from unittest.mock import patch, AsyncMock


@pytest.fixture
def travel_prompt_func():
    """Patch the mcp decorator and re-import to get raw handler function."""
    decorator_patcher = patch(
        'mcp_server.mcp_instance.mcp.prompt',
        lambda *args, **kwargs: (lambda f: f) if kwargs or args else (lambda f: f)
    )
    decorator_patcher.start()

    try:
        if 'mcp_server.handlers.prompts.travel_prompts' in sys.modules:
            del sys.modules['mcp_server.handlers.prompts.travel_prompts']
        from mcp_server.handlers.prompts import travel_prompts
        yield travel_prompts
    finally:
        decorator_patcher.stop()
        if 'mcp_server.handlers.prompts.travel_prompts' in sys.modules:
            del sys.modules['mcp_server.handlers.prompts.travel_prompts']


@pytest.mark.unit
class TestGenerateItineraryPromptHandler:
    """Test the generate_itinerary_prompt handler."""

    @pytest.mark.asyncio
    async def test_delegates_to_prompt_template(self, travel_prompt_func):
        mod = travel_prompt_func

        with patch.object(mod, "get_itinerary_prompt", new_callable=AsyncMock) as mock_prompt:
            mock_prompt.return_value = "Itinerary prompt for 3 days"
            result = await mod.generate_itinerary_prompt(3, "2025-01-15")

        assert result == "Itinerary prompt for 3 days"
        mock_prompt.assert_called_once_with(3, "2025-01-15")

    @pytest.mark.asyncio
    async def test_with_different_parameters(self, travel_prompt_func):
        mod = travel_prompt_func

        with patch.object(mod, "get_itinerary_prompt", new_callable=AsyncMock) as mock_prompt:
            mock_prompt.return_value = "Itinerary prompt for 7 days"
            result = await mod.generate_itinerary_prompt(7, "2025-06-01")

        assert result == "Itinerary prompt for 7 days"
        mock_prompt.assert_called_once_with(7, "2025-06-01")
