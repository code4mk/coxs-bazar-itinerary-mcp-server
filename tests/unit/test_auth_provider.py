"""Unit tests for auth provider configuration."""
import pytest
from unittest.mock import patch, Mock, MagicMock


AUTH_MODULE = "mcp_server.config.auth_provider"


@pytest.mark.unit
class TestGetAuthProvider:
    """Test auth provider factory function."""

    @patch(f"{AUTH_MODULE}.get_client_storage")
    @patch(f"{AUTH_MODULE}.GitHubProvider")
    @patch(f"{AUTH_MODULE}.settings")
    def test_github_provider(self, mock_settings, mock_github_cls, mock_storage):
        from mcp_server.config.auth_provider import get_auth_provider
        mock_settings.github_client_id = "gh-id"
        mock_settings.github_client_secret = "gh-secret"
        mock_settings.resource_base_url = "http://localhost:8000"
        mock_settings.jwt_signing_key = "test-jwt-key"
        mock_storage.return_value = Mock()

        result = get_auth_provider("github")

        mock_github_cls.assert_called_once()
        call_kwargs = mock_github_cls.call_args[1]
        assert call_kwargs["client_id"] == "gh-id"
        assert call_kwargs["client_secret"] == "gh-secret"
        assert result == mock_github_cls.return_value

    @patch(f"{AUTH_MODULE}.get_client_storage")
    @patch(f"{AUTH_MODULE}.GitHubProvider")
    @patch(f"{AUTH_MODULE}.settings")
    def test_github_provider_case_insensitive(self, mock_settings, mock_github_cls, mock_storage):
        from mcp_server.config.auth_provider import get_auth_provider
        mock_settings.github_client_id = "gh-id"
        mock_settings.github_client_secret = "gh-secret"
        mock_settings.resource_base_url = "http://localhost:8000"
        mock_settings.jwt_signing_key = "test-jwt-key"
        mock_storage.return_value = Mock()

        get_auth_provider("GitHub")
        mock_github_cls.assert_called_once()

    @patch(f"{AUTH_MODULE}.get_client_storage")
    @patch(f"{AUTH_MODULE}.Auth0Provider")
    @patch(f"{AUTH_MODULE}.settings")
    def test_auth0_provider(self, mock_settings, mock_auth0_cls, mock_storage):
        from mcp_server.config.auth_provider import get_auth_provider
        mock_settings.auth0_domain = "test.auth0.com"
        mock_settings.auth0_client_id = "auth0-id"
        mock_settings.auth0_client_secret = "auth0-secret"
        mock_settings.auth0_audience = "https://api.test.com"
        mock_settings.resource_base_url = "http://localhost:8000"
        mock_settings.jwt_signing_key = "test-jwt-key"
        mock_storage.return_value = Mock()

        result = get_auth_provider("auth0")

        mock_auth0_cls.assert_called_once()
        call_kwargs = mock_auth0_cls.call_args[1]
        assert call_kwargs["client_id"] == "auth0-id"
        assert call_kwargs["client_secret"] == "auth0-secret"
        assert call_kwargs["audience"] == "https://api.test.com"
        assert "well-known/openid-configuration" in call_kwargs["config_url"]
        assert result == mock_auth0_cls.return_value

    @patch(f"{AUTH_MODULE}.get_client_storage")
    @patch(f"{AUTH_MODULE}.ClerkProvider")
    @patch(f"{AUTH_MODULE}.settings")
    def test_clerk_provider(self, mock_settings, mock_clerk_cls, mock_storage):
        from mcp_server.config.auth_provider import get_auth_provider
        mock_settings.clerk_domain = "test.clerk.dev"
        mock_settings.clerk_client_id = "clerk-id"
        mock_settings.clerk_client_secret = "clerk-secret"
        mock_settings.resource_base_url = "http://localhost:8000"
        mock_settings.jwt_signing_key = "test-jwt-key"
        mock_storage.return_value = Mock()

        result = get_auth_provider("clerk")

        mock_clerk_cls.assert_called_once()
        assert result == mock_clerk_cls.return_value

    def test_unsupported_provider_raises(self):
        from mcp_server.config.auth_provider import get_auth_provider
        with pytest.raises(ValueError, match="Unsupported provider"):
            get_auth_provider("unsupported")
