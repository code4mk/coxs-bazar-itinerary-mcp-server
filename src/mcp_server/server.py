"""Main FastMCP server for Cox's Bazar AI Itinerary."""
import sys
from pathlib import Path
from typing import Any

# Add src directory to path if running directly
if __name__ == "__main__" or "mcp_server" not in sys.modules:
    src_path = Path(__file__).parent.parent  # This points to src/
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

from mcp.server.fastmcp import FastMCP
from mcp_server.utils.register_mcp_components import register_mcp_components

# Create the FastMCP server
mcp = FastMCP[Any]("Cox's Bazar AI Itinerary MCP")

# Get the base directory
base_dir = Path(__file__).parent

# Auto-register all MCP components (tools, prompts, resources)
register_mcp_components(mcp, base_dir)

def main():
    """Run the MCP server."""
    print("🌴 Starting Cox's Bazar AI Itinerary MCP server...")
    print("📍 Location: Cox's Bazar, Bangladesh")
    print("🚀 Server ready!")
    mcp.run()

if __name__ == "__main__":
    main()