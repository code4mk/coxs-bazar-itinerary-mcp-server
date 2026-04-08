"""Unit tests for the main server module."""
import pytest
import sys
from unittest.mock import patch, Mock, MagicMock
from pathlib import Path


SERVER_MODULE = "mcp_server.server"


@pytest.mark.unit
class TestServerMain:
    """Test server main() entry point."""

    @patch(f"{SERVER_MODULE}.mcp")
    @patch(f"{SERVER_MODULE}.FileSystemProvider")
    @patch(f"{SERVER_MODULE}.RateLimitingMiddleware")
    @patch.dict("os.environ", {
        "TRANSPORT_NAME": "stdio",
    }, clear=False)
    def test_main_stdio_transport(self, mock_rate_limit, mock_fsp, mock_mcp):
        from mcp_server.server import main
        mock_mcp.providers = []
        mock_mcp.add_middleware = Mock()

        main()

        mock_mcp.run.assert_called_once_with(transport="stdio")

    @patch(f"{SERVER_MODULE}.mcp")
    @patch(f"{SERVER_MODULE}.FileSystemProvider")
    @patch(f"{SERVER_MODULE}.RateLimitingMiddleware")
    @patch.dict("os.environ", {
        "TRANSPORT_NAME": "http",
        "SERVER_PORT": "9000",
        "SERVER_HOST": "127.0.0.1",
    }, clear=False)
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
    @patch.dict("os.environ", {
        "TRANSPORT_NAME": "streamable-http",
        "SERVER_PORT": "8080",
        "SERVER_HOST": "0.0.0.0",
    }, clear=False)
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
    @patch.dict("os.environ", {
        "TRANSPORT_NAME": "sse",
        "SERVER_PORT": "8000",
        "SERVER_HOST": "0.0.0.0",
    }, clear=False)
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
    @patch.dict("os.environ", {}, clear=False)
    def test_main_default_transport(self, mock_rate_limit, mock_fsp, mock_mcp):
        from mcp_server.server import main
        mock_mcp.providers = []
        mock_mcp.add_middleware = Mock()

        env_backup = {}
        for key in ("TRANSPORT_NAME", "SERVER_PORT", "SERVER_HOST"):
            import os
            env_backup[key] = os.environ.pop(key, None)

        try:
            main()
            mock_mcp.run.assert_called_once_with(transport="stdio")
        finally:
            for key, val in env_backup.items():
                if val is not None:
                    os.environ[key] = val

    @patch(f"{SERVER_MODULE}.mcp")
    @patch(f"{SERVER_MODULE}.FileSystemProvider")
    @patch(f"{SERVER_MODULE}.RateLimitingMiddleware")
    @patch.dict("os.environ", {
        "TRANSPORT_NAME": "http",
        "SERVER_PORT": "8000",
        "SERVER_HOST": "0.0.0.0",
    }, clear=False)
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
    @patch.dict("os.environ", {
        "TRANSPORT_NAME": "stdio",
    }, clear=False)
    def test_main_adds_rate_limiting(self, mock_rate_limit, mock_fsp, mock_mcp):
        from mcp_server.server import main
        mock_mcp.providers = []
        mock_mcp.add_middleware = Mock()

        main()

        mock_rate_limit.assert_called_once()
        mock_mcp.add_middleware.assert_called_once()
