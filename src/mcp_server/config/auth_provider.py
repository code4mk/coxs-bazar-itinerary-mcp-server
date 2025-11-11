import os
from fastmcp.server.auth.providers.github import GitHubProvider
from key_value.aio.stores.redis import RedisStore

def get_auth_provider(provider_name: str):
  """Get the auth provider based on the provider name."""
  if provider_name.lower() == "github":
    # Get Redis configuration
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", "6379"))
    redis_password = os.getenv("REDIS_PASSWORD")
    
    # Get GitHub configuration
    github_client_id = os.getenv("GITHUB_CLIENT_ID")
    github_client_secret = os.getenv("GITHUB_CLIENT_SECRET")
    base_url = os.getenv("RESOURCE_BASE_URL", "http://localhost:8000")
    
    # Validate required configuration
    if not github_client_id or not github_client_secret:
      raise ValueError(
        "GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET must be set in environment variables"
      )
    
    # Create RedisStore with proper configuration
    redis_store = RedisStore(
      host=redis_host,
      port=redis_port,
      password=redis_password if redis_password else None,
      db=0
    )
    
    print(f"✓ Initializing GitHub OAuth with Redis storage at {redis_host}:{redis_port}")
    
    return GitHubProvider(
      client_id=github_client_id,
      client_secret=github_client_secret,
      base_url=base_url,
      client_storage=redis_store
    )
  else:
    raise ValueError(f"Unsupported provider: {provider_name}")