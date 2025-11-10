import os
from fastmcp import FastMCP
from mcp_server.config.auth_provider import get_auth_provider
from dotenv import load_dotenv
from mcp.types import Icon

load_dotenv()

is_oauth_enabled = os.environ.get("IS_OAUTH_ENABLED") == "true"
mcp_config_context = {
    "name": "Cox's Bazar AI Itinerary MCP",
    "icons": [
        Icon(
            src="https://raw.githubusercontent.com/code4mk/coxs-bazar-itinerary-mcp-server/refs/heads/main/cox-mcp.jpeg",
            mimeType="image/jpeg",
            sizes=["48x48"]
        )
    ]
}


if is_oauth_enabled:
    mcp_config_context["auth"] = get_auth_provider("github")


mcp = FastMCP(**mcp_config_context)

