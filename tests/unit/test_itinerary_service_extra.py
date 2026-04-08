"""Additional tests for itinerary service to reach full coverage."""
import pytest
from mcp_server.services.itenerary_service import s_get_activity_suggestions


@pytest.mark.unit
class TestGetActivitySuggestionsService:
    """Test s_get_activity_suggestions service function directly."""

    @pytest.mark.asyncio
    async def test_returns_activity_list(self):
        result = await s_get_activity_suggestions(28.0, "morning")
        assert isinstance(result, list)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_afternoon_suggestions(self):
        result = await s_get_activity_suggestions(32.0, "afternoon")
        assert isinstance(result, list)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_evening_suggestions(self):
        result = await s_get_activity_suggestions(25.0, "evening")
        assert isinstance(result, list)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_default_time_of_day(self):
        result = await s_get_activity_suggestions(28.0)
        assert isinstance(result, list)
        assert len(result) > 0
