"""Unit tests for auth-related tool handlers."""
import pytest
import sys
from unittest.mock import patch, Mock, AsyncMock


def _noop_tool_decorator(*args, **kwargs):
    """No-op replacement for mcp.tool that handles both @mcp.tool and @mcp.tool(...)."""
    if args and callable(args[0]):
        return args[0]
    return lambda f: f


@pytest.fixture
def auth_tool_funcs():
    """Patch the mcp decorator and re-import to get raw handler functions."""
    decorator_patcher = patch(
        'mcp_server.mcp_instance.mcp.tool',
        _noop_tool_decorator
    )
    decorator_patcher.start()

    try:
        if 'mcp_server.handlers.tools.auth_additional' in sys.modules:
            del sys.modules['mcp_server.handlers.tools.auth_additional']
        from mcp_server.handlers.tools import auth_additional
        yield auth_additional
    finally:
        decorator_patcher.stop()
        if 'mcp_server.handlers.tools.auth_additional' in sys.modules:
            del sys.modules['mcp_server.handlers.tools.auth_additional']


@pytest.mark.unit
class TestGetUserInfoTool:
    """Test get_user_info tool handler."""

    @pytest.mark.asyncio
    @patch.dict("os.environ", {"AUTH_PROVIDER": "github"})
    async def test_github_provider(self, auth_tool_funcs):
        mod = auth_tool_funcs
        mock_token = Mock()
        mock_token.claims = {
            "login": "testuser",
            "name": "Test User",
            "email": "test@example.com"
        }

        with patch.object(mod, "get_access_token", return_value=mock_token):
            result = await mod.get_user_info()

        assert result["github_user"] == "testuser"
        assert result["name"] == "Test User"
        assert result["email"] == "test@example.com"

    @pytest.mark.asyncio
    @patch.dict("os.environ", {"AUTH_PROVIDER": "auth0"})
    async def test_auth0_provider(self, auth_tool_funcs):
        mod = auth_tool_funcs
        mock_token = Mock()
        mock_token.token = "raw-access-token"
        mock_token.claims = {
            "iss": "https://test.auth0.com/",
            "aud": "https://api.test.com",
            "scope": "openid profile email",
            "permissions": ["read:data"],
        }

        mock_user_info = {"sub": "auth0|123", "email": "test@example.com"}

        with patch.object(mod, "get_access_token", return_value=mock_token), \
             patch.object(mod, "get_auth0_user_info", return_value=mock_user_info):
            result = await mod.get_user_info()

        assert result["issuer"] == "https://test.auth0.com/"
        assert result["user_info"] == mock_user_info


@pytest.mark.unit
class TestCustomAuthTool:
    """Test custom_auth_tool handler."""

    @pytest.mark.asyncio
    async def test_returns_message(self, auth_tool_funcs):
        mod = auth_tool_funcs
        mock_token = Mock()

        with patch.object(mod, "get_access_token", return_value=mock_token):
            result = await mod.custom_auth_tool()

        assert result == {"message": "Custom auth tool"}


@pytest.mark.unit
class TestRequestInfoTool:
    """Test request_info tool handler."""

    @pytest.mark.asyncio
    async def test_returns_request_info(self, auth_tool_funcs):
        mod = auth_tool_funcs
        mock_ctx = Mock()
        mock_ctx.request_id = "req-123"
        mock_ctx.client_id = "client-456"

        with patch.object(mod, "get_client_ip", return_value="10.0.0.1"), \
             patch.object(mod, "get_user_agent", return_value="TestAgent/1.0"), \
             patch.object(mod, "get_mcp_session_id", return_value="sess-789"):
            result = await mod.request_info(mock_ctx)

        assert result["request_id"] == "req-123"
        assert result["client_id"] == "client-456"
        assert result["client_ip"] == "10.0.0.1"
        assert result["user_agent"] == "TestAgent/1.0"
        assert result["session_id"] == "sess-789"

    @pytest.mark.asyncio
    async def test_returns_unknown_client_when_none(self, auth_tool_funcs):
        mod = auth_tool_funcs
        mock_ctx = Mock()
        mock_ctx.request_id = "req-123"
        mock_ctx.client_id = None

        with patch.object(mod, "get_client_ip", return_value="Unknown"), \
             patch.object(mod, "get_user_agent", return_value="Unknown"), \
             patch.object(mod, "get_mcp_session_id", return_value="sess-1"):
            result = await mod.request_info(mock_ctx)

        assert result["client_id"] == "Unknown client"
