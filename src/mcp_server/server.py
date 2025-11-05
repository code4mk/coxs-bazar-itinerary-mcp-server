"""Main FastMCP server for Cox's Bazar AI Itinerary."""
import sys
import os
from pathlib import Path
from typing import Any
# Add src directory to path if running directly
if __name__ == "__main__" or "mcp_server" not in sys.modules:
    src_path = Path(__file__).parent.parent  # This points to src/
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mcp_server.utils.register_mcp_components import register_mcp_components
from mcp_server.utils.types import FastMCPConfigDict


load_dotenv()
# Get transport name and port from environment variables
transport_name = os.environ.get("TRANSPORT_NAME") or "stdio"
port = os.environ.get("PORT") or 8000
base_dir = Path(__file__).parent
fast_mcp_config: FastMCPConfigDict = {
    "name": "Cox's Bazar AI Itinerary MCP"
}

if transport_name == "sse" or transport_name == "streamable-http":
    fast_mcp_config["host"] = "0.0.0.0"
    fast_mcp_config["port"] = int(port)
    

mcp = FastMCP[Any](**fast_mcp_config)

# Auto-register all MCP components (tools, prompts, resources)
register_mcp_components(mcp, base_dir)

def main():
    """Run the MCP server."""
    print("🌴 Starting Cox's Bazar AI Itinerary MCP server...")
    print("📍 Location: Cox's Bazar, Bangladesh")
    print("🚀 Server ready!")
    mcp.run(transport=transport_name)

if __name__ == "__main__":
    main()