from fastmcp import FastMCP
from mcp_server.config.auth_provider import get_auth_provider
from mcp_server.config.settings import settings

# Configuration for MCP initialization
mcp_config_context = {
    "name": "Cox's Bazar AI Itinerary MCP",
}

# Add auth if auth is enabled
is_auth_enabled = settings.auth_enabled

if is_auth_enabled:
    auth_provider = settings.auth_provider
    mcp_config_context["auth"] = get_auth_provider(auth_provider)


# Initialize FastMCP with valid parameters only
mcp = FastMCP(**mcp_config_context, strict_input_validation=True)
