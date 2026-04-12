from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Settings for the MCP server."""

    model_config = SettingsConfigDict(extra="ignore", env_file=".env", env_ignore_empty=True)

    auth_enabled: bool = Field(default=False)
    auth_provider: str = Field(default="github")
    server_port: int = Field(default=8000)
    server_host: str = Field(default="127.0.0.1")
    transport_name: str = Field(default="http")
    resource_base_url: str | None = Field(default=None)

    # Redis settings
    redis_host: str = Field(default="localhost")
    redis_port: int = Field(default=6379)
    redis_password: str = Field(default="")
    storage_encryption_key: str = Field(default="")

    # GitHub settings
    github_client_id: str = Field(default="")
    github_client_secret: str = Field(default="")

    # Auth0 settings
    auth0_domain: str = Field(default="")
    auth0_client_id: str = Field(default="")
    auth0_client_secret: str = Field(default="")
    auth0_audience: str = Field(default="")

    # Clerk settings
    clerk_domain: str = Field(default="")
    clerk_client_id: str = Field(default="")
    clerk_client_secret: str = Field(default="")

    # JWT settings
    jwt_signing_key: str = Field(default="")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Get the settings.

    Cached to avoid re-reading the environment variables on each call.
    """
    return Settings()


settings = get_settings()
