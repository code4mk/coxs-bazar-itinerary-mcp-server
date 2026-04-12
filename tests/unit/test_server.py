"""Unit tests for the main server module."""
import pytest
from unittest.mock import patch, Mock
from mcp_server.config.settings import Settings


SERVER_MODULE = "mcp_server.server"


def _make_settings(**overrides) -> Settings:
    defaults = {
        "transport_name": "http",
        "server_port": 8000,
        "server_host": "127.0.0.1",
    }
    defaults.update(overrides)
    return Settings(**defaults)


@pytest.mark.unit
class TestServerMain:
    """Test server main() entry point."""

    @patch(f"{SERVER_MODULE}.mcp")
    @patch(f"{SERVER_MODULE}.FileSystemProvider")
    @patch(f"{SERVER_MODULE}.RateLimitingMiddleware")
    @patch(f"{SERVER_MODULE}.settings", _make_settings(transport_name="stdio"))
    def test_main_stdio_transport(self, mock_rate_limit, mock_fsp, mock_mcp):
        from mcp_server.server import main
        mock_mcp.providers = []
        mock_mcp.add_middleware = Mock()

        main()

        mock_mcp.run.assert_called_once_with(transport="stdio")

    @patch(f"{SERVER_MODULE}.mcp")
    @patch(f"{SERVER_MODULE}.FileSystemProvider")
    @patch(f"{SERVER_MODULE}.RateLimitingMiddleware")
    @patch(f"{SERVER_MODULE}.settings", _make_settings(
        transport_name="http", server_port=9000, server_host="127.0.0.1"
    ))
    def test_main_http_transport(self, mock_rate_limit, mock_fsp, mock_mcp):
        from mcp_server.server import main
        mock_mcp.providers = []
        mock_mcp.add_middleware = Mock()

        main()

        mock_mcp.run.assert_called_once_with(
            transport="http", port=9000, host="127.0.0.1"
        )

    @patch(f"{SERVER_MODULE}.mcp")
    @patch(f"{SERVER_MODULE}.FileSystemProvider")
    @patch(f"{SERVER_MODULE}.RateLimitingMiddleware")
    @patch(f"{SERVER_MODULE}.settings", _make_settings(
        transport_name="streamable-http", server_port=8080, server_host="0.0.0.0"
    ))
    def test_main_streamable_http_transport(self, mock_rate_limit, mock_fsp, mock_mcp):
        from mcp_server.server import main
        mock_mcp.providers = []
        mock_mcp.add_middleware = Mock()

        main()

        mock_mcp.run.assert_called_once_with(
            transport="streamable-http", port=8080, host="0.0.0.0"
        )

    @patch(f"{SERVER_MODULE}.mcp")
    @patch(f"{SERVER_MODULE}.FileSystemProvider")
    @patch(f"{SERVER_MODULE}.RateLimitingMiddleware")
    @patch(f"{SERVER_MODULE}.settings", _make_settings(
        transport_name="sse", server_port=8000, server_host="0.0.0.0"
    ))
    def test_main_sse_transport(self, mock_rate_limit, mock_fsp, mock_mcp):
        from mcp_server.server import main
        mock_mcp.providers = []
        mock_mcp.add_middleware = Mock()

        main()

        mock_mcp.run.assert_called_once_with(
            transport="sse", port=8000, host="0.0.0.0"
        )

    @patch(f"{SERVER_MODULE}.mcp")
    @patch(f"{SERVER_MODULE}.FileSystemProvider")
    @patch(f"{SERVER_MODULE}.RateLimitingMiddleware")
    @patch(f"{SERVER_MODULE}.settings", _make_settings(transport_name="stdio"))
    def test_main_default_transport(self, mock_rate_limit, mock_fsp, mock_mcp):
        from mcp_server.server import main
        mock_mcp.providers = []
        mock_mcp.add_middleware = Mock()

        main()

        mock_mcp.run.assert_called_once_with(transport="stdio")

    @patch(f"{SERVER_MODULE}.mcp")
    @patch(f"{SERVER_MODULE}.FileSystemProvider")
    @patch(f"{SERVER_MODULE}.RateLimitingMiddleware")
    @patch(f"{SERVER_MODULE}.settings", _make_settings(
        transport_name="http", server_port=8000, server_host="0.0.0.0"
    ))
    def test_main_registers_providers(self, mock_rate_limit, mock_fsp, mock_mcp):
        from mcp_server.server import main
        mock_mcp.providers = []
        mock_mcp.add_middleware = Mock()

        main()

        assert mock_fsp.call_count == 2
        assert len(mock_mcp.providers) == 2

    @patch(f"{SERVER_MODULE}.mcp")
    @patch(f"{SERVER_MODULE}.FileSystemProvider")
    @patch(f"{SERVER_MODULE}.RateLimitingMiddleware")
    @patch(f"{SERVER_MODULE}.settings", _make_settings(transport_name="stdio"))
    def test_main_adds_rate_limiting(self, mock_rate_limit, mock_fsp, mock_mcp):
        from mcp_server.server import main
        mock_mcp.providers = []
        mock_mcp.add_middleware = Mock()

        main()

        mock_rate_limit.assert_called_once()
        mock_mcp.add_middleware.assert_called_once()
