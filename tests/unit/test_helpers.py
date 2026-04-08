"""Unit tests for helper utility functions."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime


@pytest.mark.unit
class TestFormatDate:
    """Test date formatting utility."""

    def test_format_today(self):
        from mcp_server.utils.helpers import format_date
        result = format_date("today")
        expected = datetime.today().strftime("%d %b %Y")
        assert result == expected

    def test_format_valid_date_string(self):
        from mcp_server.utils.helpers import format_date
        result = format_date("2025-01-15")
        assert result == "15 Jan 2025"

    def test_format_verbose_date(self):
        from mcp_server.utils.helpers import format_date
        result = format_date("January 15, 2025")
        assert result == "15 Jan 2025"

    def test_format_invalid_date_returns_today(self):
        from mcp_server.utils.helpers import format_date
        result = format_date("not-a-date-at-all")
        expected = datetime.today().strftime("%d %b %Y")
        assert result == expected


@pytest.mark.unit
class TestValidateDays:
    """Test day count validation."""

    def test_valid_days(self):
        from mcp_server.utils.helpers import validate_days
        assert validate_days(5) == 5

    def test_below_minimum(self):
        from mcp_server.utils.helpers import validate_days
        assert validate_days(0) == 1
        assert validate_days(-3) == 1

    def test_above_maximum(self):
        from mcp_server.utils.helpers import validate_days
        assert validate_days(15) == 14
        assert validate_days(100) == 14

    def test_boundary_values(self):
        from mcp_server.utils.helpers import validate_days
        assert validate_days(1) == 1
        assert validate_days(14) == 14


@pytest.mark.unit
class TestFormatTemperature:
    """Test temperature formatting with descriptions."""

    def test_cool_temperature(self):
        from mcp_server.utils.helpers import format_temperature
        result = format_temperature(18.0)
        assert "18.0°C" in result
        assert "Cool" in result

    def test_pleasant_temperature(self):
        from mcp_server.utils.helpers import format_temperature
        result = format_temperature(22.5)
        assert "22.5°C" in result
        assert "Pleasant" in result

    def test_warm_temperature(self):
        from mcp_server.utils.helpers import format_temperature
        result = format_temperature(27.0)
        assert "27.0°C" in result
        assert "Warm" in result

    def test_hot_temperature(self):
        from mcp_server.utils.helpers import format_temperature
        result = format_temperature(32.0)
        assert "32.0°C" in result
        assert "Hot" in result

    def test_very_hot_temperature(self):
        from mcp_server.utils.helpers import format_temperature
        result = format_temperature(38.0)
        assert "38.0°C" in result
        assert "Very Hot" in result


@pytest.mark.unit
class TestRequirePermissions:
    """Test permission-checking auth helper."""

    def test_returns_true_with_matching_permissions(self):
        from mcp_server.utils.helpers import require_permissions
        checker = require_permissions("tool:read", "tool:write")

        ctx = Mock()
        ctx.token = Mock()
        ctx.token.claims = {"permissions": ["tool:read", "tool:write", "tool:admin"]}

        assert checker(ctx) is True

    def test_returns_false_with_missing_permissions(self):
        from mcp_server.utils.helpers import require_permissions
        checker = require_permissions("tool:read", "tool:admin")

        ctx = Mock()
        ctx.token = Mock()
        ctx.token.claims = {"permissions": ["tool:read"]}

        assert checker(ctx) is False

    def test_returns_false_when_no_token(self):
        from mcp_server.utils.helpers import require_permissions
        checker = require_permissions("tool:read")

        ctx = Mock()
        ctx.token = None

        assert checker(ctx) is False

    def test_returns_false_with_empty_permissions(self):
        from mcp_server.utils.helpers import require_permissions
        checker = require_permissions("tool:read")

        ctx = Mock()
        ctx.token = Mock()
        ctx.token.claims = {"permissions": []}

        assert checker(ctx) is False


@pytest.mark.unit
class TestRequirePremiumUser:
    """Test premium user auth helper."""

    def test_returns_true_with_token(self):
        from mcp_server.utils.helpers import require_premium_user
        ctx = Mock()
        ctx.token = Mock()
        assert require_premium_user(ctx) is True

    def test_returns_false_without_token(self):
        from mcp_server.utils.helpers import require_premium_user
        ctx = Mock()
        ctx.token = None
        assert require_premium_user(ctx) is False


@pytest.mark.unit
class TestGetClientIp:
    """Test client IP extraction."""

    @patch("mcp_server.utils.helpers.get_http_request")
    def test_returns_client_host(self, mock_get_request):
        from mcp_server.utils.helpers import get_client_ip
        mock_request = Mock()
        mock_request.client = Mock()
        mock_request.client.host = "192.168.1.1"
        mock_get_request.return_value = mock_request

        assert get_client_ip() == "192.168.1.1"

    @patch("mcp_server.utils.helpers.get_http_request")
    def test_returns_unknown_when_no_client(self, mock_get_request):
        from mcp_server.utils.helpers import get_client_ip
        mock_request = Mock()
        mock_request.client = None
        mock_get_request.return_value = mock_request

        assert get_client_ip() == "Unknown"


@pytest.mark.unit
class TestGetUserAgent:
    """Test user agent extraction."""

    @patch("mcp_server.utils.helpers.get_http_headers")
    def test_returns_user_agent(self, mock_get_headers):
        from mcp_server.utils.helpers import get_user_agent
        mock_get_headers.return_value = {"user-agent": "TestClient/1.0"}
        assert get_user_agent() == "TestClient/1.0"

    @patch("mcp_server.utils.helpers.get_http_headers")
    def test_returns_unknown_when_missing(self, mock_get_headers):
        from mcp_server.utils.helpers import get_user_agent
        mock_get_headers.return_value = {}
        assert get_user_agent() == "Unknown"


@pytest.mark.unit
class TestGetMcpSessionId:
    """Test MCP session ID extraction."""

    @patch("mcp_server.utils.helpers.get_context")
    def test_returns_session_id(self, mock_get_context):
        from mcp_server.utils.helpers import get_mcp_session_id
        mock_ctx = Mock()
        mock_ctx.session_id = "session-abc-123"
        mock_get_context.return_value = mock_ctx
        assert get_mcp_session_id() == "session-abc-123"


@pytest.mark.unit
class TestGetMcpClientName:
    """Test MCP client name extraction."""

    @patch("mcp_server.utils.helpers.get_context")
    def test_returns_client_name(self, mock_get_context):
        from mcp_server.utils.helpers import get_mcp_client_name
        mock_ctx = Mock()
        mock_ctx.request_context.session.client_params.clientInfo.name = "TestMCPClient"
        mock_get_context.return_value = mock_ctx
        assert get_mcp_client_name() == "TestMCPClient"


@pytest.mark.unit
class TestGetAuth0UserInfo:
    """Test Auth0 user info retrieval."""

    @patch("mcp_server.utils.helpers.requests.get")
    @patch.dict("os.environ", {"AUTH0_DOMAIN": "test.auth0.com"})
    def test_returns_user_info(self, mock_get):
        from mcp_server.utils.helpers import get_auth0_user_info
        mock_response = Mock()
        mock_response.json.return_value = {"sub": "auth0|123", "email": "test@example.com"}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = get_auth0_user_info("fake-token")

        assert result["sub"] == "auth0|123"
        assert result["email"] == "test@example.com"
        mock_get.assert_called_once_with(
            "https://test.auth0.com/userinfo",
            headers={"Authorization": "Bearer fake-token"}
        )

    @patch("mcp_server.utils.helpers.requests.get")
    @patch.dict("os.environ", {"AUTH0_DOMAIN": "test.auth0.com"})
    def test_raises_on_http_error(self, mock_get):
        from mcp_server.utils.helpers import get_auth0_user_info
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("401 Unauthorized")
        mock_get.return_value = mock_response

        with pytest.raises(Exception, match="401 Unauthorized"):
            get_auth0_user_info("bad-token")
