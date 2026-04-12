from key_value.aio.stores.redis import RedisStore
from key_value.aio.wrappers.encryption import FernetEncryptionWrapper
from cryptography.fernet import Fernet
from mcp_server.config.settings import settings
from fastmcp.server.auth.providers.github import GitHubProvider
from fastmcp.server.auth.providers.auth0 import Auth0Provider
from mcp_server.lib.clerk_auth_provider import ClerkProvider


def get_client_storage() -> FernetEncryptionWrapper:
    """Get the client storage."""
    return FernetEncryptionWrapper(
        key_value=RedisStore(
            host=settings.redis_host,
            port=settings.redis_port,
            password=settings.redis_password,
        ),
        fernet=Fernet(settings.storage_encryption_key),
    )


def get_auth_provider(provider_name: str) -> GitHubProvider | Auth0Provider | ClerkProvider:
    """Get the auth provider based on the provider name."""
    if provider_name.lower() == "github":
        # Get GitHub configuration
        github_client_id = settings.github_client_id
        github_client_secret = settings.github_client_secret
        base_url = settings.resource_base_url
        client_storage = get_client_storage()
        jwt_signing_key = settings.jwt_signing_key

        return GitHubProvider(
            client_id=github_client_id,
            client_secret=github_client_secret,
            base_url=base_url,
            # Production token management
            jwt_signing_key=jwt_signing_key,
            client_storage=client_storage,
        )
    if provider_name.lower() == "auth0":
        auth0_domain = settings.auth0_domain
        auth0_client_id = settings.auth0_client_id
        auth0_client_secret = settings.auth0_client_secret
        auth0_audience = settings.auth0_audience
        base_url = settings.resource_base_url
        client_storage = get_client_storage()
        jwt_signing_key = settings.jwt_signing_key
        auth0_config_url = f"https://{auth0_domain}/.well-known/openid-configuration"

        return Auth0Provider(
            config_url=auth0_config_url,
            client_id=auth0_client_id,
            client_secret=auth0_client_secret,
            audience=auth0_audience,
            base_url=base_url,
            required_scopes=["openid", "profile", "email"],
            jwt_signing_key=jwt_signing_key,
            client_storage=client_storage,
        )
    if provider_name.lower() == "clerk":
        clerk_domain = settings.clerk_domain
        clerk_client_id = settings.clerk_client_id
        clerk_client_secret = settings.clerk_client_secret
        base_url = settings.resource_base_url
        client_storage = get_client_storage()
        jwt_signing_key = settings.jwt_signing_key

        return ClerkProvider(
            domain=clerk_domain,
            client_id=clerk_client_id,
            client_secret=clerk_client_secret,
            base_url=base_url,
            required_scopes=["openid", "email", "profile"],
            jwt_signing_key=jwt_signing_key,
            client_storage=client_storage,
        )
    msg = f"Unsupported provider: {provider_name}"
    raise ValueError(msg)
